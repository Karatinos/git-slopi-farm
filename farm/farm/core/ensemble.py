"""Diverse ensemble with early cancellation — one implementation for all.

N parallel attempts with different temperatures (and a Pro-hot slice for hard
categories), sharing one blackboard. Recon runs ONCE per task and is handed to
every member (no repeated OCR). Judging is delegated to the Profile:

  * `profile.verdict(task, cand)` — cheap offline oracle (gold / checker);
  * `profile.submit(task, cand)`  — authoritative external verdict, called at
    most once, on the selected candidate.

Stopping policy is a per-profile knob, not a type check: `first_to_candidate`
(CTF: the first produced flag cancels siblings) vs collect-and-select (answer
competitions: run the wave, then majority-vote the candidates).
"""
from __future__ import annotations

import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as _FTimeout
from typing import List, Optional

from ..config import SETTINGS, SwarmConfig
from ..sandbox.base import SandboxProvider
from .agent import ReActAgent
from .contracts import AttemptResult, Candidate, Grade, Outcome, Task, Verdict
from .net import reachable as _reachable
from .profile import Profile


class Ensemble:
    def __init__(self, *, agent: ReActAgent, sandbox_provider: SandboxProvider,
                 swarm: SwarmConfig = None, enable_recon: bool = False,
                 check_reachability: bool = True):
        self.agent = agent
        self.sandboxes = sandbox_provider
        self.swarm = swarm or SETTINGS.swarm
        self.enable_recon = enable_recon
        self.check_reachability = check_reachability

    def solve(self, task: Task, profile: Profile, fewshot: str = "") -> Outcome:
        # Fast-fail a PURE-instance task whose host is down: no offline material
        # to work on, so skip it in seconds instead of burning the per-task
        # budget on hanging connects. A task that also ships files still runs.
        if (self.check_reachability and task.has_service and not task.files
                and not _reachable(task.endpoint)):
            return Outcome(
                id=task.id, name=task.name, category=task.category, solved=False,
                grade=Grade.NONE, candidate=None, correct=False, cost_usd=0.0,
                tokens=0, wall_seconds=0.0, time_to_solve=None, escalated=False,
                n_attempts=0, error=f"service unreachable: {task.endpoint}")
        toolset = profile.toolset(task)
        system_prompt = profile.system_prompt(task)
        temps = list(self.swarm.temperatures)[: self.swarm.ensemble_size]
        while len(temps) < self.swarm.ensemble_size:
            temps.append(0.5)

        recon = self._recon_once(task)
        # adaptive effort: on a low-signal task, cap the step budget so an
        # opaque task with no lead concludes fast instead of burning tokens.
        step_override = (self.swarm.low_signal_steps
                         if self.swarm.adaptive_effort
                         and task.extra.get("difficulty") == "low" else None)
        cancel = threading.Event()
        started = time.time()
        results: List[AttemptResult] = []
        early: dict = {}                    # author -> Verdict for a CORRECT offline hit
        first_to_candidate = getattr(profile, "first_to_candidate", True)

        def one(idx: int, temp: float) -> AttemptResult:
            author = f"{task.id}#a{idx}"
            hot = (getattr(self.agent.cascade, "enabled", True)
                   and task.category in self.agent.cascade.hard_categories
                   and idx == self.swarm.ensemble_size - 1)
            sb = self.sandboxes.create(author, seed_files=task.files)
            try:
                return self.agent.run(
                    task=task, toolset=toolset, system_prompt=system_prompt,
                    author=author, temperature=temp,
                    start_tier="pro" if hot else "flash", sandbox=sb,
                    recon=recon, fewshot=fewshot, cancel_event=cancel,
                    max_steps_override=step_override)
            finally:
                sb.destroy()

        workers = min(self.swarm.max_concurrent_sandboxes, len(temps))
        # HARD wall-clock ceiling per task: a hung attempt (slow instance, model
        # stall) can never exceed this, regardless of per-step budgets.
        hard_deadline = max(300.0, getattr(getattr(self.agent, 'budgets', None), 'max_seconds', 180.0) * 2 + 60)
        ex = ThreadPoolExecutor(max_workers=workers)
        futures = [ex.submit(one, i, t) for i, t in enumerate(temps)]
        try:
            for fut in as_completed(futures, timeout=hard_deadline):
                try:
                    res = fut.result()
                except Exception as e:  # noqa: BLE001
                    import traceback
                    res = AttemptResult(task_id=task.id, author=f"{task.id}#err",
                                        outcome="error",
                                        reason=f"{e} :: {traceback.format_exc()[-400:]}")
                results.append(res)
                if res.candidate is not None:
                    res.candidate = profile.normalize(res.candidate, task)
                    v = profile.verdict(task, res.candidate)
                    if v.grade == Grade.CORRECT:
                        res.accepted = True
                        early[res.author] = v
                        cancel.set()                    # verified: stop siblings
                    elif first_to_candidate and getattr(self.swarm, "consensus", 1) <= 1:
                        cancel.set()                    # first-to-flag heuristic
        except _FTimeout:
            cancel.set()
            for i, fut in enumerate(futures):
                if not fut.done():
                    results.append(AttemptResult(
                        task_id=task.id, author=f"{task.id}#to{i}", outcome="killed",
                        reason=f"task wall-clock deadline {hard_deadline:.0f}s exceeded"))
        finally:
            ex.shutdown(wait=False)

        wall = time.time() - started
        return self._finish(task, profile, results, early, wall)

    # ----- judging & selection ------------------------------------------- #
    def _finish(self, task: Task, profile: Profile, results: List[AttemptResult],
                early: dict, wall: float) -> Outcome:
        cost = sum(r.cost_usd for r in results)
        tokens = sum(r.tokens for r in results)
        escalated = any("pro" in r.tier_path for r in results)
        tiers = sorted({r.tier_path for r in results})
        produced = [r for r in results if r.candidate and r.candidate.value.strip()]

        chosen: Optional[Candidate] = None
        verdict: Optional[Verdict] = None
        author = None
        consensus_note = ""

        # 1) a verified-correct attempt wins outright
        for r in results:
            if r.author in early:
                chosen, verdict, author = r.candidate, early[r.author], r.author
                break

        # 2) otherwise select among produced candidates (majority by canonical
        #    value), then ask the profile for the authoritative verdict.
        if chosen is None and produced:
            counts = Counter(c.candidate.value for c in produced)
            best, bestn = counts.most_common(1)[0]
            r = next(c for c in produced if c.candidate.value == best)
            chosen, author = r.candidate, r.author
            need = max(1, getattr(self.swarm, "consensus", 1))
            if bestn >= need:
                verdict = profile.submit(task, chosen) or profile.verdict(task, chosen)
            else:
                # below consensus: grade offline but do NOT spend a live
                # submission on a lone, uncorroborated guess.
                verdict = profile.verdict(task, chosen)
                consensus_note = f"low-confidence {bestn}/{need}"
            r.accepted = verdict.grade == Grade.CORRECT

        grade = verdict.grade if verdict else Grade.NONE
        correct = grade == Grade.CORRECT
        solved = chosen is not None
        return Outcome(
            id=task.id, name=task.name, category=task.category, solved=solved,
            grade=grade, candidate=chosen, correct=correct, cost_usd=cost,
            tokens=tokens, wall_seconds=wall,
            time_to_solve=wall if solved else None, escalated=escalated,
            n_attempts=len(results), tiers=tiers,
            error=((verdict.detail if verdict else "") or
                   next((r.reason for r in results if r.outcome == "error"), ""))
                  + (f" [{consensus_note}]" if consensus_note else ""))

    def _recon_once(self, task: Task) -> str:
        if not self.enable_recon:
            return ""
        parts = []
        if task.files:
            sb = self.sandboxes.create(f"{task.id}#recon", seed_files=task.files)
            try:
                from ..agent.recon import run_recon
                d = run_recon(sb)
                if d:
                    parts.append(d)
            except Exception:  # noqa: BLE001
                pass
            finally:
                sb.destroy()
        # instance recon: first-contact signal for a LIVE service (web/pwn),
        # the network analogue of file recon. Bounded; only for attempted tasks.
        ep = (getattr(task, "endpoint", "") or "").strip()
        if ep:
            try:
                from .net import probe_instance, reachable
                if reachable(ep, timeout=3.0):
                    pr = probe_instance(ep, timeout=3.0)
                    if pr:
                        parts.append("## Instance recon (live first-contact)\n" + pr)
                else:
                    parts.append(
                        f"## Instance recon\n  note: {ep} did not accept a TCP "
                        "connection just now — retry on connect, it may be slow to start.")
            except Exception:  # noqa: BLE001
                pass
        return "\n\n".join(parts)
