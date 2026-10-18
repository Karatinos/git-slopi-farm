"""Verification & submission gate (blueprint §6 "staged validation").

Deterministic, no-LLM checks between an agent proposing a flag and it counting:
  * format validation against the task's flag regex,
  * dedup — never submit the same flag twice (avoids penalty resubmits),
  * grading against the quarantined gold set for offline evaluation.

Grading is exact on the flag body but tolerant of the `flag{` prefix case
(this CTF mixes `flag{}` and `FLAG{}`). Tasks whose only gold is a per-instance
template (random suffix) are reported as 'ungradable' rather than wrong.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional, Set

from ..config import SETTINGS
from ..memory.store import Store

_FLAG_ANY = re.compile(r"(?i:[a-z0-9_]{2,32})\{[^}\n]{1,200}\}")

# A complete flag is NAME{...} and always ENDS WITH '}'. These two regexes let
# canonicalize_flag() (a) trim a well-formed span out of surrounding prose / a
# doubled "}}}" tail, and (b) recover a flag the model left unterminated.
_FLAG_SPAN = re.compile(r"[A-Za-z0-9_]{1,32}\{[^}\n]{1,300}\}")
_FLAG_OPEN = re.compile(r"[A-Za-z0-9_]{1,32}\{[^{}\n]{1,300}$")
_LABEL = re.compile(r"(?is)^.*?\bflags?\b\s*(?:is|are|=|:)\s*")


def canonicalize_flag(raw: str, flag_format: Optional[str] = None) -> str:
    """Return the clean flag: exactly NAME{...} ending at a single '}'.

    Point-1 guarantee — a flag ALWAYS ends with '}'. This
      * strips surrounding quotes/backticks/fences and "the flag is:" labels,
      * collapses an over-closed tail (``swarm{x}}}`` -> ``swarm{x}``) and drops
        any prose after the closing brace,
      * recovers an unterminated flag the model got cut off on
        (``swarm{x_y_z`` -> ``swarm{x_y_z}``).
    It never invents a wrapper and is a no-op on already-clean input, so it is
    safe to run on every submission. Universal: works for any NAME{...} format.
    """
    if not raw:
        return raw
    s = raw.strip().strip("`").strip()
    s = s.strip("'\" ").strip()
    if re.search(r"(?i)\bflags?\b\s*(?:is|are|=|:)", s):
        s = _LABEL.sub("", s).strip().strip("`'\" ").strip()
    spans = list(_FLAG_SPAN.finditer(s))
    if spans:
        # the last complete span is the model's final answer; the regex stops at
        # the FIRST '}', so a "}}}" tail is trimmed to one brace automatically.
        return spans[-1].group(0)
    if "{" in s and "}" not in s:
        mo = _FLAG_OPEN.search(s)
        if mo:                       # opened but never closed -> terminate it
            return mo.group(0).rstrip() + "}"
    return s


def normalize(flag: str) -> str:
    flag = flag.strip().strip("`'\" ")
    # case-fold only the prefix before '{'
    if "{" in flag:
        pre, rest = flag.split("{", 1)
        return pre.lower() + "{" + rest
    return flag.lower()


def looks_like_flag(text: str, patterns=SETTINGS.flag_patterns) -> Optional[str]:
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(0)
    m = _FLAG_ANY.search(text)
    return m.group(0) if m else None


@dataclass
class VerdictLog:
    submitted: List[str] = field(default_factory=list)
    tried: Set[str] = field(default_factory=set)


class Verifier:
    def __init__(self, store: Store):
        self.store = store

    def valid_format(self, flag: str) -> bool:
        return looks_like_flag(flag) is not None

    def is_duplicate(self, log: VerdictLog, flag: str) -> bool:
        return normalize(flag) in log.tried

    def register(self, log: VerdictLog, flag: str) -> None:
        log.tried.add(normalize(flag))
        log.submitted.append(flag)

    def grade(self, task_id: str, flag: str) -> str:
        """Return 'correct' | 'incorrect' | 'ungradable'."""
        gold = self.store.gold_flags(task_id)
        if not gold:
            return "ungradable"
        nf = normalize(flag)
        gold_norm = {normalize(g) for g in gold}
        if nf in gold_norm:
            return "correct"
        # tolerate templated gold (random suffix): prefix match up to '<' or '{'
        for g in gold:
            gn = normalize(g)
            if "<" in gn:
                prefix = gn.split("<", 1)[0]
                if len(prefix) > 10 and nf.startswith(prefix):
                    return "correct"
        return "incorrect"
