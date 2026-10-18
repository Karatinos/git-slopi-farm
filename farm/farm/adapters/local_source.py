"""Local-directory source adapter (nested-layout + benchmark-integrity aware).

Directory shapes under `root`:
  * FLAT   — each immediate subdir of root is a task.
  * NESTED — root/<category>/<task>/... (the Кубок-Федерации CTF layout).

BENCHMARK INTEGRITY. The Кубок tasks ship as *разбор* (writeup) decks plus
solution scripts, so the raw folders leak the flag. To keep a run a real test of
solving ability (not grep-the-answer), this adapter:
  * takes the statement from PAGE 1 ONLY of a task PDF (the title/problem slide),
    not the solution slides, and REDACTS any known flag from it;
  * QUARANTINES (never stages to the agent) every file that is a solution — by
    name (writeup/solve/solver/unpack/exploit/attack/разбор) or because its text
    contains a known gold flag (checked for .md/.txt/.py/.json/.c/.cpp/.h and
    .pdf via pypdf).
Quarantined paths are recorded on `self.quarantined` for reporting. Gold itself
comes from an injected answer-key (keyed by "<category>/<name>" or name), read
here and never staged.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Union

_STATEMENT_NAMES = ("description.txt", "task.md", "readme.md", "statement.txt", "task.txt")
_GOLD_NAMES = ("gold", "gold.txt", "flag.txt", "answer.txt", "expected.txt")
_SOLUTION_PAT = re.compile(
    r"(w[rt]ite[\s_-]?up|writeup|solve|solver|unpack|exploit|attack|разбор|"
    r"_sol\b|solution|reference|unseal|gen_cert)",
    re.IGNORECASE)
_TEXTY = (".md", ".txt", ".py", ".json", ".c", ".cpp", ".h", ".html", ".csv",
          ".cfg", ".ini", ".log", ".yaml", ".yml")
_PDF_CAP = 4000

GoldVal = Union[str, list, None]


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return ""


def _pdf_text(p: Path, pages: Optional[int] = None, cap: int = _PDF_CAP) -> str:
    try:
        from pypdf import PdfReader
        r = PdfReader(str(p))
        pp = r.pages if pages is None else r.pages[:pages]
        out = []
        for page in pp:
            out.append(page.extract_text() or "")
            if sum(len(x) for x in out) > cap:
                break
        return "\n".join(out).strip()[:cap]
    except Exception:  # noqa: BLE001
        return ""


def _file_text(p: Path) -> str:
    low = p.suffix.lower()
    if low == ".pdf":
        return _pdf_text(p)
    if low in _TEXTY:
        return _read(p)
    return ""


def _full_text(p: Path) -> str:
    """Uncapped text for gold-leak detection (ALL pdf pages / whole text file)."""
    low = p.suffix.lower()
    if low == ".pdf":
        try:
            from pypdf import PdfReader
            return "\n".join((pg.extract_text() or "") for pg in PdfReader(str(p)).pages)
        except Exception:  # noqa: BLE001
            return ""
    if low in _TEXTY:
        return _read(p)
    return ""


class LocalSource:
    def __init__(self, root: str | Path, category_hint: Optional[str] = None,
                 answer_key: Optional[Dict[str, GoldVal]] = None,
                 only: Optional[List[str]] = None):
        self.root = Path(root)
        self.category_hint = category_hint
        self.answer_key = {unicodedata.normalize("NFC", k): v
                           for k, v in (answer_key or {}).items()}
        self.only = [unicodedata.normalize("NFC", o).casefold() for o in (only or [])]
        self.quarantined: List[str] = []       # solution files withheld from agents

    @staticmethod
    def _is_category_dir(d: Path) -> bool:
        kids = [p for p in d.iterdir() if not p.name.startswith(".")]
        return bool(kids) and all(p.is_dir() for p in kids)

    def _golds(self, tid: str, name: str):
        ak = self.answer_key.get(unicodedata.normalize("NFC", tid),
                                 self.answer_key.get(unicodedata.normalize("NFC", name)))
        if isinstance(ak, list):
            return ak[0] if ak else None, list(ak)
        return ak, ([ak] if ak else [])

    def _redact(self, text: str, golds: List[str]) -> str:
        for g in set(g for g in golds if g):
            text = text.replace(g, "flag{REDACTED}")
            m = re.match(r"^[A-Za-z0-9_]{1,32}\{(.+)\}$", g)
            if m:
                text = text.replace(m.group(1), "REDACTED")
        return text

    def _task_record(self, d: Path, category: str) -> dict:
        tid = f"{category.lower()}/{d.name}"
        gold, golds = self._golds(tid, d.name)
        extra: Dict[str, object] = {}
        if len(golds) > 1:
            extra["gold_any"] = golds

        files: list = []
        statement = ""
        stmt_pdf = ""
        for f in sorted(d.rglob("*")):
            if not f.is_file() or f.name == ".DS_Store":
                continue
            low = f.name.lower()
            if low in _GOLD_NAMES and f.parent == d:          # quarantined sidecar
                if gold is None:
                    gold = _read(f).strip() or None
                    if gold:
                        golds = [gold]
                continue
            if low in _STATEMENT_NAMES and len(_read(f)) > len(statement):
                statement = _read(f)
                continue
            # decide: is this a solution file to quarantine? (full-text gold scan)
            rel = f.relative_to(d).as_posix()
            is_solution = bool(_SOLUTION_PAT.search(rel)) or \
                any(g and g in _full_text(f) for g in golds)
            if is_solution:
                self.quarantined.append(f.relative_to(self.root).as_posix())
                # still mine a PDF's PAGE 1 for the problem statement (title slide)
                if f.suffix.lower() == ".pdf" and len(stmt_pdf) < 40:
                    stmt_pdf = _pdf_text(f, pages=1)
                continue
            files.append((f, f.relative_to(d).as_posix()))
            if f.suffix.lower() == ".pdf" and len(stmt_pdf) < 40:
                stmt_pdf = _pdf_text(f, pages=1)

        if len(statement) < 40 and stmt_pdf:
            statement = stmt_pdf
        statement = self._redact(statement or d.name, golds)

        return {"id": tid, "name": d.name, "category": category.lower(),
                "statement": statement, "files": files,
                "endpoint": "", "points": 1, "gold": gold, "extra": extra}

    def read(self) -> List[dict]:
        out: List[dict] = []
        if not self.root.is_dir():
            return out
        children = sorted(p for p in self.root.iterdir()
                          if p.is_dir() and not p.name.startswith("."))
        for c in children:
            if self._is_category_dir(c):
                for t in sorted(p for p in c.iterdir()
                                if p.is_dir() and not p.name.startswith(".")):
                    out.append(self._task_record(t, c.name))
            else:
                out.append(self._task_record(
                    c, self.category_hint or self.root.name or "misc"))
        if self.only:
            def _keep(r):
                hay = unicodedata.normalize("NFC", r["id"] + " " + r["name"]).casefold()
                return any(o in hay for o in self.only)
            out = [r for r in out if _keep(r)]
        return out
