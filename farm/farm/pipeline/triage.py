"""Triage — the cheap first pass (blueprint §6, §8.2).

For every task, estimate the three numbers the scheduler needs: category,
difficulty, and p_solve (probability the swarm cracks it). The blueprint says
this is a fast, cheap pass — heuristics or a single Flash call — that feeds the
knapsack priority. We default to a deterministic heuristic (free, offline) and
allow an optional single Flash call to refine it.

The p_solve base rates come straight from the "реалистичные ожидания" table:
web/forensics/misc are the swarm's strong side, pwn/advanced-crypto are the
hard tail that mostly stays with humans.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

from ..gateway.client import ModelGateway

# base solve probability by category (strong side high, hard tail low)
_P_BY_CATEGORY = {
    "web": 0.70, "forensic": 0.65, "forensics": 0.65, "misc": 0.60,
    "osint": 0.45, "crypto": 0.45, "reverse": 0.40, "pentest": 0.40,
    "pwn": 0.25,
}
_DIFFICULTY_MULT = {"easy": 1.25, "medium": 1.0, "hard": 0.6, "unknown": 0.9}

# very light keyword classifier (used when category is genuinely unknown)
_KEYWORDS = {
    "web": ["http", "sql", "xss", "cookie", "jwt", "ssrf", "сайт", "сервис", "url"],
    "crypto": ["rsa", "aes", "шифр", "gost", "ключ", "encrypt", "хеш", "lattice"],
    "pwn": ["overflow", "rop", "heap", "libc", "pwntools", "exploit", "gadget"],
    "reverse": ["ida", "ghidra", "disassemb", "бинар", "pe32", "elf", ".exe"],
    "forensic": ["pcap", "wireshark", "dump", "volatility", "memory", "трафик"],
    "osint": ["osint", "разведк", "геолокац", "coordinates", "профил"],
    "misc": [],
}


@dataclass
class TriageResult:
    category: str
    difficulty: str
    p_solve: float
    source: str  # 'heuristic' | 'flash'


def _classify_category(text: str, fallback: str) -> str:
    low = text.lower()
    best, best_hits = fallback, 0
    for cat, kws in _KEYWORDS.items():
        hits = sum(1 for k in kws if k in low)
        if hits > best_hits:
            best, best_hits = cat, hits
    return best if best_hits >= 2 else fallback


def _estimate_difficulty(category: str, n_materials: int, text_len: int) -> str:
    if category in ("pwn",):
        return "hard"
    if category in ("reverse", "crypto") and n_materials > 5:
        return "hard"
    if text_len < 1200 and n_materials <= 2:
        return "easy"
    return "medium"


def heuristic_triage(*, category_hint: str, description: str,
                     n_materials: int) -> TriageResult:
    cat = _classify_category(description, category_hint)
    diff = _estimate_difficulty(cat, n_materials, len(description))
    base = _P_BY_CATEGORY.get(cat, 0.4)
    p = round(min(0.95, base * _DIFFICULTY_MULT.get(diff, 0.9)), 3)
    return TriageResult(category=cat, difficulty=diff, p_solve=p, source="heuristic")


def flash_triage(gateway: ModelGateway, *, category_hint: str,
                 description: str, n_materials: int) -> TriageResult:
    """Optional single Flash call to refine the heuristic (kept tiny)."""
    sys = ("You are a CTF triage classifier. Reply with STRICT JSON: "
           '{"category": one of [web,crypto,pwn,reverse,forensic,osint,misc,pentest],'
           ' "difficulty": one of [easy,medium,hard], "p_solve": 0..1 float}. '
           "No prose.")
    user = f"Category hint: {category_hint}\nMaterials: {n_materials}\n" \
           f"Description:\n{description[:1500]}"
    try:
        resp = gateway.chat(
            messages=[{"role": "system", "content": sys},
                      {"role": "user", "content": user}],
            tier="flash", temperature=0.0, max_tokens=120)
        data = json.loads(_extract_json(resp.text))
        return TriageResult(category=data.get("category", category_hint),
                            difficulty=data.get("difficulty", "medium"),
                            p_solve=float(data.get("p_solve", 0.4)),
                            source="flash")
    except Exception:  # noqa: BLE001 - fall back gracefully
        return heuristic_triage(category_hint=category_hint,
                                description=description, n_materials=n_materials)


def _extract_json(text: str) -> str:
    i, j = text.find("{"), text.rfind("}")
    return text[i:j + 1] if 0 <= i < j else "{}"
