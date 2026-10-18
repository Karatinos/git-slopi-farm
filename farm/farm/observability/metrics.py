"""KPI computation (blueprint §11.2).

The metrics the blueprint says actually matter:
  cost-per-flag, time-to-flag, solve-rate (overall + by category),
  escalation-rate, stall/cancel-rate.
Computed from the list of per-task EnsembleResults of a run.
"""
from __future__ import annotations

import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List

# forward ref to avoid import cycle
try:
    from ..pipeline.ensemble import EnsembleResult
except Exception:  # noqa: BLE001
    EnsembleResult = object  # type: ignore


@dataclass
class RunMetrics:
    provider: str
    mode: str
    tasks_total: int = 0
    tasks_gradable: int = 0
    solved_correct: int = 0
    solved_ungradable: int = 0
    total_cost_usd: float = 0.0
    total_tokens: int = 0
    escalated_tasks: int = 0
    attempts_total: int = 0
    attempts_stalled: int = 0
    attempts_killed: int = 0
    time_to_flag: List[float] = field(default_factory=list)
    by_category: Dict[str, Dict[str, int]] = field(default_factory=dict)

    @property
    def solve_rate(self) -> float:
        denom = self.tasks_gradable or self.tasks_total
        return self.solved_correct / denom if denom else 0.0

    @property
    def cost_per_flag(self) -> float:
        flags = self.solved_correct + self.solved_ungradable
        return self.total_cost_usd / flags if flags else float("nan")

    @property
    def escalation_rate(self) -> float:
        return self.escalated_tasks / self.tasks_total if self.tasks_total else 0.0

    @property
    def stall_cancel_rate(self) -> float:
        return ((self.attempts_stalled + self.attempts_killed) /
                self.attempts_total) if self.attempts_total else 0.0

    @property
    def median_ttf(self) -> float:
        return statistics.median(self.time_to_flag) if self.time_to_flag else 0.0

    @property
    def mean_ttf(self) -> float:
        return statistics.mean(self.time_to_flag) if self.time_to_flag else 0.0

    def as_dict(self) -> dict:
        return {
            "provider": self.provider, "mode": self.mode,
            "tasks_total": self.tasks_total, "tasks_gradable": self.tasks_gradable,
            "solved_correct": self.solved_correct,
            "solved_ungradable": self.solved_ungradable,
            "solve_rate": round(self.solve_rate, 4),
            "cost_per_flag": round(self.cost_per_flag, 5)
            if self.cost_per_flag == self.cost_per_flag else None,
            "total_cost_usd": round(self.total_cost_usd, 5),
            "total_tokens": self.total_tokens,
            "escalation_rate": round(self.escalation_rate, 4),
            "stall_cancel_rate": round(self.stall_cancel_rate, 4),
            "median_ttf_s": round(self.median_ttf, 3),
            "mean_ttf_s": round(self.mean_ttf, 3),
            "by_category": self.by_category,
        }


def compute(results: List["EnsembleResult"], *, provider: str, mode: str,
            gradable_ids: set) -> RunMetrics:
    m = RunMetrics(provider=provider, mode=mode)
    cat = defaultdict(lambda: {"total": 0, "solved": 0})
    for r in results:
        m.tasks_total += 1
        if r.task_id in gradable_ids:
            m.tasks_gradable += 1
        m.total_cost_usd += r.total_cost_usd
        m.total_tokens += r.total_tokens
        if r.escalated:
            m.escalated_tasks += 1
        category = r.task_id.split("/")[0]
        cat[category]["total"] += 1
        for a in r.attempts:
            m.attempts_total += 1
            if a.outcome == "stalled":
                m.attempts_stalled += 1
            elif a.outcome == "killed":
                m.attempts_killed += 1
        if r.solved and r.graded == "correct":
            m.solved_correct += 1
            cat[category]["solved"] += 1
            if r.time_to_flag is not None:
                m.time_to_flag.append(r.time_to_flag)
        elif r.solved and r.graded == "ungradable":
            m.solved_ungradable += 1
            if r.time_to_flag is not None:
                m.time_to_flag.append(r.time_to_flag)
    m.by_category = {k: dict(v) for k, v in sorted(cat.items())}
    return m
