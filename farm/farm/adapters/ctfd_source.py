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
from ..orchestration.ctfd_client import CTFdClient

_OUT = DATA_DIR / "ctf_bench" / "files"


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
                m = re.search(r'https?://\S+|\d{1,3}(?:\.\d{1,3}){3}[:\s]\d+', ch.description)
                endpoint = m.group(0).strip() if m else ""
            out.append({
                "id": f"ctfd/{ch.id}", "name": ch.name, "category": ch.category,
                "statement": ch.description, "files": ch.files, "endpoint": endpoint,
                "points": ch.value, "extra": {"cid": ch.id}})
        return out

    def submitter(self, cid, flag: str) -> str:
        return self.client.submit(cid, flag)

    def close(self) -> None:
        self.client.close()
