"""matplotlib charts for progress/metrics reports.

Kept theme-light and defensive; every function returns the output path so the
report can embed it, and failures degrade to a skipped chart rather than a crash.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_ACCENT = "#0f766e"
_MUTED = "#94a3b8"
_OK = "#16a34a"
_BAD = "#dc2626"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": "#cbd5e1",
                     "axes.grid": True, "grid.color": "#e2e8f0",
                     "figure.dpi": 150})


def solve_by_category(by_cat: Dict[str, Dict[str, int]], out: Path) -> Path:
    cats = list(by_cat.keys())
    total = [by_cat[c]["total"] for c in cats]
    solved = [by_cat[c]["solved"] for c in cats]
    fig, ax = plt.subplots(figsize=(7, 3))
    x = range(len(cats))
    ax.bar(x, total, color=_MUTED, label="всего")
    ax.bar(x, solved, color=_ACCENT, label="решено")
    ax.set_xticks(list(x)); ax.set_xticklabels(cats, rotation=30, ha="right")
    ax.set_ylabel("задач"); ax.set_title("Solve-rate по категориям")
    ax.legend(); fig.tight_layout(); fig.savefig(out); plt.close(fig)
    return out


def cost_per_task(pairs: List[tuple], out: Path) -> Path:
    """pairs: [(task_short, cost_usd, solved_bool), ...]"""
    pairs = sorted(pairs, key=lambda p: p[1], reverse=True)
    names = [p[0] for p in pairs]
    costs = [p[1] for p in pairs]
    colors = [_OK if p[2] else _BAD for p in pairs]
    fig, ax = plt.subplots(figsize=(7, max(3, len(names) * 0.22)))
    ax.barh(range(len(names)), costs, color=colors)
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names, fontsize=7)
    ax.invert_yaxis(); ax.set_xlabel("стоимость, $ (зелёный=решено)")
    ax.set_title("Стоимость на задачу")
    fig.tight_layout(); fig.savefig(out); plt.close(fig)
    return out


def kpi_donut(solve_rate: float, escalation_rate: float, out: Path) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.6))
    for ax, val, label, col in [
        (axes[0], solve_rate, "solve-rate", _ACCENT),
        (axes[1], escalation_rate, "escalation-rate", "#f59e0b")]:
        ax.pie([val, 1 - val], colors=[col, "#e2e8f0"], startangle=90,
               counterclock=False, wedgeprops={"width": 0.42})
        ax.text(0, 0, f"{val*100:.0f}%", ha="center", va="center",
                fontsize=15, color=col)
        ax.set_title(label)
    fig.tight_layout(); fig.savefig(out); plt.close(fig)
    return out


def time_per_task(pairs: List[tuple], out: Path) -> Path:
    """pairs: [(task_short, seconds, solved_bool), ...]"""
    pairs = sorted(pairs, key=lambda p: p[1], reverse=True)
    names = [p[0] for p in pairs]
    secs = [p[1] for p in pairs]
    cols = [_OK if p[2] else _BAD for p in pairs]
    fig, ax = plt.subplots(figsize=(7, max(3, len(names) * 0.22)))
    ax.barh(range(len(names)), secs, color=cols)
    ax.set_yticks(range(len(names))); ax.set_yticklabels(names, fontsize=7)
    ax.invert_yaxis(); ax.set_xlabel("время, с (зелёный=решено)")
    ax.set_title("Время на задачу")
    fig.tight_layout(); fig.savefig(out); plt.close(fig)
    return out


def cumulative_spend(costs: List[float], out: Path, cap: float = None) -> Path:
    running = []
    s = 0.0
    for c in costs:
        s += c
        running.append(s)
    fig, ax = plt.subplots(figsize=(7, 2.8))
    ax.plot(range(1, len(running) + 1), running, color=_ACCENT, marker="o", ms=3)
    if cap:
        ax.axhline(cap, color=_BAD, ls="--", lw=1, label=f"лимит ${cap:.2f}")
        ax.legend()
    ax.set_xlabel("задача №"); ax.set_ylabel("сумма, $")
    ax.set_title("Накопленные траты")
    fig.tight_layout(); fig.savefig(out); plt.close(fig)
    return out
