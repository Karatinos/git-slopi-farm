"""Unified agent tooling (ACI) — one shared toolbelt for every profile.

The blueprint calls the agent-computer interface the most under-valued lever, so
there is exactly ONE implementation of the sandbox hands (shell, python, file
I/O, image inspection, blackboard sharing). What used to be two near-identical
`build_tools` / `build_general_tools` functions (differing only in the terminal
tool) is now: a shared toolbelt + a profile-supplied *terminal* tool that
records a `Candidate`. No branching on competition type.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from ..memory.blackboard import Blackboard
from ..sandbox.base import Sandbox
from .contracts import Candidate

MAX_OBS = 6000


def _clip(text: str, limit: int = MAX_OBS) -> str:
    if len(text) <= limit:
        return text
    return f"{text[: limit - 400]}\n...[truncated {len(text) - limit + 700} chars]...\n{text[-300:]}"


@dataclass
class ToolContext:
    """Everything a tool may touch. Domain-agnostic: no verifier, no flag — a
    terminal tool just records a `candidate`, and the engine asks the Profile to
    judge it afterwards. `scratch` is free space for a profile's own tools."""
    sandbox: Sandbox
    blackboard: Blackboard
    task_id: str
    author: str
    candidate: Optional[Candidate] = None
    scratch: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict[str, Any]
    fn: Callable[[Dict[str, Any], ToolContext], str]
    terminal: bool = False

    def schema(self) -> Dict[str, Any]:
        return {"type": "function", "function": {
            "name": self.name, "description": self.description,
            "parameters": self.parameters}}


@dataclass
class ToolSet:
    """A task's tools. The agent loop reads `.tools`; `.schemas()` / `.by_name()`
    are conveniences. A terminal tool sets `ctx.candidate`."""
    tools: List[Tool]

    def schemas(self) -> List[Dict[str, Any]]:
        return [t.schema() for t in self.tools]

    def by_name(self) -> Dict[str, Tool]:
        return {t.name: t for t in self.tools}


# --------------------------------------------------------------------------- #
# shared executors (sandbox hands) — identical for every profile              #
# --------------------------------------------------------------------------- #
def _list_files(args, ctx: ToolContext) -> str:
    files = ctx.sandbox.list_files(args.get("path", "."))
    return "Files:\n" + "\n".join(f"- {f}" for f in files[:200]) if files else "(no files)"


def _read_file(args, ctx: ToolContext) -> str:
    path = args.get("path", "")
    return _clip(ctx.sandbox.read_file(path)) if path else "error: 'path' is required"


def _run_shell(args, ctx: ToolContext) -> str:
    cmd = args.get("command", "")
    if not cmd:
        return "error: 'command' is required"
    res = ctx.sandbox.run(cmd)
    parts = [f"[exit={res.exit_code}{' TIMEOUT' if res.timed_out else ''}]"]
    if res.stdout:
        parts.append("stdout:\n" + res.stdout)
    if res.stderr:
        parts.append("stderr:\n" + res.stderr)
    return _clip("\n".join(parts))


def _run_python(args, ctx: ToolContext) -> str:
    code = args.get("code", "")
    if not code:
        return "error: 'code' is required"
    ctx.sandbox.write_file("_snippet.py", code)
    res = ctx.sandbox.run("python3 _snippet.py")
    parts = [f"[exit={res.exit_code}{' TIMEOUT' if res.timed_out else ''}]"]
    if res.stdout:
        parts.append(res.stdout)
    if res.stderr:
        parts.append("stderr:\n" + res.stderr)
    return _clip("\n".join(parts))


def _publish_finding(args, ctx: ToolContext) -> str:
    content = args.get("content", "")
    if not content:
        return "error: 'content' is required"
    ctx.blackboard.publish(ctx.task_id, args.get("kind", "note"), content, ctx.author)
    return "published finding to the shared blackboard"


def _inspect_image(args, ctx: ToolContext) -> str:
    path = args.get("path", "")
    if not path:
        return "error: 'path' is required"
    from ..agent.image_inspect import run_inspect
    return _clip(run_inspect(ctx.sandbox, path))


def shared_toolbelt() -> List[Tool]:
    """The sandbox hands every agent gets, regardless of profile."""
    return [
        Tool("list_files", "List files available in the working directory.",
             {"type": "object", "properties": {
                 "path": {"type": "string", "description": "dir, default '.'"}}}, _list_files),
        Tool("read_file", "Read a text file (UTF-8, truncated).",
             {"type": "object", "properties": {"path": {"type": "string"}},
              "required": ["path"]}, _read_file),
        Tool("run_shell", "Run a shell command in the sandbox and get its output.",
             {"type": "object", "properties": {"command": {"type": "string"}},
              "required": ["command"]}, _run_shell),
        Tool("run_python", "Run a Python3 snippet in the sandbox.",
             {"type": "object", "properties": {"code": {"type": "string"}},
              "required": ["code"]}, _run_python),
        Tool("publish_finding",
             "Share a reusable finding (an offset, key, endpoint, decoded chunk, "
             "parsed constraint, partial result) with sibling attempts via the "
             "shared blackboard.",
             {"type": "object", "properties": {
                 "kind": {"type": "string",
                          "enum": ["artifact", "hypothesis", "credential",
                                   "partial", "decode", "note"]},
                 "content": {"type": "string"}}, "required": ["content"]},
             _publish_finding),
        Tool("inspect_image",
             "Convert an image (map, chart, schematic, screenshot) into data: OCR "
             "text with positions/colours, coloured regions, point markers.",
             {"type": "object", "properties": {"path": {"type": "string"}},
              "required": ["path"]}, _inspect_image),
    ]


def terminal_tool(*, name: str, description: str, arg: str, kind: str,
                  source: str = "arg",
                  prepare: Optional[Callable[[str, ToolContext], Optional[str]]] = None
                  ) -> Tool:
    """Build a profile's terminal tool. When the model calls it, the `arg` value
    (or, when `source="file"`, the sandbox file it names) becomes a Candidate of
    `kind`, recorded on the context. `prepare` may transform/validate the raw
    value and return None to reject it (the model keeps going).

    This one factory replaces submit_flag / submit_answer / submit_program — the
    only thing that differed between the old CTF and general toolsets.
    """
    def _fn(args: Dict[str, Any], ctx: ToolContext) -> str:
        raw = (args.get(arg) or "").strip()
        if not raw:
            return f"error: '{arg}' is required"
        if source == "file":
            content = ctx.sandbox.read_file(raw)
            if not content.strip() or content.startswith(("[no such file", "[read error")):
                return f"error: cannot read '{raw}' or it is empty"
            raw = content
        if prepare is not None:
            prepared = prepare(raw, ctx)
            if prepared is None:
                return (f"rejected: that {kind} is not acceptable yet; keep working "
                        f"and resubmit a complete {kind}.")
            raw = prepared
        ctx.candidate = Candidate(value=raw, kind=kind)
        return f"RECORDED {kind} ({len(raw)} chars)"

    return Tool(name, description,
                {"type": "object", "properties": {arg: {"type": "string"}},
                 "required": [arg]}, _fn, terminal=True)
