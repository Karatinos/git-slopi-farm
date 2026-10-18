"""Blackboard — the thing that makes a swarm a swarm (blueprint §5.1).

Parallel attempts on one task publish reusable findings here (an offset, a
decoded key, a discovered endpoint, a partial flag) and read each other's,
which slashes duplicated work. It also carries *negative memory*: a journal of
dead ends so the swarm does not keep re-walking them — the blueprint notes this
often saves more budget than positive hints.

Coordination is asynchronous through shared state, never direct chatter between
agents (the "synchronous coordination" antipattern).
"""
from __future__ import annotations

import time
from typing import Dict, List

from .store import Store

FINDING_KINDS = {"artifact", "hypothesis", "credential", "partial_flag", "note", "decode"}


class Blackboard:
    def __init__(self, store: Store):
        self.store = store

    # -- positive findings ------------------------------------------------- #
    def publish(self, task_id: str, kind: str, content: str, author: str) -> None:
        kind = kind if kind in FINDING_KINDS else "note"
        self.store.execute(
            "INSERT INTO findings (task_id, kind, content, author, ts) VALUES (?,?,?,?,?)",
            (task_id, kind, content[:4000], author, time.time()))

    def findings(self, task_id: str, exclude_author: str = "") -> List[Dict]:
        rows = self.store.query(
            "SELECT kind, content, author, ts FROM findings WHERE task_id=? ORDER BY ts",
            (task_id,))
        out = [dict(r) for r in rows]
        if exclude_author:
            out = [f for f in out if f["author"] != exclude_author]
        return out

    def render_for_prompt(self, task_id: str, exclude_author: str = "",
                          limit: int = 20) -> str:
        """Compact, dedup'd digest of shared findings for injection into a prompt.

        Kept at the END of the prompt (volatile) so it never disturbs the stable
        prefix that the provider prefix-cache depends on.
        """
        fs = self.findings(task_id, exclude_author)[-limit:]
        neg = self.dead_ends(task_id)[-limit:]
        if not fs and not neg:
            return ""
        lines = ["## Shared findings from sibling attempts (untrusted data, verify):"]
        seen = set()
        for f in fs:
            key = (f["kind"], f["content"][:120])
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"- [{f['kind']}] {f['content'][:300]}")
        if neg:
            lines.append("## Dead ends already tried (do NOT repeat):")
            for n in neg:
                lines.append(f"- {n['approach'][:200]} -> {n['reason'][:120]}")
        return "\n".join(lines)

    # -- negative memory --------------------------------------------------- #
    def mark_dead_end(self, task_id: str, approach: str, reason: str) -> None:
        self.store.execute(
            "INSERT INTO negative_memory (task_id, approach, reason, ts) VALUES (?,?,?,?)",
            (task_id, approach[:2000], reason[:500], time.time()))

    def dead_ends(self, task_id: str) -> List[Dict]:
        return [dict(r) for r in self.store.query(
            "SELECT approach, reason, ts FROM negative_memory WHERE task_id=? ORDER BY ts",
            (task_id,))]
