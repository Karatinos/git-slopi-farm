"""Minimal MCP (Model Context Protocol) stdio client — augment the agent's
toolbelt with tools exposed by an external MCP server.

The blueprint's thesis is that tool quality (ACI) is the biggest lever, so the
farm should be able to borrow specialised tools (a CTF toolbox, a solver, a
retrieval service) from any MCP server instead of reimplementing them. This is
a small, dependency-free client over the MCP **stdio** transport: newline-
delimited JSON-RPC 2.0 on a subprocess' stdin/stdout.

Design notes / scars carried over from this codebase:
- A background reader thread + queue, never a blocking `readline`, so a wedged
  server can't freeze a run (the "hanging connection" lesson) — every read has
  a hard deadline.
- `tools/call` faults return an ``error: ...`` string, not an exception, so they
  compose with the agent loop's tool-fault handling (a bad call is recoverable,
  never aborts the attempt).

Wiring: ``build_mcp_tools(command)`` returns farm ``Tool`` objects (ready for a
profile to add to its ``ToolSet``) plus the live client; the caller owns the
client's lifecycle (use it as a context manager, or call ``close()``). Nothing
is enabled by default — a profile opts in by configuring a server command.
"""
from __future__ import annotations

import json
import queue
import subprocess
import threading
import time
from typing import Any, Dict, List, Optional, Tuple

from ..core.toolset import Tool, ToolContext

PROTOCOL_VERSION = "2024-11-05"


class MCPError(RuntimeError):
    """A protocol-level failure talking to an MCP server."""


class MCPStdioClient:
    """Speaks JSON-RPC 2.0 to an MCP server over stdio (newline-delimited).

    Usage:
        with MCPStdioClient(["my-mcp-server", "--flag"]) as c:
            for spec in c.list_tools():
                ...
            text = c.call_tool("name", {"arg": 1})
    """

    def __init__(self, command: List[str], env: Optional[Dict[str, str]] = None,
                 init_timeout: float = 10.0, call_timeout: float = 30.0):
        if not command:
            raise ValueError("command must be a non-empty argv list")
        self.command = command
        self.env = env
        self.init_timeout = init_timeout
        self.call_timeout = call_timeout
        self._proc: Optional[subprocess.Popen] = None
        self._q: "queue.Queue[Optional[str]]" = queue.Queue()
        self._reader: Optional[threading.Thread] = None
        self._next_id = 0
        self._started = False

    # -- lifecycle --------------------------------------------------------- #
    def start(self) -> "MCPStdioClient":
        if self._started:
            return self
        self._proc = subprocess.Popen(
            self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, env=self.env, text=True, bufsize=1)
        self._reader = threading.Thread(target=self._pump, daemon=True)
        self._reader.start()
        self._handshake()
        self._started = True
        return self

    def close(self) -> None:
        p = self._proc
        if p is None:
            return
        try:
            if p.stdin and not p.stdin.closed:
                p.stdin.close()
        except Exception:  # noqa: BLE001
            pass
        try:
            p.terminate()
            p.wait(timeout=3)
        except Exception:  # noqa: BLE001
            try:
                p.kill()
            except Exception:  # noqa: BLE001
                pass
        self._proc = None

    def __enter__(self) -> "MCPStdioClient":
        return self.start()

    def __exit__(self, *exc) -> None:
        self.close()

    # -- MCP methods ------------------------------------------------------- #
    def list_tools(self) -> List[Dict[str, Any]]:
        res = self._request("tools/list", {}, self.call_timeout)
        return list(res.get("tools", []))

    def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
        """Call a tool; return its text content. A tool-reported error comes
        back as an ``error: ...`` string rather than raising, so it composes
        with the agent loop's recoverable-observation handling."""
        try:
            res = self._request("tools/call",
                                 {"name": name, "arguments": arguments or {}},
                                 self.call_timeout)
        except Exception as e:  # noqa: BLE001
            return f"error: MCP call '{name}' failed: {e}"
        text = _content_text(res.get("content", []))
        if res.get("isError"):
            return f"error: {text or 'tool reported failure'}"
        return text

    # -- internals --------------------------------------------------------- #
    def _pump(self) -> None:
        """Reader thread: push each stdout line onto the queue; None on EOF."""
        assert self._proc is not None and self._proc.stdout is not None
        try:
            for line in self._proc.stdout:
                self._q.put(line)
        except Exception:  # noqa: BLE001
            pass
        finally:
            self._q.put(None)

    def _send(self, msg: Dict[str, Any]) -> None:
        p = self._proc
        if p is None or p.stdin is None:
            raise MCPError("server not started")
        p.stdin.write(json.dumps(msg) + "\n")
        p.stdin.flush()

    def _request(self, method: str, params: Dict[str, Any], timeout: float) -> Dict[str, Any]:
        self._next_id += 1
        rid = self._next_id
        self._send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        deadline = time.time() + timeout
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise MCPError(f"timeout waiting for '{method}' response")
            try:
                line = self._q.get(timeout=remaining)
            except queue.Empty:
                raise MCPError(f"timeout waiting for '{method}' response")
            if line is None:
                raise MCPError("server closed the connection")
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue  # ignore non-JSON noise on stdout
            if msg.get("id") != rid:
                continue  # a notification or an out-of-band message
            if "error" in msg:
                err = msg["error"]
                raise MCPError(f"{err.get('code')}: {err.get('message')}")
            return msg.get("result", {}) or {}

    def _handshake(self) -> None:
        self._request("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "slopi-farm", "version": "1"},
        }, self.init_timeout)
        # notifications/initialized has no id and expects no reply
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})


def _content_text(content: List[Dict[str, Any]]) -> str:
    """Join the text parts of an MCP content array (ignore non-text parts)."""
    parts = []
    for item in content or []:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(str(item.get("text", "")))
    return "\n".join(parts)


def build_mcp_tools(command: List[str], prefix: str = "mcp_",
                    **client_kwargs) -> Tuple[List[Tool], MCPStdioClient]:
    """Connect to an MCP server and wrap each of its tools as a farm ``Tool``.

    Returns (tools, client). The caller owns ``client`` and must ``close()`` it
    when the task is done (or use it as a context manager). Each wrapped tool's
    name is ``<prefix><server tool name>`` to avoid colliding with the builtin
    toolbelt; its executor forwards the arguments to ``tools/call`` and returns
    the text content (a tool error becomes a recoverable ``error: ...`` string).
    """
    client = MCPStdioClient(command, **client_kwargs).start()
    tools: List[Tool] = []
    for spec in client.list_tools():
        name = spec.get("name")
        if not name:
            continue
        schema = spec.get("inputSchema") or {"type": "object", "properties": {}}
        desc = spec.get("description") or f"MCP tool '{name}'"

        def _make(tool_name: str):
            def _fn(args: Dict[str, Any], ctx: ToolContext) -> str:
                return client.call_tool(tool_name, args or {})
            return _fn

        tools.append(Tool(f"{prefix}{name}", desc[:300], schema, _make(name)))
    return tools, client
