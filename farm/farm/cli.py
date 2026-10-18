"""Unified farm CLI — one entrypoint for every competition.

    python -m farm.cli run --profile ctf     --source ctfd  [opts]
    python -m farm.cli run --profile ctf     --source local --path tasks/...
    python -m farm.cli run --profile generic --source local --path work-on/...
    python -m farm.cli profiles            # list registered profiles

There is no CTF-vs-other code path: `--profile` selects a strategy and
`--source` selects an input adapter; the Engine runs them identically.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
from pathlib import Path
from typing import List, Optional

from .config import DATA_DIR, SETTINGS
from .core import Engine, Outcome, available, build
from .observability.governor import BalanceGuard, deepseek_balance_fetcher
import farm.profiles  # noqa: F401  (register built-in profiles)

OUT = DATA_DIR / "runs"


def _build_engine(limit_usd: float, per_task_usd: float) -> Engine:
    # one undercount factor corrects the local price table so the real-time
    # estimate governor trips near the true billed limit.
    undercount = 1.9
    bud = dataclasses.replace(SETTINGS.budgets, per_task_usd_cap=per_task_usd,
                              max_usd=per_task_usd)
    settings = dataclasses.replace(SETTINGS, budgets=bud)
    eng = Engine(settings=settings, global_cap_usd=max(0.05, limit_usd / undercount))
    if eng.provider == "deepseek":
        fetch = deepseek_balance_fetcher(SETTINGS.deepseek_api_key, SETTINGS.deepseek_base_url)
        start = fetch()
        eng.gateway.balance_guard = BalanceGuard(
            fetch, floor_usd=start - limit_usd * 0.9, every_calls=2,
            estimate_fn=lambda: eng.governor.spent_usd,
            estimate_ceiling=max(0.05, limit_usd / undercount))
        eng._start_balance = start
    else:
        eng._start_balance = None
    return eng


def _source(args, profile):
    if args.source == "ctfd":
        from .adapters import CTFdSource
        src = CTFdSource(args.base_url, args.header, args.reg_code)
        if hasattr(profile, "submitter") or args.profile == "ctf":
            profile.submitter = src.submitter       # live grading
        return src
    from .adapters import LocalSource
    return LocalSource(args.path, category_hint=args.category_hint)


def _dump(outcomes: List[Outcome], label: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for o in outcomes:
        d = dataclasses.asdict(o)
        d["grade"] = o.grade.value
        d["value"] = o.value
        rows.append(d)
    p = OUT / f"outcomes_{label}.json"
    p.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def cmd_run(args) -> None:
    import farm.profiles  # ensure registration
    profile = build(args.profile, flag_format=args.flag_format) \
        if args.profile == "ctf" else build(args.profile)
    eng = _build_engine(args.limit, args.per_task)
    src = _source(args, profile)
    print(f"run={eng.run_id} provider={eng.provider} profile={args.profile} "
          f"source={args.source} limit=${args.limit:.2f}", flush=True)
    outcomes: List[Outcome] = []

    def on_result(o: Outcome) -> None:
        outcomes.append(o)
        mark = "✓CORRECT" if o.correct else ("produced" if o.solved else "—")
        print(f"  [{len(outcomes)}] {o.name[:40]:40} :: {mark} "
              f"${o.cost_usd:.3f} {o.wall_seconds:.0f}s {o.tiers} {o.error[:50]}", flush=True)
        _dump(outcomes, args.label)

    try:
        eng.run(profile, src, categories=args.categories, limit=args.max_tasks,
                offline_only=args.offline_only, on_result=on_result)
    finally:
        if hasattr(src, "close"):
            src.close()
    correct = sum(o.correct for o in outcomes)
    produced = sum(o.solved for o in outcomes)
    from .core.report import write_report
    meta = {"label": args.label, "profile": args.profile, "source": args.source,
            "provider": eng.provider}
    rep = write_report(outcomes, meta, OUT / f"report_{args.label}.md")
    print(f"DONE. correct {correct}/{len(outcomes)} produced {produced}/{len(outcomes)} "
          f"spent=${eng.governor.spent_usd:.3f}\n  data -> {_dump(outcomes, args.label)}"
          f"\n  report -> {rep}", flush=True)


def cmd_profiles(_args) -> None:
    print("registered profiles:", ", ".join(available()))


def main() -> None:
    ap = argparse.ArgumentParser(prog="farm")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="ingest + solve a competition")
    r.add_argument("--profile", default="ctf", help=f"one of: {', '.join(available()) or 'ctf, generic'}")
    r.add_argument("--source", choices=["ctfd", "local"], default="ctfd")
    r.add_argument("--path", default="", help="local source root (for --source local)")
    r.add_argument("--category-hint", default=None)
    r.add_argument("--flag-format", default="swarm{...}", help="CTF flag wrapper shown to the agent")
    r.add_argument("--limit", type=float, default=2.0, help="max REAL spend, USD")
    r.add_argument("--per-task", type=float, default=0.10)
    r.add_argument("--max-tasks", type=int, default=None)
    r.add_argument("--categories", nargs="*", default=None)
    r.add_argument("--offline-only", action="store_true", help="skip live-instance tasks")
    r.add_argument("--label", default="run")
    r.add_argument("--base-url", default="")
    r.add_argument("--header", default="")
    r.add_argument("--reg-code", default="")
    r.set_defaults(func=cmd_run)

    p = sub.add_parser("profiles", help="list registered profiles")
    p.set_defaults(func=cmd_profiles)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
