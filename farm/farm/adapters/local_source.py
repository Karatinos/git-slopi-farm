"""Local-directory source adapter.

Each immediate subdirectory of `root` is one task: its statement is the longest
of description.txt / task.md / README.md / *.md (or the dir name if none), its
files are every other file staged into the sandbox, and an optional `gold` /
`flag.txt` sidecar provides a quarantined expected solution (never shown to the
agent — it is read here and removed from the staged files). Category is taken
from a `category` sidecar, else the parent directory name, else "misc".

Profile-neutral: the same raw records feed either the CTF or the generic profile.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

_STATEMENT_NAMES = ("description.txt", "task.md", "readme.md", "statement.txt", "task.txt")
_GOLD_NAMES = ("gold", "gold.txt", "flag.txt", "answer.txt", "expected.txt")


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return ""


class LocalSource:
    def __init__(self, root: str | Path, category_hint: Optional[str] = None):
        self.root = Path(root)
        self.category_hint = category_hint

    def read(self) -> List[dict]:
        out: List[dict] = []
        if not self.root.is_dir():
            return out
        for d in sorted(p for p in self.root.iterdir() if p.is_dir()):
            files, statement, gold, category = [], "", None, None
            for f in sorted(d.rglob("*")):
                if not f.is_file():
                    continue
                low = f.name.lower()
                if low in _GOLD_NAMES:
                    gold = _read(f).strip() or None
                    continue
                if low == "category":
                    category = _read(f).strip() or None
                    continue
                if low in _STATEMENT_NAMES and len(_read(f)) > len(statement):
                    statement = _read(f)
                    continue
                files.append((f, f.relative_to(d).as_posix()))
            out.append({
                "id": f"{self.root.name}/{d.name}", "name": d.name,
                "category": category or self.category_hint or self.root.name or "misc",
                "statement": statement or d.name, "files": files,
                "endpoint": "", "points": 1, "gold": gold, "extra": {}})
        return out
