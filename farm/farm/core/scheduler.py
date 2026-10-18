"""Control plane: priority scheduling + admission control (blueprint §7–8).

A free slot always goes to the task with the best points-per-resource density,
not the next in line:

    priority ≈ (points · p_solve · decay) / est_cost + deadline_boost − sink_penalty

`p_solve` and `est_cost` are cheap category heuristics (refined later from the
solution bank). Admission control drops only non-actionable tasks (no files and
no live target). The plan then groups same-category tasks adjacently so their
long, identical system prefixes hit the provider prefix-cache (−cost, −latency),
which the blueprint flags as a nearly-free lever.

Domain-agnostic: it schedules `Task`s and never asks what competition they came
from.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

from .contracts import Task

# category difficulty priors (p_solve, relative est_cost); "the tail is hard".
_PRIORS: Dict[str, tuple] = {
    "web": (0.55, 1.0), "forensics": (0.5, 1.0), "forensic": (0.5, 1.0),
    "misc": (0.45, 1.0), "osint": (0.4, 1.1), "crypto": (0.35, 1.2),
    "reverse": (0.3, 1.3), "rev": (0.3, 1.3), "pwn": (0.2, 1.5),
    # generic (non-CTF) competition domains
    "algorithmic": (0.45, 1.2), "data": (0.55, 1.0), "math": (0.45, 1.1),
    "geometry": (0.4, 1.1), "protocol": (0.4, 1.2), "generic": (0.45, 1.0),
}


@dataclass
class Scheduler:
    group_by_category: bool = True
    sink_penalties: Optional[Dict[str, float]] = None   # task_id -> penalty (from prior stalls)

    def priority(self, task: Task, now: Optional[float] = None) -> float:
        # Prefer a triage assessment stored on the task; fall back to the prior.
        prior_p, prior_c = _PRIORS.get(task.category.lower(), (0.4, 1.1))
        p_solve = float(task.extra.get("p_solve", prior_p))
        est_cost = float(task.extra.get("est_cost",
                                        prior_c * (1.0 + 0.2 * (len(task.files) > 2))))
        base = (task.points * p_solve) / max(est_cost, 0.1)
        boost = 0.0
        if task.deadline_ts:
            now = now or time.time()
            remaining = task.deadline_ts - now
            if 0 < remaining < 1800:                     # <30 min: push it up
                boost = 5.0 * (1 - remaining / 1800)
        sink = (self.sink_penalties or {}).get(task.id, 0.0)
        return base + boost - sink

    def plan(self, tasks: Sequence[Task], *, categories: Optional[Sequence[str]] = None,
             limit: Optional[int] = None, offline_only: bool = False) -> List[Task]:
        now = time.time()
        admitted = [t for t in tasks
                    if t.actionable and (not offline_only or not t.has_service)
                    and (not categories or t.category.lower() in
                         {c.lower() for c in categories})]
        admitted.sort(key=lambda t: self.priority(t, now), reverse=True)
        ordered = self._group(admitted) if self.group_by_category else admitted
        return ordered[:limit] if limit else ordered

    def _group(self, tasks: List[Task]) -> List[Task]:
        """Keep global priority order but pull same-category tasks together, so
        the stable per-category system prefix stays hot in the prefix-cache."""
        seen: List[str] = []
        buckets: Dict[str, List[Task]] = {}
        for t in tasks:                                  # preserves priority order
            buckets.setdefault(t.category, []).append(t)
            if t.category not in seen:
                seen.append(t.category)
        out: List[Task] = []
        for cat in seen:                                 # categories by first (best) appearance
            out.extend(buckets[cat])
        return out
