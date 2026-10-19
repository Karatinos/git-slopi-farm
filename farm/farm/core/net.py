"""Tiny network-reachability helper for live-service (instance) tasks.

A fast TCP connect test so the engine can skip a task whose instance host is
down instead of spending the whole per-task budget on an agent that just retries
hanging connects (blueprint §9: don't burn budget on dead ends). Parsing is
best-effort over the shapes a scoreboard emits: `host:port`, `nc host port`,
`http(s)://host[:port]/...`.
"""
from __future__ import annotations

import re
import socket
from typing import Optional, Tuple
from urllib.parse import urlparse


def parse_endpoint(endpoint: str) -> Optional[Tuple[str, int]]:
    """Extract (host, port) from an endpoint string, or None if unparseable."""
    e = (endpoint or "").strip()
    if not e:
        return None
    if e.startswith(("http://", "https://")):
        u = urlparse(e)
        if u.hostname:
            return (u.hostname, u.port or (443 if u.scheme == "https" else 80))
        return None
    m = re.search(r"\bnc\s+(\S+)\s+(\d{1,5})", e)              # nc host port
    if m:
        return (m.group(1), int(m.group(2)))
    m = re.search(r"([A-Za-z0-9_.\-]+)[:\s](\d{1,5})\b", e)    # host:port / host port
    if m:
        return (m.group(1), int(m.group(2)))
    return None


def reachable(endpoint: str, timeout: float = 3.0) -> bool:
    """True if a TCP connection to the endpoint's host:port succeeds quickly.
    Unparseable endpoints are treated as reachable (don't block on uncertainty)."""
    hp = parse_endpoint(endpoint)
    if hp is None:
        return True
    host, port = hp
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:  # noqa: BLE001  (refused, timeout, DNS, unreachable)
        return False


def _http_probe(host: str, port: int, scheme: str, timeout: float) -> str:
    """Fast HTTP recon: status, telling headers, <title>, forms, HTML comments,
    and a bounded robots.txt peek. Best-effort; returns '' on any failure."""
    import urllib.request
    out = []

    def _get(path):
        url = f"{scheme}://{host}:{port}{path}"
        req = urllib.request.Request(url, headers={"User-Agent": "slopi-recon/1"})
        with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310 (task target)
            body = r.read(20000)
            return r.status, dict(r.headers), body
    try:
        status, hdrs, body = _get("/")
    except Exception as e:  # noqa: BLE001
        # a 401/403/… still carries useful headers
        import urllib.error
        if isinstance(e, urllib.error.HTTPError):
            status, hdrs, body = e.code, dict(e.headers), (e.read(20000) if hasattr(e, "read") else b"")
        else:
            return ""
    out.append(f"  http: {status} {scheme}://{host}:{port}/")
    for h in ("Server", "X-Powered-By", "WWW-Authenticate", "Location", "Set-Cookie", "Content-Type"):
        if hdrs.get(h):
            out.append(f"  hdr {h}: {str(hdrs[h])[:90]}")
    try:
        text = body.decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        text = ""
    mt = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    if mt:
        out.append(f"  title: {mt.group(1).strip()[:100]}")
    for c in re.findall(r"<!--(.*?)-->", text, re.S)[:3]:
        c = c.strip()
        if c:
            out.append(f"  comment: {c[:110]}")
    for f in re.findall(r"<form[^>]*>", text, re.I)[:3]:
        ma = re.search(r'action\s*=\s*["\']?([^"\'\s>]+)', f, re.I)
        mm = re.search(r'method\s*=\s*["\']?([^"\'\s>]+)', f, re.I)
        out.append(f"  form: method={(mm.group(1) if mm else 'GET')} action={ma.group(1) if ma else '/'}")
    inputs = re.findall(r'<input[^>]*name\s*=\s*["\']?([^"\'\s>]+)', text, re.I)[:8]
    if inputs:
        out.append("  inputs: " + ", ".join(dict.fromkeys(inputs)))
    try:
        rs, _rh, rb = _get("/robots.txt")
        if rs == 200 and rb:
            dis = [l for l in rb.decode("utf-8", "replace").splitlines() if l.lower().startswith(("disallow", "allow"))][:5]
            if dis:
                out.append("  robots: " + " ".join(dis))
    except Exception:  # noqa: BLE001
        pass
    return "\n".join(out)


def _tcp_probe(host: str, port: int, timeout: float) -> str:
    """Raw-TCP banner grab: read what the service greets with; if silent, nudge
    with a newline and read the reply. Best-effort; returns '' on failure."""
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            chunks = []
            try:
                chunks.append(s.recv(512))
            except Exception:  # noqa: BLE001
                pass
            if not chunks or not chunks[0]:
                try:
                    s.sendall(b"\n")
                    chunks.append(s.recv(512))
                except Exception:  # noqa: BLE001
                    pass
            data = b"".join(chunks)
            if not data:
                return f"  tcp: connected {host}:{port} (no banner)"
            txt = data.decode("utf-8", "replace").strip()
            lines = [l for l in txt.splitlines() if l.strip()][:6]
            return f"  tcp banner {host}:{port}:\n" + "\n".join("    " + l[:110] for l in lines)
    except Exception:  # noqa: BLE001
        return ""


def probe_instance(endpoint: str, timeout: float = 3.0) -> str:
    """Lightweight recon of a LIVE instance (the instance analogue of file recon).

    HTTP endpoints → status/headers/title/forms/comments/robots.
    Raw TCP (nc/host:port) → banner grab.
    Bounded and fast so it never burns the per-task budget. '' on any failure."""
    hp = parse_endpoint(endpoint)
    if hp is None:
        return ""
    host, port = hp
    e = (endpoint or "").strip()
    is_http = e.startswith(("http://", "https://")) or port in (80, 443, 8000, 8080, 8443, 5000, 3000)
    scheme = "https" if (e.startswith("https://") or port == 443) else "http"
    if is_http:
        r = _http_probe(host, port, scheme, timeout)
        if r:
            return r
    r = _tcp_probe(host, port, timeout)
    return r
