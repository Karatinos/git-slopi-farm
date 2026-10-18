"""Domain-agnostic contracts shared by the whole farm.

These are the ONLY data types the orchestration engine knows about. The engine
never asks "is this a CTF task or something else?" — it speaks `Task`,
`Candidate`, `Verdict`, `Outcome`, and a `Profile` (see `profile.py`) supplies
every domain-specific behaviour behind those types. That is what removes the
`if ctf: … else: …` branching the old `farm`/`general_farm` split was built on.

A `Task` is any unit of work with a success signal:
  * a CTF challenge whose success is "the flag was accepted", or
  * a competitive-programming / data / math task whose success is "the produced
    answer matches the checker".
The engine treats them identically; only the `Profile` differs.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Grade(str, Enum):
    """Outcome of judging a candidate. Deliberately small and universal."""
    CORRECT = "correct"        # verified success (gold match / remote accept / checker pass)
    INCORRECT = "incorrect"    # verified failure
    UNGRADED = "ungraded"      # produced, but no oracle available to judge it offline
    NONE = "none"              # nothing was produced


@dataclass
class Task:
    """A unit of work, normalised from any source by a Profile's ingester.

    `files` are (host_path, arcname) pairs staged into the sandbox. `endpoint`
    is a live service/instance target (host:port or URL) when the task is not
    (only) file-based — this is what makes the farm handle instances and files
    through the same path. `answer_format` is the expected shape of a solution
    (a flag format like `swarm{...}`, or an output spec); it is advice to the
    agent, never a branch in the engine. `extra` carries profile-private data
    (e.g. a CTFd challenge id) the engine passes through untouched.
    """
    id: str
    name: str
    category: str
    statement: str
    files: List[Tuple[Path, str]] = field(default_factory=list)
    endpoint: str = ""
    answer_format: str = ""
    points: float = 1.0
    deadline_ts: Optional[float] = None
    gold: Optional[str] = None                      # known solution (benchmark only; quarantined)
    extra: Dict[str, object] = field(default_factory=dict)

    @property
    def has_service(self) -> bool:
        return bool(self.endpoint)

    @property
    def actionable(self) -> bool:
        """Something concrete to work on — files to analyse or a live target.
        The scheduler drops only tasks that are neither."""
        return bool(self.files) or self.has_service


@dataclass
class Candidate:
    """A proposed solution an attempt produced: a flag, an answer string, or a
    program's source. `kind` lets a Profile's verdict/submit treat it correctly
    without the engine knowing what the kinds mean."""
    value: str
    kind: str = "flag"                              # flag | answer | program | ...
    meta: Dict[str, object] = field(default_factory=dict)


@dataclass
class Verdict:
    """A Profile's judgement of a candidate."""
    grade: Grade
    detail: str = ""
    canonical: Optional[str] = None                 # normalised candidate actually judged


@dataclass
class AttemptResult:
    """One ensemble member's trajectory."""
    task_id: str
    author: str
    outcome: str                                    # solved | failed | stalled | killed | error
    candidate: Optional[Candidate] = None
    accepted: bool = False                          # terminal verdict was CORRECT
    steps: int = 0
    tokens: int = 0
    cost_usd: float = 0.0
    tier_path: str = "flash"
    trace_id: str = ""
    reason: str = ""
    tools_used: Dict[str, int] = field(default_factory=dict)


@dataclass
class Outcome:
    """The engine's per-task result, profile-independent."""
    id: str
    name: str
    category: str
    solved: bool                                    # a candidate was accepted/produced
    grade: Grade
    candidate: Optional[Candidate]
    correct: bool
    cost_usd: float
    tokens: int
    wall_seconds: float
    time_to_solve: Optional[float]
    escalated: bool
    n_attempts: int
    tiers: List[str] = field(default_factory=list)
    error: str = ""

    @property
    def value(self) -> Optional[str]:
        return self.candidate.value if self.candidate else None
