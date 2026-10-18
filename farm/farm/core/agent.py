"""The thin ReAct agent — one loop for every profile (blueprint §4).

Observation → thought → one tool call → observation, with the three things the
blueprint insists on: a triple budget (steps/tokens/time) that hard-stops
instead of looping, stall detection that escalates Flash→Pro on the *same*
trajectory (just a different `tier` on the next call), and a shared blackboard.

It is domain-agnostic: the profile supplies the system prompt and the tools
(including the terminal tool). "Done" means a terminal tool recorded a
`Candidate` on the context — the agent never knows whether that candidate is a
flag, an answer, or a program.
"""
from __future__ import annotations

import hashlib
import json
import time
from typing import Dict, List, Optional

from ..config import Budgets, CascadePolicy, SETTINGS
from ..gateway.client import Ledger, ModelGateway
from ..gateway.types import ToolCall
from ..memory.blackboard import Blackboard
from ..observability.tracing import Tracer
from ..sandbox.base import Sandbox
from .contracts import AttemptResult, Task
from .toolset import ToolContext, ToolSet


def _user_prompt(task: Task, file_listing: str, recon: str, fewshot: str,
                 shared: str) -> str:
    blocks = [f"# Task: {task.name}",
              f"Answer format: {task.answer_format or '(not specified)'}",
              "## Description", task.statement.strip() or "(no description)"]
    if task.endpoint:
        blocks.append(f"## Live target\n{task.endpoint}")
    if file_listing:
        blocks.append("## Files in the working directory\n" + file_listing)
    if recon:
        blocks.append(recon)
    if fewshot:                    # RAG demonstrations from the solution bank
        blocks.append(fewshot)
    if shared:
        blocks.append(shared)
    blocks.append("Begin. Investigate, solve, verify, then submit via the terminal tool.")
    return "\n\n".join(blocks)


def _assistant_msg(text: str, tool_calls: List[ToolCall]) -> Dict:
    return {"role": "assistant", "content": text or None,
            "tool_calls": [{"id": tc.id, "type": "function",
                            "function": {"name": tc.name,
                                         "arguments": json.dumps(tc.arguments)}}
                           for tc in tool_calls]}


class ReActAgent:
    def __init__(self, gateway: ModelGateway, blackboard: Blackboard,
                 budgets: Budgets = None, cascade: CascadePolicy = None):
        self.gw = gateway
        self.bb = blackboard
        self.budgets = budgets or SETTINGS.budgets
        self.cascade = cascade or SETTINGS.cascade

    def run(self, *, task: Task, toolset: ToolSet, system_prompt: str, author: str,
            temperature: float = 0.2, start_tier: str = "flash",
            sandbox: Sandbox, recon: str = "", fewshot: str = "", cancel_event=None,
            max_steps_override: Optional[int] = None) -> AttemptResult:
        max_steps = max_steps_override or self.budgets.max_steps
        tracer = Tracer(meta={"task": task.id, "author": author,
                              "category": task.category, "temp": temperature})
        ledger = Ledger()
        tools = toolset.tools
        schemas = toolset.schemas()
        by_name = toolset.by_name()
        ctx = ToolContext(sandbox=sandbox, blackboard=self.bb,
                          task_id=task.id, author=author)

        file_listing = "\n".join(f"- {f}" for f in sandbox.list_files(".")[:100])
        recon_block = (f"## Automated recon:\n{recon}" if recon else "")
        shared = self.bb.render_for_prompt(task.id, exclude_author=author)
        messages: List[Dict] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": _user_prompt(
                task, file_listing, recon_block, fewshot, shared)}]

        tier, tiers_used = start_tier, [start_tier]
        started = time.time()
        seen_obs: set = set()
        stall = 0
        tool_counts: Dict[str, int] = {}
        outcome, reason = "failed", "exhausted steps"

        for step in range(1, max_steps + 1):
            if cancel_event is not None and cancel_event.is_set():
                outcome, reason = "killed", "cancelled: sibling solved first"
                break
            if time.time() - started > self.budgets.max_seconds:
                outcome, reason = "killed", "time budget exceeded"
                break
            if ledger.prompt_tokens + ledger.completion_tokens > self.budgets.max_tokens:
                outcome, reason = "killed", "token budget exceeded"
                break

            sp = tracer.start("llm", tier)
            try:
                resp = self.gw.chat(messages=messages, tier=tier, tools=schemas,
                                    temperature=temperature,
                                    max_tokens=self.budgets.max_tokens_per_call, ledger=ledger)
            except Exception as e:  # noqa: BLE001
                tracer.finish(sp, result=f"gateway error: {e}")
                outcome, reason = "error", f"gateway error: {e}"
                break
            tracer.finish(sp, tokens_in=resp.usage.prompt_tokens,
                          tokens_out=resp.usage.completion_tokens,
                          cost_usd=resp.cost_usd, result=resp.text[:400])

            if not resp.has_tool_calls:
                reason = (resp.text or "no tool call").strip()[:200]
                outcome = "stalled" if ("no further progress" in reason.lower()
                                        or "exhausted" in reason.lower()) else "failed"
                self.bb.mark_dead_end(task.id, f"{author}: no-op", reason)
                break

            messages.append(_assistant_msg(resp.text, resp.tool_calls))
            terminal_hit = new_fact = False
            for tc in resp.tool_calls:
                tool = by_name.get(tc.name)
                tool_counts[tc.name] = tool_counts.get(tc.name, 0) + 1
                if tool is None:
                    obs = f"error: unknown tool '{tc.name}'"
                else:
                    tsp = tracer.start("tool", tc.name, payload=tc.arguments)
                    obs = tool.fn(tc.arguments, ctx)
                    tracer.finish(tsp, result=obs)
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
                oh = hashlib.md5(obs.encode()).hexdigest()
                if oh not in seen_obs and not obs.lower().startswith(
                        ("error", "rejected", "skipped")):
                    new_fact = True
                seen_obs.add(oh)
                if tool is not None and tool.terminal and ctx.candidate is not None:
                    terminal_hit = True

            if terminal_hit:
                outcome, reason = "solved", "candidate recorded"
                break

            stall = 0 if new_fact else stall + 1
            if stall >= self.budgets.stall_steps:
                if self.cascade.enabled and tier == self.cascade.default_model \
                        and self._may_escalate(ledger):
                    tier = self.cascade.escalation_model
                    tiers_used.append(tier)
                    stall = 0
                    tracer.note("escalate", to=tier, at_step=step)
                    messages.append({"role": "user", "content":
                        "You seem stuck. A stronger model now continues. Re-examine "
                        "the evidence and try a different angle. "
                        + self.bb.render_for_prompt(task.id, exclude_author=author)})
                else:
                    outcome, reason = "stalled", "no progress; stall budget hit"
                    self.bb.mark_dead_end(task.id, f"{author}: stalled",
                                          "no new facts for N steps")
                    break

        tracer.close({"outcome": outcome, "candidate":
                      (ctx.candidate.value if ctx.candidate else None),
                      "steps": tracer._step, "cost": ledger.cost_usd, "reason": reason})
        return AttemptResult(
            task_id=task.id, author=author, outcome=outcome, candidate=ctx.candidate,
            steps=tracer._step, tokens=ledger.prompt_tokens + ledger.completion_tokens,
            cost_usd=ledger.cost_usd, tier_path="->".join(tiers_used),
            trace_id=tracer.trace_id, reason=reason, tools_used=tool_counts)

    def _may_escalate(self, ledger: Ledger) -> bool:
        return ledger.cost_usd < SETTINGS.budgets.per_task_usd_cap
