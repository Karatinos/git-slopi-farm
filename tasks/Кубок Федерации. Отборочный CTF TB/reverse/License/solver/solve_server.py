#!/usr/bin/env python3
"""Local HTTPS activation server for the MosMetro AutoPilot CTF challenge."""

from __future__ import annotations

import argparse
import json
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

# The valid PRO activation contract the client expects. This is the whole point
# of the intended solve: return exactly this to unlock PRO. Non-secret; keep in
# sync with source/tools/generate_secrets.py and the static site.
CONFIG = {
    "x_admin_token": "7a8f9c3e2b1d4056a9c8f7e6d5b4a3c2",
    "endpoints": {"check": "/check", "status": "/status"},
    "response_success": {
        "valid": True,
        "active": True,
        "exists": True,
        "expires_at": "2099-12-31T23:59:59Z",
        "days_left": 3650,
        "client": "CTF",
        "plan": "pro",
    },
}


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a local MosMetro activation server.")
    parser.add_argument("--cert", type=Path, default=Path(__file__).with_name("cert.pem"))
    parser.add_argument("--key", type=Path, default=Path(__file__).with_name("key.pem"))
    parser.add_argument("--port", type=int, default=443)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    config = CONFIG

    if not args.cert.is_file() or not args.key.is_file():
        raise SystemExit("Certificate files are missing. Run solver/gen_cert.py <activation-host> first.")

    body = json.dumps(config["response_success"], ensure_ascii=False).encode("utf-8")
    token = config["x_admin_token"]

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def _reply(self, payload: bytes = body) -> None:
            print(f"{self.command} {self.path} from {self.client_address[0]}")
            # The client only checks that we ECHO its own X-Admin-Token back, so we
            # simply reflect the request header — the token's value is never needed.
            # (Fallback to the known constant for requests that omit it, e.g. GET.)
            echoed = self.headers.get("X-Admin-Token") or token
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("X-Admin-Token", echoed)
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:  # noqa: N802
            if self.path == config["endpoints"]["status"]:
                self._reply()
            else:
                self.send_error(404)

        def do_POST(self) -> None:  # noqa: N802
            if self.path == config["endpoints"]["check"]:
                # Any key is accepted: the vulnerability is that the client trusts
                # whatever the (attacker-controlled) server returns. The typed key
                # is irrelevant; we drain it only to finish reading the request.
                content_length = int(self.headers.get("Content-Length", "0"))
                if content_length:
                    self.rfile.read(content_length)
                self._reply()
            else:
                self.send_error(404)

        def log_message(self, _format: str, *_args: object) -> None:
            pass

    server = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(args.cert, args.key)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    print(f"Activation server listening on https://0.0.0.0:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
