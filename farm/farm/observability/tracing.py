"""Per-step tracing.

Every trajectory is logged as an ordered sequence of
thought -> action -> observation events, each with tokens, cost, latency and
outcome. Traces are the debugging surface for a swarm of hundreds of agents and
the raw material for the future self-improvement loop (blueprint §11), so we
turn tracing on from day one.

Storage: newline-delimited JSON per trajectory under data/traces/, plus a
summary row written to the DB by the caller. NDJSON keeps it append-only and
crash-safe (a killed worker still leaves a valid partial trace).
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..config import TRACE_DIR


def new_trace_id() -> str:
    return uuid.uuid4().hex


@dataclass
class Span:
    step: int
    kind: str                       # 'llm' | 'tool' | 'note'
    name: str                       # tier / tool name
    started_at: float
    duration_ms: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0
    payload: Dict[str, Any] = field(default_factory=dict)   # small, truncated
    result: str = ""                # truncated observation / text


class Tracer:
    def __init__(self, trace_id: Optional[str] = None, meta: Optional[dict] = None,
                 trace_dir: Path = TRACE_DIR):
        self.trace_id = trace_id or new_trace_id()
        self.path = trace_dir / f"{self.trace_id}.ndjson"
        self.spans: List[Span] = []
        self._step = 0
        self.meta = meta or {}
        self._write({"type": "meta", "trace_id": self.trace_id, **self.meta})

    def _write(self, obj: dict) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False, default=str) + "\n")

    @staticmethod
    def _trunc(s: Any, n: int = 2000) -> str:
        s = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False, default=str)
        return s if len(s) <= n else s[:n] + f"...<+{len(s) - n} chars>"

    def start(self, kind: str, name: str, payload: Optional[dict] = None) -> Span:
        self._step += 1
        sp = Span(step=self._step, kind=kind, name=name,
                  started_at=time.time(), payload=payload or {})
        return sp

    def finish(self, sp: Span, *, tokens_in: int = 0, tokens_out: int = 0,
               cost_usd: float = 0.0, result: str = "") -> None:
        sp.duration_ms = (time.time() - sp.started_at) * 1000.0
        sp.tokens_in, sp.tokens_out, sp.cost_usd = tokens_in, tokens_out, cost_usd
        sp.result = self._trunc(result)
        sp.payload = {k: self._trunc(v, 800) for k, v in sp.payload.items()}
        self.spans.append(sp)
        self._write({"type": "span", **asdict(sp)})

    def note(self, name: str, **fields) -> None:
        self._write({"type": "note", "name": name, "step": self._step, **fields})

    def close(self, outcome: dict) -> None:
        self._write({"type": "end", "trace_id": self.trace_id,
                     "steps": self._step, **outcome})

    # convenience aggregates
    @property
    def total_cost(self) -> float:
        return sum(s.cost_usd for s in self.spans)

    @property
    def total_tokens(self) -> int:
        return sum(s.tokens_in + s.tokens_out for s in self.spans)
