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
