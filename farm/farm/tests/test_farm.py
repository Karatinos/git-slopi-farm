"""Unit suite for the unified farm core (stdlib unittest, zero API cost).

Covers the pieces the rebuild depends on: flag canonicalization, both profiles'
verdict/normalize/ingest, the scheduler's admission + priority + triage override,
triage scoring, the reachability gate, ensemble candidate selection, and the KPI
report. Run: `python -m unittest farm.tests.test_farm -v`.
"""
from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import List, Optional

import farm.profiles  # noqa: F401  (register profiles)
from farm.config import SETTINGS
from farm.core.contracts import AttemptResult, Candidate, Grade, Outcome, Task, Verdict
from farm.core.ensemble import Ensemble
from farm.core.net import parse_endpoint, probe_instance, reachable
from farm.core.profile import BaseProfile, available, build
from farm.core.report import kpis, render_markdown
from farm.core.scheduler import Scheduler
from farm.core.toolset import ToolContext, ToolSet
from farm.core.triage import Triage
from farm.pipeline.verify import canonicalize_flag


# --------------------------------------------------------------------------- #
# stubs                                                                       #
# --------------------------------------------------------------------------- #
class _Cascade:
    hard_categories = {"pwn", "reverse"}


class _StubAgent:
    """Returns a canned candidate per author; records whether it was called."""
    def __init__(self, by_author=None, raise_if_called=False):
        self.cascade = _Cascade()
        self.by_author = by_author or {}
        self.raise_if_called = raise_if_called
        self.calls = 0

    def run(self, *, task, author, **kw):
        self.calls += 1
        if self.raise_if_called:
            raise AssertionError("agent must not run")
        val = self.by_author.get(author)
        cand = Candidate(val, "flag") if val else None
        return AttemptResult(task_id=task.id, author=author,
                             outcome="solved" if cand else "failed", candidate=cand)


class _SB:
    def list_files(self, p="."):
        return []
    def write_file(self, *a, **k):
        pass
    def read_file(self, *a, **k):
        return ""
    def run(self, *a, **k):
        return None
    def destroy(self):
        pass


class _StubProvider:
    def create(self, name, seed_files=None):
        return _SB()


class _StubProfile(BaseProfile):
    """Minimal profile: optionally mark one value CORRECT; else UNGRADED."""
    name = "stub"
    first_to_candidate = False
    def __init__(self, correct_value: Optional[str] = None):
        self.correct_value = correct_value
    def toolset(self, task):
        return ToolSet([])
    def system_prompt(self, task):
        return "sys"
    def verdict(self, task, candidate):
        if self.correct_value and candidate.value == self.correct_value:
            return Verdict(Grade.CORRECT, "match", candidate.value)
        return Verdict(Grade.UNGRADED, "no oracle", candidate.value)


def _ensemble(agent, size=3):
    sw = SETTINGS.swarm.__class__(ensemble_size=size,
                                  temperatures=tuple(0.1 * i for i in range(size)),
                                  max_concurrent_sandboxes=size)
    return Ensemble(agent=agent, sandbox_provider=_StubProvider(), swarm=sw)


# --------------------------------------------------------------------------- #
# flag canonicalization (point-1 guarantee)                                   #
# --------------------------------------------------------------------------- #
class TestCanonicalize(unittest.TestCase):
    def test_trims_extra_braces(self):
        self.assertEqual(canonicalize_flag("swarm{a_b}}}"), "swarm{a_b}")
    def test_terminates_cutoff(self):
        self.assertEqual(canonicalize_flag("swarm{a_b_c"), "swarm{a_b_c}")
    def test_strips_prose_and_quotes(self):
        self.assertEqual(canonicalize_flag("the flag is: `swarm{x}` done"), "swarm{x}")
    def test_passthrough_non_flag(self):
        self.assertEqual(canonicalize_flag("not a flag"), "not a flag")


# --------------------------------------------------------------------------- #
# CTF profile                                                                 #
# --------------------------------------------------------------------------- #
class TestCTFProfile(unittest.TestCase):
    def setUp(self):
        self.p = build("ctf", flag_format="swarm{...}")
    def test_verdict_exact_and_body(self):
        t = Task("x", "x", "crypto", "", gold="swarm{abc}")
        self.assertEqual(self.p.verdict(t, Candidate("swarm{abc}")).grade, Grade.CORRECT)
        self.assertEqual(self.p.verdict(t, Candidate("flag{abc}")).grade, Grade.CORRECT)
        self.assertEqual(self.p.verdict(t, Candidate("swarm{no}")).grade, Grade.INCORRECT)
    def test_verdict_ungraded_without_gold(self):
        t = Task("y", "y", "crypto", "")
        self.assertEqual(self.p.verdict(t, Candidate("swarm{z}")).grade, Grade.UNGRADED)
    def test_normalize_canonicalizes(self):
        t = Task("x", "x", "crypto", "")
        self.assertEqual(self.p.normalize(Candidate("swarm{a}}}"), t).value, "swarm{a}")
    def test_ingest_injects_service_block_and_endpoint(self):
        tasks = self.p.ingest([{"id": "c/1", "name": "n", "category": "web",
                                "statement": "do it", "endpoint": "nc h 1", "files": []}])
        self.assertTrue(tasks[0].has_service)
        self.assertIn("Live service", tasks[0].statement)
        self.assertEqual(tasks[0].answer_format, "swarm{...}")
    def test_terminal_dedup_and_reject(self):
        t = Task("x", "x", "crypto", "")
        sub = self.p.toolset(t).by_name()["submit_flag"]
        ctx = ToolContext(sandbox=_SB(), blackboard=None, task_id="x", author="a")
        self.assertIn("RECORDED", sub.fn({"flag": "swarm{a}}}"}, ctx))
        self.assertEqual(ctx.candidate.value, "swarm{a}")
        ctx.candidate = None
        self.assertIn("rejected", sub.fn({"flag": "swarm{a}"}, ctx))  # dedup
    def test_submit_wrapper_retry(self):
        seen = []
        def submitter(cid, flag):
            seen.append(flag)
            return "correct" if flag == "swarm{body}" else "incorrect"
        p = build("ctf", flag_format="swarm{...}", submitter=submitter)
        t = Task("c/1", "n", "web", "", extra={"cid": 1})
        v = p.submit(t, Candidate("flag{body}"))  # wrong wrapper -> retried as swarm{}
        self.assertEqual(v.grade, Grade.CORRECT)
        self.assertIn("swarm{body}", seen)


# --------------------------------------------------------------------------- #
# generic profile                                                             #
# --------------------------------------------------------------------------- #
class TestGenericProfile(unittest.TestCase):
    def setUp(self):
        self.p = build("generic")
    def test_normalize_strips_fences_and_labels(self):
        t = Task("g", "g", "data", "")
        self.assertEqual(self.p.normalize(Candidate("Answer: 13,37"), t).value, "13,37")
        self.assertEqual(self.p.normalize(Candidate("```\n42\n```"), t).value, "42")
    def test_verdict_separator_insensitive(self):
        t = Task("g", "g", "data", "", gold="13,37")
        self.assertEqual(self.p.verdict(t, Candidate("13.37")).grade, Grade.CORRECT)
        self.assertEqual(self.p.verdict(t, Candidate("99")).grade, Grade.INCORRECT)
    def test_toolset_has_both_terminals(self):
        names = set(self.p.toolset(Task("g", "g", "data", "")).by_name())
        self.assertIn("submit_answer", names)
        self.assertIn("submit_program", names)


# --------------------------------------------------------------------------- #
# scheduler & triage                                                          #
# --------------------------------------------------------------------------- #
class TestScheduler(unittest.TestCase):
    def test_admission_and_offline(self):
        T = [Task("a", "File", "web", "s", files=[(Path("/tmp/a"), "a")]),
             Task("b", "Inst", "pwn", "s", endpoint="http://h:1"),
             Task("c", "Empty", "misc", "s")]
        sch = Scheduler()
        names = {t.name for t in sch.plan(T)}
        self.assertEqual(names, {"File", "Inst"})            # Empty dropped
        off = {t.name for t in sch.plan(T, offline_only=True)}
        self.assertEqual(off, {"File"})                       # Inst filtered
    def test_triage_override_reorders(self):
        a = Task("a", "A", "pwn", "s", files=[(Path("/t"), "a")])   # low prior
        b = Task("b", "B", "web", "s", files=[(Path("/t"), "b")])   # high prior
        sch = Scheduler(group_by_category=False)
        self.assertEqual([t.name for t in sch.plan([a, b])], ["B", "A"])
        a.extra["p_solve"] = 0.99                              # triage boosts A
        self.assertEqual([t.name for t in sch.plan([a, b])], ["A", "B"])


class TestTriage(unittest.TestCase):
    def test_difficulty(self):
        tr = Triage()
        self.assertEqual(tr.assess(Task("p", "p", "pwn", "x")).difficulty, "hard")
        self.assertEqual(tr.assess(Task("m", "m", "misc", "x")).difficulty, "low")
    def test_bank_boost(self):
        class _Bank:
            def retrieve(self, q, category=None, k=1):
                return [{"score": 0.9}]
        base = Triage().assess(Task("c", "c", "crypto", "x")).p_solve
        boosted = Triage(bank=_Bank()).assess(Task("c", "c", "crypto", "x")).p_solve
        self.assertGreater(boosted, base)
    def test_negative_memory_penalty(self):
        class _BB:
            def dead_ends(self, tid):
                return [{"approach": "x"}]
        base = Triage().assess(Task("c", "c", "crypto", "x")).p_solve
        pen = Triage(blackboard=_BB()).assess(Task("c", "c", "crypto", "x")).p_solve
        self.assertLess(pen, base)


# --------------------------------------------------------------------------- #
# net reachability                                                            #
# --------------------------------------------------------------------------- #
class TestNet(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse_endpoint("nc 10.0.0.1 1337"), ("10.0.0.1", 1337))
        self.assertEqual(parse_endpoint("http://h.test:8080/x"), ("h.test", 8080))
        self.assertEqual(parse_endpoint("1.2.3.4:9999"), ("1.2.3.4", 9999))
        self.assertIsNone(parse_endpoint(""))
        # scheme default port
        self.assertEqual(parse_endpoint("https://ctf.example.com/x"),
                         ("ctf.example.com", 443))
        # single-label host with an explicit colon-port still parses
        self.assertEqual(parse_endpoint("chal:1337"), ("chal", 1337))
        # robustness: prose with no real port, a time, and an out-of-range port
        # must not produce a bogus (host, port) from the fallback path
        self.assertIsNone(parse_endpoint("connect at 192.168.1.108 to start"))
        self.assertIsNone(parse_endpoint("meeting at 12:34 today"))
        self.assertIsNone(parse_endpoint("1.2.3.4:99999"))
    def test_reachable_live_and_dead(self):
        import socket
        srv = socket.socket(); srv.bind(("127.0.0.1", 0)); srv.listen(1)
        port = srv.getsockname()[1]
        self.assertTrue(reachable(f"127.0.0.1:{port}", timeout=1))
        srv.close()
        self.assertFalse(reachable("127.0.0.1:1", timeout=1))   # nothing listening
        self.assertTrue(reachable("", timeout=1))               # unparseable -> not blocked
    def test_probe_http(self):
        import threading
        from http.server import BaseHTTPRequestHandler, HTTPServer
        html = (b"<html><head><title>Vault</title></head>"
                b"<!-- debug ?admin=1 --><form method=POST action=/login>"
                b"<input name=user><input name=pass></form></html>")
        class H(BaseHTTPRequestHandler):
            def log_message(self, *a): pass
            def do_GET(self):
                self.send_response(200); self.send_header("Server", "nginx")
                self.end_headers(); self.wfile.write(html)
        httpd = HTTPServer(("127.0.0.1", 0), H); port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            out = probe_instance(f"http://127.0.0.1:{port}/", timeout=2.0)
        finally:
            httpd.shutdown()
        self.assertIn("http: 200", out)
        self.assertIn("title: Vault", out)
        self.assertIn("action=/login", out)
        self.assertIn("user", out)            # input name surfaced
    def test_probe_tcp_banner(self):
        import socket, threading, time
        srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", 0)); port = srv.getsockname()[1]; srv.listen(1)
        def serve():
            c, _ = srv.accept(); c.sendall(b"welcome to pwnme v2\n"); time.sleep(0.05); c.close()
        threading.Thread(target=serve, daemon=True).start()
        try:
            out = probe_instance(f"nc 127.0.0.1 {port}", timeout=2.0)
        finally:
            srv.close()
        self.assertIn("welcome to pwnme", out)
    def test_probe_unreachable_is_empty(self):
        self.assertEqual(probe_instance("nc 127.0.0.1 1", timeout=1.0), "")


# --------------------------------------------------------------------------- #
# ensemble selection & reachability gate                                      #
# --------------------------------------------------------------------------- #
class TestEnsemble(unittest.TestCase):
    def test_majority_vote(self):
        agent = _StubAgent({"t#a0": "swarm{A}", "t#a1": "swarm{A}", "t#a2": "swarm{B}"})
        oc = _ensemble(agent).solve(Task("t", "t", "web", "s", files=[(Path("/t"), "a")]),
                                    _StubProfile())
        self.assertTrue(oc.solved)
        self.assertEqual(oc.value, "swarm{A}")                 # majority
    def test_first_to_correct_wins(self):
        agent = _StubAgent({"t#a0": "swarm{X}", "t#a1": "swarm{GOLD}", "t#a2": "swarm{Y}"})
        oc = _ensemble(agent).solve(Task("t", "t", "web", "s", files=[(Path("/t"), "a")]),
                                    _StubProfile(correct_value="swarm{GOLD}"))
        self.assertTrue(oc.correct)
        self.assertEqual(oc.value, "swarm{GOLD}")
    def test_reachability_gate_skips_dead_instance(self):
        agent = _StubAgent(raise_if_called=True)               # must not run
        oc = _ensemble(agent).solve(
            Task("t", "t", "pwn", "s", endpoint="127.0.0.1:1"), _StubProfile())
        self.assertFalse(oc.solved)
        self.assertIn("unreachable", oc.error)
        self.assertEqual(agent.calls, 0)


# --------------------------------------------------------------------------- #
# report & registry                                                           #
# --------------------------------------------------------------------------- #
class TestReportAndRegistry(unittest.TestCase):
    def test_kpis(self):
        outs = [
            Outcome("1", "a", "web", True, Grade.CORRECT, Candidate("f"), True,
                    0.02, 100, 30.0, 30.0, False, 2, ["flash"]),
            Outcome("2", "b", "pwn", True, Grade.INCORRECT, Candidate("g"), False,
                    0.04, 200, 0.0, None, True, 2, ["flash->pro"]),
            Outcome("3", "c", "web", False, Grade.NONE, None, False,
                    0.01, 50, 0.0, None, False, 2, ["flash"]),
        ]
        k = kpis(outs)
        self.assertEqual(k["correct"], 1)
        self.assertEqual(k["tasks"], 3)
        self.assertAlmostEqual(k["cost_per_flag_usd"], 0.07, places=4)
        self.assertAlmostEqual(k["escalation_rate"], 1 / 3, places=3)
        self.assertIn("web", k["by_category"])
        self.assertIn("# Farm run report", render_markdown(outs, {"label": "t"}))
    def test_registry(self):
        self.assertIn("ctf", available())
        self.assertIn("generic", available())
        with self.assertRaises(KeyError):
            build("nope")


class TestCtfdClientTimeouts(unittest.TestCase):
    def test_connect_timeout_is_tight(self):
        # Regression: when the host drops off the network mid-run, CTFd calls
        # must fail fast at connect, not stall for minutes on a half-open
        # socket (the freeze that wedged the live sweep when the Mac left the
        # LAN). A scalar 90s/300s timeout had no tight connect cap.
        try:
            import httpx  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("httpx not installed")
        from farm.orchestration.ctfd_client import CTFdClient
        root = Path(tempfile.mkdtemp(prefix="slopi_ctfd_"))
        self.addCleanup(shutil.rmtree, root, True)
        client = CTFdClient("https://127.0.0.1:1", "x-benchmark: t", root)
        self.addCleanup(client.c.close)
        connect = client.c.timeout.connect
        self.assertIsNotNone(connect, "connect timeout must be set explicitly")
        self.assertLessEqual(connect, 15.0,
                             "connect timeout too loose; a dead network would hang")


class TestLocalSandbox(unittest.TestCase):
    def _sandbox(self):
        from farm.config import SandboxConfig
        from farm.sandbox.local import LocalSandbox
        root = Path(tempfile.mkdtemp(prefix="slopi_test_"))
        self.addCleanup(shutil.rmtree, root, True)
        return LocalSandbox(root, SandboxConfig())

    def test_run_python_pythonpath_exposes_host_packages(self):
        # Regression: run() scrubs HOME, which used to hide the host user
        # site-packages and make PIL/pycryptodome/numpy unimportable in
        # run_python -- so only pure-stdlib tasks solved (lsb_stego failed the
        # clean-bench gate). run() must re-expose the host interpreter's site
        # dirs via PYTHONPATH.
        from farm.sandbox.local import _host_site_pythonpath
        expected = _host_site_pythonpath()
        self.assertTrue(expected, "host interpreter should expose a site dir")
        sb = self._sandbox()
        sb.write_file("_snippet.py",
                      "import os; print(os.environ.get('PYTHONPATH', ''))")
        res = sb.run("python3 _snippet.py")
        self.assertEqual(res.exit_code, 0, res.stderr)
        self.assertIn(expected.split(os.pathsep)[0], res.stdout)

    def test_run_keeps_home_scrubbed(self):
        # exposing packages must not leak the real HOME back into the sandbox.
        sb = self._sandbox()
        sb.write_file("_snippet.py",
                      "import os; print(os.environ.get('HOME', ''))")
        res = sb.run("python3 _snippet.py")
        self.assertEqual(res.exit_code, 0, res.stderr)
        self.assertEqual(res.stdout.strip(), sb.workdir)


class TestAgentToolResilience(unittest.TestCase):
    def test_tool_exception_becomes_recoverable_observation(self):
        # Regression: a tool that raises (e.g. the sandbox "path escapes" guard
        # on an absolute path) must NOT abort the whole attempt. The agent loop
        # turns it into an error observation and keeps going -- here it reaches
        # the terminal tool on the next step and still records a candidate.
        from farm.core.agent import ReActAgent
        from farm.core.contracts import Candidate, Task
        from farm.core.toolset import Tool, ToolSet
        from farm.gateway.types import ToolCall

        class _Usage:
            prompt_tokens = 1
            completion_tokens = 1

        class _Resp:
            def __init__(self, text="", tool_calls=None):
                self.text = text
                self.tool_calls = tool_calls or []
                self.has_tool_calls = bool(tool_calls)
                self.cost_usd = 0.0
                self.usage = _Usage()

        class _Gateway:
            def __init__(self, scripted):
                self._s = list(scripted)
            def chat(self, **kw):
                return self._s.pop(0) if self._s else _Resp("no further progress")

        class _BB:
            def render_for_prompt(self, *a, **k):
                return ""
            def mark_dead_end(self, *a, **k):
                pass

        def _boom(args, ctx):
            raise ValueError("path escapes sandbox: /tmp/x")

        def _win(args, ctx):
            ctx.candidate = Candidate("flag{ok}", "flag")
            return "recorded"

        tools = ToolSet([
            Tool("boom", "raises", {"type": "object", "properties": {}}, _boom),
            Tool("win", "submit", {"type": "object", "properties": {}}, _win,
                 terminal=True),
        ])
        gw = _Gateway([
            _Resp("try boom", [ToolCall(id="1", name="boom", arguments={})]),
            _Resp("now win", [ToolCall(id="2", name="win", arguments={})]),
        ])
        agent = ReActAgent(gateway=gw, blackboard=_BB())
        task = Task(id="t1", name="T", category="misc", statement="s")
        res = agent.run(task=task, toolset=tools, system_prompt="sys",
                        author="t1#a0", sandbox=_SB())
        self.assertEqual(res.outcome, "solved")
        self.assertIsNotNone(res.candidate)
        self.assertEqual(res.candidate.value, "flag{ok}")


class TestAdaptiveEffort(unittest.TestCase):
    def _swarm(self, adaptive, low_steps=5):
        import dataclasses
        return dataclasses.replace(SETTINGS.swarm, adaptive_effort=adaptive,
                                   low_signal_steps=low_steps)

    def test_disabled_returns_none(self):
        from farm.core.contracts import Task
        from farm.core.ensemble import _adaptive_step_override
        t = Task(id="t", name="n", category="misc", statement="s",
                 extra={"difficulty": "low"})
        self.assertIsNone(_adaptive_step_override(self._swarm(False), "sig", t))

    def test_high_signal_recon_keeps_full_budget(self):
        # even with a 'low' volume label, a real recon lead keeps the full budget
        from farm.core.contracts import Task
        from farm.core.ensemble import _adaptive_step_override
        t = Task(id="t", name="n", category="misc", statement="s",
                 extra={"difficulty": "low"})
        recon = "  elf imports: system, execve\n  elf symbols: main"
        self.assertIsNone(_adaptive_step_override(self._swarm(True), recon, t))

    def test_low_signal_recon_caps_budget(self):
        from farm.core.contracts import Task
        from farm.core.ensemble import _adaptive_step_override
        t = Task(id="t", name="n", category="misc", statement="s")
        self.assertEqual(
            _adaptive_step_override(self._swarm(True, 5), "  nothing useful here", t), 5)

    def test_no_recon_falls_back_to_difficulty(self):
        from farm.core.contracts import Task
        from farm.core.ensemble import _adaptive_step_override
        low = Task(id="t", name="n", category="misc", statement="s",
                   extra={"difficulty": "low"})
        med = Task(id="t", name="n", category="misc", statement="s",
                   extra={"difficulty": "medium"})
        self.assertEqual(_adaptive_step_override(self._swarm(True, 7), "", low), 7)
        self.assertIsNone(_adaptive_step_override(self._swarm(True, 7), "", med))


class TestCtfdEndpointExtraction(unittest.TestCase):
    def test_validated_extraction(self):
        from farm.adapters.ctfd_source import _endpoint_from_text
        self.assertEqual(_endpoint_from_text("Connect: nc chals.io 31337 to play"),
                         "nc chals.io 31337")
        self.assertEqual(_endpoint_from_text("service at http://x.test:8080/a."),
                         "http://x.test:8080/a")
        self.assertEqual(_endpoint_from_text("target 192.168.1.5:9001 now"),
                         "192.168.1.5:9001")
        # prose that is not a real endpoint yields nothing
        self.assertEqual(_endpoint_from_text("meeting at 12:34 today"), "")
        self.assertEqual(_endpoint_from_text(""), "")


class TestMCPClient(unittest.TestCase):
    # A tiny stdlib-only MCP stdio server: initialize, one 'echo' tool.
    STUB = (
        "import sys, json\n"
        "def send(m): sys.stdout.write(json.dumps(m)+chr(10)); sys.stdout.flush()\n"
        "for line in sys.stdin:\n"
        "    line=line.strip()\n"
        "    if not line: continue\n"
        "    msg=json.loads(line); mid=msg.get('id'); method=msg.get('method')\n"
        "    if method=='initialize':\n"
        "        send({'jsonrpc':'2.0','id':mid,'result':{'protocolVersion':'2024-11-05','capabilities':{'tools':{}},'serverInfo':{'name':'stub','version':'1'}}})\n"
        "    elif method=='notifications/initialized':\n"
        "        pass\n"
        "    elif method=='tools/list':\n"
        "        send({'jsonrpc':'2.0','id':mid,'result':{'tools':[{'name':'echo','description':'echo back msg','inputSchema':{'type':'object','properties':{'msg':{'type':'string'}}}}]}})\n"
        "    elif method=='tools/call':\n"
        "        p=msg.get('params',{}); args=p.get('arguments',{})\n"
        "        if p.get('name')=='echo':\n"
        "            send({'jsonrpc':'2.0','id':mid,'result':{'content':[{'type':'text','text':'echo: '+str(args.get('msg',''))}],'isError':False}})\n"
        "        else:\n"
        "            send({'jsonrpc':'2.0','id':mid,'result':{'content':[{'type':'text','text':'unknown tool'}],'isError':True}})\n"
        "    elif mid is not None:\n"
        "        send({'jsonrpc':'2.0','id':mid,'error':{'code':-32601,'message':'method not found'}})\n"
    )

    def _server_cmd(self):
        import sys
        root = Path(tempfile.mkdtemp(prefix="slopi_mcp_"))
        self.addCleanup(shutil.rmtree, root, True)
        p = root / "stub_server.py"
        p.write_text(self.STUB)
        return [sys.executable, str(p)]

    def test_list_and_call(self):
        from farm.orchestration.mcp_client import MCPStdioClient
        with MCPStdioClient(self._server_cmd()) as c:
            self.assertEqual([t["name"] for t in c.list_tools()], ["echo"])
            self.assertIn("echo: hi", c.call_tool("echo", {"msg": "hi"}))
            # a tool error becomes a recoverable string, never an exception
            self.assertTrue(c.call_tool("nope", {}).startswith("error:"))

    def test_build_mcp_tools_wraps_as_farm_tools(self):
        from farm.orchestration.mcp_client import build_mcp_tools
        tools, client = build_mcp_tools(self._server_cmd())
        try:
            self.assertEqual(tools[0].name, "mcp_echo")
            self.assertIn("echo: x", tools[0].fn({"msg": "x"}, None))
        finally:
            client.close()

    def test_timeout_on_silent_server(self):
        # a server that never answers must fail fast, not hang (hanging-conn lesson)
        import sys
        from farm.orchestration.mcp_client import MCPStdioClient, MCPError
        root = Path(tempfile.mkdtemp(prefix="slopi_mcp_"))
        self.addCleanup(shutil.rmtree, root, True)
        p = root / "silent.py"
        p.write_text("import sys, time\nfor _ in sys.stdin: time.sleep(5)\n")
        c = MCPStdioClient([sys.executable, str(p)], init_timeout=1.0)
        self.addCleanup(c.close)
        with self.assertRaises(MCPError):
            c.start()


if __name__ == "__main__":
    unittest.main(verbosity=2)
