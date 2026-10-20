"""Live-scoreboard source adapter (CTFd).

Reads challenges into profile-neutral raw records `{id, name, category,
statement, files, endpoint, points, extra}` and exposes a `submitter`
(challenge_id, flag) -> status for the profile's live verdict. The farm's
instance support is here: a challenge's `connection_info` becomes `endpoint`, so
a pure-instance challenge with no files is still ingested and attempted.

Wraps the existing, battle-tested `CTFdClient` (streaming downloads with retry,
CSRF handling, throwaway registration).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

from ..config import DATA_DIR
from ..core.net import parse_endpoint
from ..orchestration.ctfd_client import CTFdClient

_OUT = DATA_DIR / "ctf_bench" / "files"

# Endpoint shapes a description might mention, widest-signal first. Each
# candidate is validated with net.parse_endpoint, so prose like "at 12:34"
# never becomes a bogus endpoint.
_EP_PATTERNS = (
    r"https?://\S+",
    r"\bnc\s+\S+\s+\d{1,5}\b",
    r"\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b",
    r"\b[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)+:\d{1,5}\b",
)


def _endpoint_from_text(text: str) -> str:
    """Best-effort extract a *validated* endpoint string from a description."""
    for pat in _EP_PATTERNS:
        for m in re.finditer(pat, text or ""):
            cand = m.group(0).strip().rstrip(".,);]")
            if parse_endpoint(cand) is not None:
                return cand
    return ""


class CTFdSource:
    def __init__(self, base_url: str, header: str, reg_code: str,
                 account_prefix: str = "slopi"):
        self.client = CTFdClient(base_url, header, _OUT)
        self.account = self.client.register(reg_code, prefix=account_prefix)

    def read(self) -> List[dict]:
        out: List[dict] = []
        for ch in self.client.fetch():
            endpoint = (ch.connection_info or "").strip()
            if not endpoint:
                endpoint = _endpoint_from_text(ch.description)
            out.append({
                "id": f"ctfd/{ch.id}", "name": ch.name, "category": ch.category,
                "statement": ch.description, "files": ch.files, "endpoint": endpoint,
                "points": ch.value, "extra": {"cid": ch.id}})
        return out

    def submitter(self, cid, flag: str) -> str:
        return self.client.submit(cid, flag)

    def close(self) -> None:
        self.client.close()
