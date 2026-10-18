"""Triage stage (blueprint §6, §8.2) — cheap assessment before scheduling.

A fast, deterministic pass (no LLM spend) that estimates, per task:
  * p_solve   — probability the swarm solves it, from the category prior,
                *refined by the solution bank* ("we've solved similar before"
                → up; negative memory on this task → down). This is the moat
                feeding the scheduler, exactly as §11.3 describes.
  * difficulty — low | medium | hard, from category + material volume; drives
                 adaptive effort (don't spend a full step budget on an opaque
                 task with no lead).
  * est_cost  — relative resource estimate for the knapsack density.

Domain-agnostic: it reads a `Task` and the shared bank/blackboard; it never
asks which competition the task came from. Kept no-LLM so it is free to run on
every task even on a tight budget (a flash classifier can be slotted in later
behind the same `assess` method).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .contracts import Task
from .scheduler import _PRIORS


@dataclass
class Assessment:
    p_solve: float
    difficulty: str
    est_cost: float


class Triage:
    def __init__(self, bank=None, blackboard=None):
        self.bank = bank
        self.blackboard = blackboard

    def assess(self, task: Task) -> Assessment:
        p_solve, est_cost = _PRIORS.get(task.category.lower(), (0.4, 1.1))
        est_cost *= 1.0 + 0.2 * (len(task.files) > 2)

        # bank evidence: a high-similarity past solution in this category is
        # direct evidence the swarm can crack this kind of task -> raise p_solve.
        if self.bank is not None:
            try:
                hits = self.bank.retrieve(
                    f"{task.category} {task.name} {task.statement[:300]}",
                    category=task.category, k=1)
                if hits and hits[0].get("score", 0) >= 0.2:
                    p_solve = min(0.95, p_solve * (1.0 + 0.5 * hits[0]["score"]))
            except Exception:  # noqa: BLE001
                pass

        # negative memory: prior dead-ends on this exact task lower our estimate.
        if self.blackboard is not None:
            try:
                if self.blackboard.dead_ends(task.id):
                    p_solve *= 0.8
            except Exception:  # noqa: BLE001
                pass

        difficulty = self._difficulty(task)
        return Assessment(round(p_solve, 4), difficulty, round(est_cost, 4))

    @staticmethod
    def _difficulty(task: Task) -> str:
        hard = {"pwn", "reverse", "rev"}
        if task.category.lower() in hard:
            return "hard"
        volume = len(task.files) + len(task.statement) // 400
        if volume <= 1 and not task.has_service:
            return "low"           # little to work with -> conclude fast
        return "medium"
