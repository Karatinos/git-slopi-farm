"""Model providers behind the gateway.

Two providers implement the same `.complete()` contract so the swarm never
knows (or cares) which backend answered:

* DeepSeekProvider - real OpenAI-compatible DeepSeek API (Flash / Pro).
* MockProvider     - deterministic, offline "brain" that emits OpenAI-style
                     tool calls from a tiny rule engine, so the ENTIRE farm
                     pipeline (ingest -> triage -> ensemble -> verify ->
                     metrics) runs end-to-end with no key and no spend.

The mock is intentionally small but *useful*: it reads observations, decides
which tool to call next, and submits a flag the moment it sees one. That makes
metrics on the corpus non-trivial even before a paid key is plugged in.
"""
from __future__ import annotations

import json
import os
import re
import uuid
from typing import Any, Dict, List, Optional

from .types import GatewayResponse, ToolCall, Usage


# --------------------------------------------------------------------------- #
# DeepSeek (OpenAI-compatible)                                                 #
# --------------------------------------------------------------------------- #
class DeepSeekProvider:
    name = "deepseek"

    def __init__(self, api_key: str, base_url: str, model_ids: Dict[str, str],
                 timeout: float = 120.0):
        from openai import OpenAI  # lazy import; only needed with a real key
        self._client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
        self._model_ids = model_ids
        self._base_url = base_url or ""
        self._is_openrouter = "openrouter" in self._base_url.lower()
        # off|low|medium|high — controls the OpenRouter `reasoning` param so the
        # same Flash slug can run cheap (low) or hard (high) without a model swap.
        self._reasoning_effort = os.environ.get("DEEPSEEK_REASONING_EFFORT", "low").lower()
        # OpenRouter adds extra HTTP headers for attribution/routing.
        self._extra_headers = ({"HTTP-Referer": "https://localhost/slopi-farm",
                                "X-Title": "slopi-farm"} if self._is_openrouter else None)

    def complete(self, *, messages: List[Dict[str, Any]], tier: str,
                 tools: Optional[List[Dict[str, Any]]] = None,
                 temperature: float = 0.2, max_tokens: int = 2048) -> GatewayResponse:
        model_id = self._model_ids[tier]
        kwargs: Dict[str, Any] = dict(
            model=model_id, messages=messages,
            temperature=temperature, max_tokens=max_tokens,
        )
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        extra_body: Dict[str, Any] = {}
        if self._is_openrouter:
            # Ask OpenRouter to return the real billed cost in usage so the
            # governor is EXACT (no local price-table drift / undercount hack).
            extra_body["usage"] = {"include": True}
            if self._reasoning_effort in ("low", "medium", "high"):
                extra_body["reasoning"] = {"effort": self._reasoning_effort}
            elif self._reasoning_effort in ("off", "none", "false"):
                extra_body["reasoning"] = {"enabled": False}
        if extra_body:
            kwargs["extra_body"] = extra_body
        if self._extra_headers:
            kwargs["extra_headers"] = self._extra_headers
        resp = self._client.chat.completions.create(**kwargs)
        choice = resp.choices[0]
        msg = choice.message
        tool_calls: List[ToolCall] = []
        for tc in (msg.tool_calls or []):
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {"_raw": tc.function.arguments}
            tool_calls.append(ToolCall(id=tc.id, name=tc.function.name, arguments=args))
        text = msg.content or ""
        if "DSML" in text:
            # V4-Pro sometimes leaks its internal tool-call markup into content
            # instead of structured tool_calls (seen even when no tools were
            # offered). Recover the calls when tools exist; never pass the
            # markup on as text (it once became a "candidate answer").
            text, leaked = _parse_dsml(text)
            if tools and not tool_calls:
                tool_calls = leaked

        u = resp.usage

        def _extra(obj, key, default=None):
            v = getattr(obj, key, None)
            if v is None and hasattr(obj, "model_extra") and obj.model_extra:
                v = obj.model_extra.get(key)
            return default if v is None else v

        prompt = (u.prompt_tokens if u else 0) or 0
        # Cache-hit tokens: DeepSeek-native field OR OpenAI/OpenRouter
        # prompt_tokens_details.cached_tokens.
        hit = _extra(u, "prompt_cache_hit_tokens") if u else None
        if hit is None and u is not None:
            det = getattr(u, "prompt_tokens_details", None)
            if det is not None:
                hit = _extra(det, "cached_tokens")
        hit = int(hit or 0)
        miss = max(0, prompt - hit)
        usage = Usage(
            prompt_tokens=prompt,
            completion_tokens=(u.completion_tokens if u else 0) or 0,
            cache_hit_tokens=hit,
            cache_miss_tokens=miss,
        )
        # Exact billed cost from OpenRouter (usage.cost), when present.
        reported_cost = _extra(u, "cost") if u else None
        gr = GatewayResponse(
            text=text,
            tool_calls=tool_calls,
            model_tier=tier,
            provider=self.name,
            usage=usage,
            finish_reason=choice.finish_reason or "stop",
            raw=resp,
        )
        if reported_cost is not None:
            try:
                gr.cost_usd = float(reported_cost)
                gr.cost_from_provider = True
            except (TypeError, ValueError):
                pass
        return gr


_DSML_BLOCK = re.compile(r"<[｜|]+DSML[｜|]+tool_calls>.*?(?:</[｜|]+DSML[｜|]+tool_calls>|$)", re.DOTALL)
_DSML_INVOKE = re.compile(r"<[｜|]+DSML[｜|]+invoke name=\"([^\"]+)\">(.*?)</[｜|]+DSML[｜|]+invoke>", re.DOTALL)
_DSML_PARAM = re.compile(r"<[｜|]+DSML[｜|]+parameter name=\"([^\"]+)\"(?: string=\"(true|false)\")?>"
                         r"(.*?)</[｜|]+DSML[｜|]+parameter>", re.DOTALL)


def _parse_dsml(text: str):
    """Split leaked DSML tool-call markup out of assistant text.
    Returns (text_without_markup, [ToolCall])."""
    calls: List[ToolCall] = []
    for name, body in _DSML_INVOKE.findall(text):
        args: Dict[str, Any] = {}
        for pname, is_str, val in _DSML_PARAM.findall(body):
            if is_str == "true":
                args[pname] = val
            else:
                try:
                    args[pname] = json.loads(val)
                except json.JSONDecodeError:
                    args[pname] = val
        calls.append(ToolCall(id=f"dsml_{uuid.uuid4().hex[:12]}", name=name, arguments=args))
    clean = _DSML_BLOCK.sub("", text)
    clean = re.sub(r"</?[｜|]+DSML[｜|]+[^>]*>", "", clean).strip()
    return clean, calls


# --------------------------------------------------------------------------- #
# Mock provider - deterministic offline brain                                 #
# --------------------------------------------------------------------------- #
_FLAG_RE = re.compile(r"[A-Za-z0-9_]{2,32}\{[^}\n]{1,200}\}")


class MockProvider:
    """A rule-based stand-in for an LLM.

    Estimates realistic token usage so cost accounting and the governor behave
    exactly as they would with a real model. Emits OpenAI-style tool calls.
    """
    name = "mock"

    def __init__(self, model_ids: Dict[str, str]):
        self._model_ids = model_ids

    # rough token estimate: ~4 chars/token
    @staticmethod
    def _est_tokens(text: str) -> int:
        return max(1, len(text) // 4)

    def complete(self, *, messages: List[Dict[str, Any]], tier: str,
                 tools: Optional[List[Dict[str, Any]]] = None,
                 temperature: float = 0.2, max_tokens: int = 2048) -> GatewayResponse:
        prompt_text = "\n".join(
            (m.get("content") or "") if isinstance(m.get("content"), str) else
            json.dumps(m.get("content")) for m in messages
        )
        prompt_tokens = self._est_tokens(prompt_text)
        # Simulate prefix-cache: a big stable system prefix -> mostly cache hits
        # after the first call. Heuristic: 80% hit for prompts over ~1k tokens.
        if prompt_tokens > 1000:
            hit = int(prompt_tokens * 0.8)
        else:
            hit = 0
        miss = prompt_tokens - hit

        text, tool_calls = self._decide(messages, tools)
        completion_tokens = self._est_tokens(text) + sum(
            self._est_tokens(json.dumps(tc.arguments)) for tc in tool_calls
        )
        usage = Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cache_hit_tokens=hit,
            cache_miss_tokens=miss,
        )
        return GatewayResponse(
            text=text, tool_calls=tool_calls, model_tier=tier,
            provider=self.name, usage=usage,
            finish_reason=("tool_calls" if tool_calls else "stop"),
        )

    # --- the tiny "reasoning" engine ------------------------------------- #
    def _decide(self, messages, tools):
        tool_names = {t["function"]["name"] for t in (tools or [])}
        last = messages[-1] if messages else {}
        last_content = last.get("content") or ""
        if not isinstance(last_content, str):
            last_content = json.dumps(last_content)

        # Gather everything the agent has observed so far.
        seen = "\n".join(
            (m.get("content") or "") for m in messages
            if isinstance(m.get("content"), str)
        )

        # 1) If any flag is visible in observations -> submit the first one we
        #    have NOT tried yet (there may be a placeholder before the real one).
        if "submit_flag" in tool_names:
            candidates = list(dict.fromkeys(_FLAG_RE.findall(seen)))
            tried = {
                json.loads(tc["function"]["arguments"]).get("flag", "").strip()
                for msg in messages if msg.get("role") == "assistant"
                for tc in (msg.get("tool_calls") or [])
                if tc["function"]["name"] == "submit_flag"
            }
            for cand in candidates:
                if cand.strip() not in tried:
                    return "", [self._call("submit_flag", {"flag": cand})]

        def already_ran(substr: str) -> bool:
            return any(substr in json.dumps(msg.get("tool_calls") or [])
                       for msg in messages if msg.get("role") == "assistant")

        # 2) Broad flag scan across all files/text at once (robust & realistic).
        if "run_shell" in tool_names and not already_ran("grep -rEoiha"):
            return "", [self._call("run_shell", {"command":
                "grep -rEoiha 'flag\\{[^}]{1,120}\\}' . 2>/dev/null | sort -u | head -40"})]

        # 3) List files if not yet listed.
        if "list_files" in tool_names and not already_ran('"list_files"') \
                and '"name": "list_files"' not in json.dumps(messages):
            return "", [self._call("list_files", {"path": "."})]

        # 4) Read an unread text file (strip listing bullets/spaces from names).
        if "read_file" in tool_names:
            cands = re.findall(r"[\w./ ]+\.(?:txt|md|py|json|log|csv|pem|c|h)", seen)
            read_already = {
                json.loads(tc["function"]["arguments"]).get("path", "").strip()
                for msg in messages if msg.get("role") == "assistant"
                for tc in (msg.get("tool_calls") or [])
                if tc["function"]["name"] == "read_file"}
            for c in cands:
                path = c.strip(" -\t\r\n")
                if path and path not in read_already:
                    return "", [self._call("read_file", {"path": path})]

        # 5) strings scan over binaries/images.
        if "run_shell" in tool_names and not already_ran("strings") \
                and re.search(r"\.(bin|elf|exe|so|png|jpg|jpeg|pcap)", seen):
            return "", [self._call("run_shell", {"command":
                "for f in *; do strings -n 6 \"$f\" 2>/dev/null | grep -iE 'flag\\{' ; done | head"})]

        # 6) Give up cleanly (lets the orchestrator stop the trajectory).
        return ("No further progress: exhausted deterministic heuristics without "
                "recovering a flag."), []

    @staticmethod
    def _call(name: str, args: Dict[str, Any]) -> ToolCall:
        return ToolCall(id="mock-" + uuid.uuid4().hex[:8], name=name, arguments=args)


# --------------------------------------------------------------------------- #
# ScriptedSolver - no-LLM tooling baseline (pipeline validator)               #
# --------------------------------------------------------------------------- #
class ScriptedSolverProvider:
    """Drives the ReAct loop with a fixed, model-free policy: list files, run the
    generic autosolver over them in the sandbox, then submit any flag it printed.

    It performs REAL work through the real sandbox tools and the real verdict
    path, so an end-to-end run proves tools+sandbox+scoring without spending a
    cent - and measures the tooling-only solve baseline. Not for live use.
    """
    name = "scripted"

    def __init__(self, model_ids: Dict[str, str]):
        self._model_ids = model_ids
        from ..config import FARM_ROOT
        try:
            self._autosolve = (FARM_ROOT / "research" / "autosolve.py").read_text(encoding="utf-8")
        except Exception:  # noqa: BLE001
            self._autosolve = "print('NO_FLAG_FOUND')"

    @staticmethod
    def _est(text: str) -> int:
        return max(1, len(text) // 4)

    def complete(self, *, messages: List[Dict[str, Any]], tier: str,
                 tools: Optional[List[Dict[str, Any]]] = None,
                 temperature: float = 0.2, max_tokens: int = 2048) -> GatewayResponse:
        names = {t["function"]["name"] for t in (tools or [])}
        blob = json.dumps(messages, ensure_ascii=False)

        def resp(text, calls):
            u = Usage(prompt_tokens=self._est(blob),
                      completion_tokens=self._est(text) + sum(self._est(json.dumps(c.arguments)) for c in calls),
                      cache_hit_tokens=0, cache_miss_tokens=self._est(blob))
            return GatewayResponse(text=text, tool_calls=calls, model_tier=tier,
                                   provider=self.name, usage=u,
                                   finish_reason=("tool_calls" if calls else "stop"))

        def tc(name, args):
            return ToolCall(id="scr-" + uuid.uuid4().hex[:8], name=name, arguments=args)

        m = re.search(r"FLAG=([A-Za-z0-9_]{2,16}\{[A-Za-z0-9_]{1,80}\})", blob)
        already = '"submit_flag"' in blob and "RECORDED" in blob
        if "submit_flag" in names and m and not already:
            return resp("", [tc("submit_flag", {"flag": m.group(1)})])
        if "run_python" in names and "FLAG=" not in blob and "NO_FLAG_FOUND" not in blob:
            return resp("", [tc("run_python", {"code": self._autosolve})])
        if "list_files" in names and '"list_files"' not in blob:
            return resp("", [tc("list_files", {"path": "."})])
        return resp("No further progress: tooling baseline exhausted.", [])
