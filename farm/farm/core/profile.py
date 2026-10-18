"""The Profile abstraction and registry — the farm's extensibility seam.

A `Profile` is everything that makes one *kind* of competition different from
another, expressed as a strategy object the engine calls polymorphically. The
engine (scheduler, ensemble, ReAct loop, budgets, blackboard, observability) is
written once and never branches on the competition type; to support a new kind
of contest you register a new Profile — no engine edits, no `if`.

A Profile answers five questions, nothing more:

  1. ingest(source)         -> how do raw inputs become normalised Tasks?
  2. toolset(task)          -> which tools (incl. the terminal one) does the
                               agent get, and how is a terminal call turned into
                               a Candidate?
  3. system_prompt(task)    -> the stable, cache-friendly role/doctrine prefix.
  4. verdict(task, cand)    -> is a Candidate correct? (offline oracle)
  5. submit(task, cand)     -> optional external submission (e.g. a live
                               scoreboard) returning the authoritative verdict.

Defaults are provided so a minimal Profile only overrides what it needs.
"""
from __future__ import annotations

from typing import Callable, Dict, List, Optional, Protocol, Sequence, runtime_checkable

from .contracts import Candidate, Grade, Task, Verdict
from .toolset import ToolSet


@runtime_checkable
class Profile(Protocol):
    """Strategy object for one competition family. Implemented by duck-typing;
    `BaseProfile` gives sane defaults for everything except `ingest`."""

    name: str

    def ingest(self, source: object) -> List[Task]:
        """Normalise a source (a directory, a scoreboard client, a list…) into
        Tasks. The only method with no universal default."""
        ...

    def toolset(self, task: Task) -> ToolSet:
        """Tools available to the agent for this task, including the terminal
        tool and the function that extracts a Candidate from a fired terminal."""
        ...

    def system_prompt(self, task: Task) -> str:
        """Stable per-(profile, category) system prefix (safe for prefix-cache)."""
        ...

    def verdict(self, task: Task, candidate: Candidate) -> Verdict:
        """Offline judgement against any known oracle (gold / checker)."""
        ...

    def submit(self, task: Task, candidate: Candidate) -> Optional[Verdict]:
        """Submit to an external authority if one exists; else None."""
        ...

    def normalize(self, candidate: Candidate, task: Task) -> Candidate:
        """Clean a candidate into its canonical form before judging/submitting."""
        ...


class BaseProfile:
    """Convenience base: implement `ingest` + `toolset` + `system_prompt`, and
    override `verdict`/`submit`/`normalize` only when the domain needs them."""

    name: str = "base"
    # Sandbox overrides the engine merges onto SETTINGS.sandbox for this profile
    # (image/toolchain, network policy, per-tool timeout). Read uniformly by the
    # engine — a profile declaring its isolation needs, not an engine branch.
    sandbox_spec: Dict[str, object] = {}

    def ingest(self, source: object) -> List[Task]:  # pragma: no cover - abstract
        raise NotImplementedError

    def toolset(self, task: Task) -> ToolSet:  # pragma: no cover - abstract
        raise NotImplementedError

    def system_prompt(self, task: Task) -> str:  # pragma: no cover - abstract
        raise NotImplementedError

    def normalize(self, candidate: Candidate, task: Task) -> Candidate:
        return candidate

    def verdict(self, task: Task, candidate: Candidate) -> Verdict:
        # No oracle by default: a produced candidate is ungraded (honest), an
        # empty one is none.
        if candidate and candidate.value.strip():
            return Verdict(Grade.UNGRADED, "no offline oracle", candidate.value)
        return Verdict(Grade.NONE, "empty")

    def submit(self, task: Task, candidate: Candidate) -> Optional[Verdict]:
        return None


# --------------------------------------------------------------------------- #
# Registry — profiles register themselves by name; the CLI/engine look them up.
# --------------------------------------------------------------------------- #
_REGISTRY: Dict[str, Callable[..., Profile]] = {}


def register(name: str):
    """Decorator: register a Profile factory under `name`."""
    def deco(factory: Callable[..., Profile]) -> Callable[..., Profile]:
        _REGISTRY[name] = factory
        return factory
    return deco


def build(name: str, **kwargs) -> Profile:
    if name not in _REGISTRY:
        raise KeyError(f"unknown profile '{name}'; known: {sorted(_REGISTRY)}")
    return _REGISTRY[name](**kwargs)


def available() -> Sequence[str]:
    return sorted(_REGISTRY)
