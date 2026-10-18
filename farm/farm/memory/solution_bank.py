"""Solution bank (RAG) — the fully-API-compatible growth loop (blueprint §10).

Every solved trajectory is distilled into a reusable card: category, a short
summary of the attack vector, and a template of the key steps/tools. On a new
task the bank retrieves the most similar past cards and the agent injects them
as few-shot demonstrations. This is the main, cheap, "cascade-free" way the
swarm gets smarter over time without touching model weights.
"""
from __future__ import annotations

import json
import time
from typing import Dict, List, Optional

import numpy as np

from .embeddings import DEFAULT_EMBEDDER, cosine
from .store import Store


class SolutionBank:
    def __init__(self, store: Store, embedder=DEFAULT_EMBEDDER):
        self.store = store
        self.embedder = embedder

    def add(self, *, category: str, title: str, summary: str, template: str,
            task_id: Optional[str] = None) -> None:
        text = f"{category} :: {title} :: {summary}"
        vec = self.embedder.embed(text).tolist()
        self.store.execute(
            "INSERT INTO solutions (task_id, category, title, summary, template, vector, ts) "
            "VALUES (?,?,?,?,?,?,?)",
            (task_id, category, title, summary, template,
             json.dumps(vec), time.time()))

    def retrieve(self, query: str, category: Optional[str] = None,
                 k: int = 3) -> List[Dict]:
        rows = self.store.query(
            "SELECT category, title, summary, template, vector FROM solutions"
            + (" WHERE category=?" if category else ""),
            (category,) if category else ())
        if not rows:
            return []
        qv = self.embedder.embed(query)
        scored = []
        for r in rows:
            v = np.array(json.loads(r["vector"]), dtype=np.float32)
            scored.append((cosine(qv, v), dict(r)))
        scored.sort(key=lambda x: x[0], reverse=True)
        out = []
        for score, r in scored[:k]:
            r.pop("vector", None)
            r["score"] = round(score, 4)
            out.append(r)
        return out

    def render_fewshot(self, query: str, category: Optional[str] = None,
                       k: int = 2, min_score: float = 0.08) -> str:
        hits = [h for h in self.retrieve(query, category, k) if h["score"] >= min_score]
        if not hits:
            return ""
        lines = ["## Relevant past solutions (from the farm's solution bank):"]
        for h in hits:
            lines.append(f"### {h['title']} ({h['category']}, sim={h['score']})")
            lines.append(h["summary"])
            if h["template"]:
                lines.append("Template:\n" + h["template"])
        return "\n".join(lines)

    def count(self) -> int:
        r = self.store.query_one("SELECT COUNT(*) AS n FROM solutions")
        return r["n"] if r else 0
