"""Local-directory source adapter (nested-layout aware).

Supports two directory shapes under `root`:
  * FLAT   — each immediate subdir of root is a task.
  * NESTED — root/<category>/<task>/... : a subdir whose own children are ALL
             directories is treated as a *category*, and its children as tasks.
             (This is the Кубок-Федерации CTF layout: category/taskname/files.)

A task's statement is the longest of description.txt / task.md / *.md (or the
dir name if none). Every other file is staged into the sandbox. A quarantined
gold solution comes from an optional sidecar (gold / flag.txt / ...) OR from an
injected answer-key (keyed by "<category>/<name>" or by name). The gold is read
HERE and never staged to the agent.

Task id is "<category>/<name>"; category is the parent dir (nested) else the
hint / root name. Profile-neutral: the same records feed ctf or generic.
"""
from __future__ import annotations

import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Union

_STATEMENT_NAMES = ("description.txt", "task.md", "readme.md", "statement.txt", "task.txt")
_GOLD_NAMES = ("gold", "gold.txt", "flag.txt", "answer.txt", "expected.txt")

GoldVal = Union[str, list, None]


_PDF_CAP = 4000  # chars of brief text to fold into the statement


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return ""


def _pdf_text(p: Path, cap: int = _PDF_CAP) -> str:
    """Best-effort text extraction from a brief PDF (pypdf). Never fatal."""
    try:
        from pypdf import PdfReader
        r = PdfReader(str(p))
        out = []
        for page in r.pages:
            out.append(page.extract_text() or "")
            if sum(len(x) for x in out) > cap:
                break
        txt = "\n".join(out).strip()
        return txt[:cap]
    except Exception:  # noqa: BLE001
        return ""


class LocalSource:
    def __init__(self, root: str | Path, category_hint: Optional[str] = None,
                 answer_key: Optional[Dict[str, GoldVal]] = None,
                 only: Optional[List[str]] = None):
        self.root = Path(root)
        self.category_hint = category_hint
        self.only = [unicodedata.normalize("NFC", o).casefold() for o in (only or [])]
        # Normalize keys to NFC so lookups survive macOS NFD filenames.
        self.answer_key = {unicodedata.normalize("NFC", k): v
                           for k, v in (answer_key or {}).items()}

    @staticmethod
    def _is_category_dir(d: Path) -> bool:
        kids = [p for p in d.iterdir() if not p.name.startswith(".")]
        return bool(kids) and all(p.is_dir() for p in kids)

    def _task_record(self, d: Path, category: str) -> dict:
        files: list = []
        statement = ""
        gold: GoldVal = None
        for f in sorted(d.rglob("*")):
            if not f.is_file() or f.name == ".DS_Store":
                continue
            low = f.name.lower()
            if low in _GOLD_NAMES and f.parent == d:      # quarantined sidecar
                gold = _read(f).strip() or None
                continue
            if low in _STATEMENT_NAMES and len(_read(f)) > len(statement):
                statement = _read(f)
                continue
            files.append((f, f.relative_to(d).as_posix()))

        if len(statement) < 40:                       # no real statement file
            pdfs = [hp for hp, _ in files if hp.suffix.lower() == ".pdf"]
            briefs = []
            for hp in pdfs:
                t = _pdf_text(hp)
                if t:
                    briefs.append(f"[from {hp.name}]\n{t}")
            if briefs:
                statement = "\n\n".join(briefs)[:_PDF_CAP * 2]

        tid = f"{category.lower()}/{d.name}"
        tid_n = unicodedata.normalize("NFC", tid)
        name_n = unicodedata.normalize("NFC", d.name)
        extra: Dict[str, object] = {}
        ak = self.answer_key.get(tid_n, self.answer_key.get(name_n))
        if isinstance(ak, list):
            extra["gold_any"] = ak
            if gold is None and ak:
                gold = ak[0]
        elif ak is not None and gold is None:
            gold = ak

        # SAFETY: never leak a known flag to the agent via the statement.
        golds = [g for g in ([gold] + (extra.get("gold_any") or [])) if g]
        import re as _re
        for g in set(golds):
            statement = statement.replace(g, "flag{REDACTED}")
            m = _re.match(r"^[A-Za-z0-9_]{1,32}\{(.+)\}$", g)
            if m:
                statement = statement.replace(m.group(1), "REDACTED")

        return {"id": tid, "name": d.name, "category": category.lower(),
                "statement": statement or d.name, "files": files,
                "endpoint": "", "points": 1, "gold": gold, "extra": extra}

    def read(self) -> List[dict]:
        out: List[dict] = []
        if not self.root.is_dir():
            return out
        children = sorted(p for p in self.root.iterdir()
                          if p.is_dir() and not p.name.startswith("."))
        for c in children:
            if self._is_category_dir(c):                  # NESTED: c is a category
                for t in sorted(p for p in c.iterdir()
                                if p.is_dir() and not p.name.startswith(".")):
                    out.append(self._task_record(t, c.name))
            else:                                         # FLAT: c is a task
                out.append(self._task_record(
                    c, self.category_hint or self.root.name or "misc"))
        if self.only:
            def _keep(r):
                hay = unicodedata.normalize("NFC", r["id"] + " " + r["name"]).casefold()
                return any(o in hay for o in self.only)
            out = [r for r in out if _keep(r)]
        return out
