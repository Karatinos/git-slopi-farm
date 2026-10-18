"""Observability: the KPIs the farm is steered by (blueprint §11.2).

Computes the metrics that matter on a live competition — cost-per-flag,
time-to-flag, solve-rate by category, escalation-rate — from a list of
`Outcome`s, and renders a compact Markdown report. Domain-agnostic: a "flag"
here is any accepted candidate, so the same report serves CTF and other
competitions.
"""
from __future__ import annotations

import statistics
from typing import Dict, List, Sequence

from .contracts import Grade, Outcome


def kpis(outcomes: Sequence[Outcome]) -> Dict[str, object]:
    n = len(outcomes)
    correct = [o for o in outcomes if o.correct]
    produced = [o for o in outcomes if o.solved]
    graded = [o for o in outcomes if o.grade in (Grade.CORRECT, Grade.INCORRECT)]
    spend = sum(o.cost_usd for o in outcomes)
    ttf = [o.wall_seconds for o in correct if o.wall_seconds]
    by_cat: Dict[str, List[int]] = {}
    for o in outcomes:
        c = by_cat.setdefault(o.category, [0, 0])
        c[1] += 1
        if o.correct:
            c[0] += 1
    return {
        "tasks": n,
        "correct": len(correct),
        "produced": len(produced),
        "graded": len(graded),
        "accuracy_on_graded": round(len(correct) / len(graded), 3) if graded else None,
        "spend_usd": round(spend, 4),
        "cost_per_flag_usd": round(spend / len(correct), 4) if correct else None,
        "median_time_to_flag_s": round(statistics.median(ttf), 1) if ttf else None,
        "escalation_rate": round(sum(o.escalated for o in outcomes) / n, 3) if n else 0,
        "by_category": {k: {"correct": v[0], "tasks": v[1]} for k, v in sorted(by_cat.items())},
    }


def render_markdown(outcomes: Sequence[Outcome], meta: Dict[str, object]) -> str:
    k = kpis(outcomes)
    lines = [f"# Farm run report — {meta.get('label', 'run')}", ""]
    lines.append(f"- profile: **{meta.get('profile', '?')}** · source: "
                 f"{meta.get('source', '?')} · provider: {meta.get('provider', '?')}")
    lines.append(f"- correct: **{k['correct']}/{k['tasks']}** "
                 f"(produced a candidate: {k['produced']}/{k['tasks']})")
    if k["accuracy_on_graded"] is not None:
        lines.append(f"- accuracy on graded: {k['accuracy_on_graded']:.0%}")
    lines.append(f"- spend: **${k['spend_usd']}**" + (
        f" · cost/flag: ${k['cost_per_flag_usd']}" if k["cost_per_flag_usd"] else ""))
    if k["median_time_to_flag_s"]:
        lines.append(f"- median time-to-flag: {k['median_time_to_flag_s']}s")
    lines.append(f"- escalation-rate (Flash→Pro): {k['escalation_rate']:.0%}")
    lines += ["", "## Solve-rate by category", "", "| category | correct | tasks |",
              "|---|---|---|"]
    for cat, v in k["by_category"].items():
        lines.append(f"| {cat} | {v['correct']} | {v['tasks']} |")
    lines += ["", "## Per-task", "", "| task | category | result | $ | s | tiers |",
              "|---|---|---|---|---|---|"]
    for o in outcomes:
        res = "✓correct" if o.correct else ("produced" if o.solved else "—")
        lines.append(f"| {o.name[:40]} | {o.category} | {res} | {o.cost_usd:.3f} "
                     f"| {o.wall_seconds:.0f} | {'·'.join(o.tiers)} |")
    return "\n".join(lines) + "\n"


def write_report(outcomes: Sequence[Outcome], meta: Dict[str, object], path) -> str:
    from pathlib import Path
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render_markdown(outcomes, meta), encoding="utf-8")
    return str(p)
