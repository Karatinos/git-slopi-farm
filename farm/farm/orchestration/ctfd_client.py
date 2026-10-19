"""Minimal CTFd client for the benchmark instance.

Access chain: an outer forward-auth proxy (auth.snowyx.dev) is cleared by the
`x-benchmark` header on every request; CTFd's own challenge API then needs a
logged-in session, so we register a throwaway benchmark account with the
registration code. Flags are not exposed by the API (admin-only), so scoring is
done the real way: submit the farm's candidate flag to /api/v1/challenges/attempt
and record CTFd's correct/incorrect verdict.

Only reads challenges and submits flags for solved tasks; touches nothing else.
"""
from __future__ import annotations

import re
import secrets
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import httpx


@dataclass
class Challenge:
    id: int
    name: str
    category: str
    description: str
    value: int
    files: List[Tuple[Path, str]] = field(default_factory=list)
    connection_info: str = ""


class CTFdClient:
    def __init__(self, base_url: str, bench_header: str, files_dir: Path):
        name, _, value = bench_header.partition(":")
        self.h = {name.strip(): value.strip()}
        self.files_dir = files_dir
        self.files_dir.mkdir(parents=True, exist_ok=True)
        self.c = httpx.Client(base_url=base_url, timeout=90, follow_redirects=True,
                              headers=self.h)
        self.who = None

    def _nonce(self, path: str) -> str:
        html = self.c.get(path).text
        m = re.search(r"'csrfNonce':\s*\"([0-9a-f]+)\"", html)
        if not m:
            m = re.search(r'name=["\']nonce["\'][^>]*value=["\']([0-9a-f]+)', html)
        if not m:
            raise RuntimeError(f"no CSRF nonce on {path}")
        return m.group(1)

    def register(self, registration_code: str, prefix: str = "slopi") -> str:
        """Register an identifiable account for this run and RECORD its creds so
        the human can log in and see this prototype's solves on the scoreboard.
        Username is <prefix>_<rand> (prefix carries the prototype/label)."""
        uid = secrets.token_hex(3)
        user = f"{prefix}_{uid}"[:48]
        pw = secrets.token_urlsafe(16)
        data = {"name": user, "email": f"{user}@bench.local", "password": pw,
                "nonce": self._nonce("/register"),
                "registration_code": registration_code, "_submit": "Submit"}
        r = self.c.post("/register", data=data)
        probe = self.c.get("/api/v1/challenges", headers={"Accept": "application/json"})
        if "login" in str(probe.url) or not probe.headers.get("content-type", "").startswith("application/json"):
            raise RuntimeError(f"registration did not authenticate (status {r.status_code}, "
                               f"probe -> {probe.url})")
        self.who = user
        try:  # record creds for the human (never shown to agents)
            acct = self.files_dir.parent / "accounts.log"
            with acct.open("a") as fh:
                fh.write(f"{time.strftime('%Y-%m-%d %H:%M')}\t{user}\t{pw}\n")
        except Exception:  # noqa: BLE001
            pass
        return user

    def _download(self, cid: int, url: str) -> Optional[Tuple[Path, str]]:
        """Stream one challenge file to disk. Robust: retries a couple of times,
        streams (so a large forensic image doesn't buffer in RAM), and returns
        None on persistent failure so ONE bad/flaky/huge file never aborts the
        whole fetch. A file already on disk from a prior run is reused."""
        fn = url.split("/")[-1].split("?")[0]
        dest = self.files_dir / f"{cid}__{fn}"
        if dest.exists() and dest.stat().st_size > 0:
            return (dest, fn)
        for attempt in range(3):
            try:
                with self.c.stream("GET", url, timeout=300) as r:
                    if r.status_code != 200:
                        return None
                    tmp = dest.with_suffix(dest.suffix + ".part")
                    with open(tmp, "wb") as fh:
                        for chunk in r.iter_bytes(1 << 20):
                            fh.write(chunk)
                    tmp.rename(dest)
                return (dest, fn)
            except Exception:  # noqa: BLE001  (protocol error, timeout, reset...)
                try:
                    dest.with_suffix(dest.suffix + ".part").unlink()
                except OSError:
                    pass
                time.sleep(2 * (attempt + 1))
        return None

    def fetch(self) -> List[Challenge]:
        j = self.c.get("/api/v1/challenges", headers={"Accept": "application/json"}).json()
        out: List[Challenge] = []
        for row in j.get("data", []):
            cid = row["id"]
            try:
                det = self.c.get(f"/api/v1/challenges/{cid}",
                                 headers={"Accept": "application/json"}).json().get("data", {})
            except Exception:  # noqa: BLE001  (never let one challenge abort the fetch)
                det = {"name": row.get("name", str(cid)),
                       "category": row.get("category", "misc"), "description": "",
                       "value": row.get("value", 0), "files": []}
            files: List[Tuple[Path, str]] = []
            for url in det.get("files", []):
                got = self._download(cid, url)
                if got:
                    files.append(got)
            out.append(Challenge(
                id=cid, name=det.get("name", row.get("name", str(cid))),
                category=(det.get("category") or row.get("category") or "misc").lower(),
                description=det.get("description", ""), value=det.get("value", row.get("value", 0)),
                files=files, connection_info=det.get("connection_info") or ""))
        return out

    def submit(self, challenge_id: int, flag: str) -> str:
        """Submit a flag; return CTFd's status: correct | incorrect | already_solved
        | ratelimited | <other>."""
        data = {"challenge_id": challenge_id, "submission": flag}
        for attempt in range(3):
            try:
                r = self.c.post("/api/v1/challenges/attempt", json=data,
                                headers={"Accept": "application/json",
                                         "CSRF-Token": self._nonce("/challenges")})
                try:
                    return r.json().get("data", {}).get("status", f"http{r.status_code}")
                except Exception:  # noqa: BLE001
                    return f"http{r.status_code}"
            except Exception as e:  # noqa: BLE001  (network flap must not kill the run)
                if attempt < 2:
                    time.sleep(2 * (attempt + 1)); continue
                return f"error:{type(e).__name__}"
        return "error"

    def close(self) -> None:
        self.c.close()
