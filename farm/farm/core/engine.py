"""The Engine — composition root and end-to-end driver (blueprint §5–8).

Wires the five layers into one object and runs the pipeline for ANY profile:

    ingest → triage/priority → ensemble (sandboxed attempts) → verdict → submit

This single class replaces the old `Farm` / `GeneralFarm` / `live_ctf` trio.
It never branches on competition type: it holds the domain-agnostic machinery
(gateway+governor, sandbox provider, blackboard, ensemble, scheduler) and a
`Profile` supplies ingest, tools, prompts, verdict and submission.
"""
from __future__ import annotations

import uuid
from typing import Callable, List, Optional, Sequence

from ..config import SETTINGS, Settings
from ..gateway.client import ModelGateway
from ..memory.blackboard import Blackboard
from ..memory.solution_bank import SolutionBank
from ..memory.store import Store
from ..observability.governor import CostGovernor, KillSwitch
from ..sandbox.factory import make_provider
from .agent import ReActAgent
from .contracts import Grade, Outcome, Task
from .ensemble import Ensemble
from .profile import Profile
from .scheduler import Scheduler
from .triage import Triage


class Engine:
    def __init__(self, settings: Settings = SETTINGS,
                 global_cap_usd: Optional[float] = None):
        self.settings = settings
        self.run_id = uuid.uuid4().hex[:8]
        self.governor = CostGovernor(
            global_cap_usd=global_cap_usd or settings.budgets.global_usd_cap)
        self.gateway = ModelGateway(settings=settings, on_spend=self.governor.record)
        self.store = Store()
        self.blackboard = Blackboard(self.store)
        self.bank = SolutionBank(self.store)
        self.sandboxes = make_provider(settings.sandbox)
        self.agent = ReActAgent(self.gateway, self.blackboard,
                                budgets=settings.budgets, cascade=settings.cascade)
        self.ensemble = Ensemble(agent=self.agent, sandbox_provider=self.sandboxes,
                                 swarm=settings.swarm, enable_recon=settings.enable_recon)
        self.scheduler = Scheduler()
        self.triage = Triage(bank=self.bank, blackboard=self.blackboard)

    @property
    def provider(self) -> str:
        return self.gateway.provider_name

    def run(self, profile: Profile, source: object, *,
            categories: Optional[Sequence[str]] = None,
            limit: Optional[int] = None, offline_only: bool = False,
            on_result: Optional[Callable[[Outcome], None]] = None) -> List[Outcome]:
        """Ingest via the profile, schedule, then solve each task in priority
        order until the budget kill-switch trips. Returns one Outcome per task
        attempted."""
        self._apply_sandbox(profile)
        tasks = profile.ingest(source)
        for t in tasks:                              # triage → annotate for scheduler
            a = self.triage.assess(t)
            t.extra["p_solve"] = a.p_solve
            t.extra["est_cost"] = a.est_cost
            t.extra["difficulty"] = a.difficulty
        plan = self.scheduler.plan(tasks, categories=categories, limit=limit,
                                   offline_only=offline_only)
        outcomes: List[Outcome] = []
        for task in plan:
            try:
                self.governor.check()               # kill-switch before new spend
            except KillSwitch as e:
                oc = Outcome(id=task.id, name=task.name, category=task.category,
                             solved=False, grade=Grade.NONE, candidate=None,
                             correct=False, cost_usd=0.0, tokens=0, wall_seconds=0.0,
                             time_to_solve=None, escalated=False, n_attempts=0,
                             error=f"budget stop: {e}")
                outcomes.append(oc)
                if on_result:
                    on_result(oc)
                break
            oc = self.ensemble.solve(task, profile, fewshot=self._fewshot(task))
            self._feedback(task, oc)
            outcomes.append(oc)
            if on_result:
                on_result(oc)
        return outcomes

    def solve_one(self, profile: Profile, task: Task) -> Outcome:
        self._apply_sandbox(profile)
        self.governor.check()
        oc = self.ensemble.solve(task, profile, fewshot=self._fewshot(task))
        self._feedback(task, oc)
        return oc

    def _fewshot(self, task: Task) -> str:
        """RAG: retrieve demonstrations of similar past solutions (§10/§11.3) —
        the main API-mode growth lever. Query is the task text; category-scoped
        so it reinforces the per-category prefix. Never fatal."""
        try:
            return self.bank.render_fewshot(
                query=f"{task.category} {task.name} {task.statement[:400]}",
                category=task.category)
        except Exception:  # noqa: BLE001
            return ""

    def _apply_sandbox(self, profile: Profile) -> None:
        """Rebuild the sandbox provider from the profile's declared spec merged
        onto the base settings (isolated image, network policy, timeouts)."""
        spec = getattr(profile, "sandbox_spec", {}) or {}
        if not spec:
            return
        import dataclasses
        cfg = dataclasses.replace(self.settings.sandbox, **spec)
        self.ensemble.sandboxes = self.sandboxes = make_provider(cfg)

    def _feedback(self, task: Task, oc: Outcome) -> None:
        """Close the loop: successes seed the RAG bank (blueprint §10)."""
        self.store.set_task_status(task.id, "solved" if oc.solved else "failed")
        if oc.correct and oc.candidate:
            try:
                self.bank.add(category=task.category, title=task.name,
                              summary=f"solved ({oc.candidate.kind}) in {oc.wall_seconds:.0f}s",
                              template=oc.candidate.value[:400])
            except Exception:  # noqa: BLE001  (feedback must never break a run)
                pass

    def budget_snapshot(self) -> dict:
        return self.governor.snapshot()
