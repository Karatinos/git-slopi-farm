#!/usr/bin/env python3
"""Prove the farm solves INSTANCE (live-service) tasks end-to-end, offline/free.
Starts a local HTTP service holding a flag, builds a web task pointing at it,
runs the engine (scripted provider), and asserts a CORRECT verdict.
"""
from __future__ import annotations
import dataclasses, http.server, socketserver, sys, threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from farm.config import SETTINGS
from farm.core import Engine, build
from farm.core.contracts import Task
import farm.profiles  # register ctf/generic

FLAG = "flag{l1v3_s3rv1c3_r34ch3d_0k}"

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = FLAG.encode() if self.path in ("/", "/flag") else b"nothing here\n"
        self.send_response(200); self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def log_message(self, *a):  # silence
        pass

def main():
    httpd = socketserver.TCPServer(("127.0.0.1", 0), H)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    ep = f"http://127.0.0.1:{port}/"
    settings = dataclasses.replace(SETTINGS, provider="scripted")
    eng = Engine(settings=settings, global_cap_usd=1.0)
    profile = build("ctf", flag_format="flag{...}")
    task = Task(id="instance/web_demo", name="web_demo", category="web",
                statement="A live web service is running. Recover the flag.",
                endpoint=ep, answer_format="flag{...}", gold=FLAG)
    oc = eng.solve_one(profile, task)
    httpd.shutdown()
    print(f"endpoint   : {ep}")
    print(f"provider   : {eng.provider}")
    print(f"correct    : {oc.correct}  grade={oc.grade.value}  value={oc.value}")
    print(f"cost       : ${oc.cost_usd:.4f}  attempts={oc.n_attempts}")
    print("RESULT:", "PASS (instance solved end-to-end)" if oc.correct else "FAIL")
    return 0 if oc.correct else 1

if __name__ == "__main__":
    raise SystemExit(main())
