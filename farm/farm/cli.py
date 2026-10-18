"""Unified farm CLI — one engine, selectable strategy (prototype).

    python -m farm.cli run --source local --path <dir> --prototype p1
    python -m farm.cli run --source local --path <dir> --prototype p3 --limit 2.0
    python -m farm.cli profiles

A prototype is a reproducible bundle of strategy knobs on ONE engine (a fair
A/B): p1 single ReAct · p2 ensemble · p3 cascade(Flash->Pro)+recon ·
p4 cascade+recon+adaptive. Explicit flags override the bundle.
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
ANSWER_KEY = DATA_DIR / "answer_key.json"

_PROTOTYPES = {
    # ensemble, escalate(Flash->Pro), recon, adaptive_effort
    "p1": dict(ensemble=1, escalate=False, recon=False, adaptive=False),
    "p2": dict(ensemble=4, escalate=False, recon=False, adaptive=False),
    "p3": dict(ensemble=3, escalate=True,  recon=True,  adaptive=False),
    "p4": dict(ensemble=4, escalate=True,  recon=True,  adaptive=True),
}
_DEFAULTS = dict(ensemble=4, escalate=True, recon=False, adaptive=False)


def _apply_prototype(args) -> None:
    bundle = _PROTOTYPES.get(args.prototype or "", {})
    for k in ("ensemble", "escalate", "recon", "adaptive"):
        if getattr(args, k) is None:
            setattr(args, k, bundle.get(k, _DEFAULTS[k]))


def _settings_from_args(args):
    s = SETTINGS
    bud = dataclasses.replace(s.budgets, per_task_usd_cap=args.per_task,
                              max_usd=args.per_task)
    conc = max(1, min(args.ensemble, s.swarm.max_concurrent_sandboxes))
    swarm = dataclasses.replace(s.swarm, ensemble_size=max(1, args.ensemble),
                                adaptive_effort=bool(args.adaptive),
                                max_concurrent_sandboxes=conc)
    casc = dataclasses.replace(s.cascade, enabled=bool(args.escalate))
    return dataclasses.replace(s, budgets=bud, swarm=swarm, cascade=casc,
                               enable_recon=bool(args.recon))


def _load_answer_key(path=None) -> dict:
    p = Path(path) if path else ANSWER_KEY
    try:
        return json.loads(p.read_text(encoding="utf-8")).get("flags", {})
    except Exception:  # noqa: BLE001
        return {}


def _build_engine(settings, limit_usd: float) -> Engine:
    is_or = "openrouter" in (settings.deepseek_base_url or "").lower()
    # OpenRouter returns exact per-call cost -> governor is exact, cap == limit.
    # Native DeepSeek price table under-counts -> keep the historical margin.
    undercount = 1.0 if is_or else 1.9
    eng = Engine(settings=settings, global_cap_usd=max(0.05, limit_usd / undercount))
    eng._start_balance = None
    # Real-balance guard only makes sense for native DeepSeek; OpenRouter has no
    # /user/balance and its usage.cost already makes the governor exact.
    if eng.provider == "deepseek" and not is_or and settings.deepseek_api_key:
        try:
            fetch = deepseek_balance_fetcher(settings.deepseek_api_key,
                                             settings.deepseek_base_url)
            start = fetch()
            eng.gateway.balance_guard = BalanceGuard(
                fetch, floor_usd=start - limit_usd * 0.9, every_calls=2,
                estimate_fn=lambda: eng.governor.spent_usd,
                estimate_ceiling=max(0.05, limit_usd / undercount))
            eng._start_balance = start
        except Exception as e:  # noqa: BLE001
            print(f"  [warn] balance guard unavailable ({e}); estimate-only governor",
                  flush=True)
    return eng


def _source(args, profile):
    if args.source == "ctfd":
        from .adapters import CTFdSource
        src = CTFdSource(args.base_url, args.header, args.reg_code)
        if hasattr(profile, "submitter") or args.profile == "ctf":
            profile.submitter = src.submitter
        return src
    from .adapters import LocalSource
    return LocalSource(args.path, category_hint=args.category_hint,
                       answer_key=_load_answer_key(getattr(args, "answer_key", None)),
                       only=args.only)


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
    _apply_prototype(args)
    settings = _settings_from_args(args)
    profile = build(args.profile, flag_format=args.flag_format) \
        if args.profile == "ctf" else build(args.profile)
    eng = _build_engine(settings, args.limit)
    src = _source(args, profile)
    print(f"run={eng.run_id} provider={eng.provider} profile={args.profile} "
          f"source={args.source} prototype={args.prototype or 'custom'} "
          f"ensemble={args.ensemble} escalate={args.escalate} recon={args.recon} "
          f"adaptive={args.adaptive} limit=${args.limit:.2f} cap=${eng.governor.global_cap_usd:.2f}",
          flush=True)
    outcomes: List[Outcome] = []

    def on_result(o: Outcome) -> None:
        outcomes.append(o)
        mark = "✓CORRECT" if o.correct else ("produced" if o.solved else "—")
        print(f"  [{len(outcomes)}] {o.name[:34]:34} :: {mark:9} "
              f"${o.cost_usd:.4f} {o.wall_seconds:4.0f}s {o.tiers} {o.error[:45]}",
              flush=True)
        _dump(outcomes, args.label)

    try:
        eng.run(profile, src, categories=args.categories, limit=args.max_tasks,
                offline_only=args.offline_only, on_result=on_result)
    finally:
        if hasattr(src, "close"):
            src.close()
    correct = sum(o.correct for o in outcomes)
    produced = sum(o.solved for o in outcomes)
    gradable = sum(1 for o in outcomes if o.grade.value in ("correct", "incorrect"))
    from .core.report import write_report
    meta = {"label": args.label, "profile": args.profile, "source": args.source,
            "provider": eng.provider, "prototype": args.prototype or "custom",
            "ensemble": args.ensemble, "escalate": args.escalate,
            "recon": args.recon, "adaptive": args.adaptive}
    rep = write_report(outcomes, meta, OUT / f"report_{args.label}.md")
    sr = (correct / gradable) if gradable else 0.0
    cpf = (eng.governor.spent_usd / correct) if correct else float("nan")
    print(f"DONE. correct {correct}/{gradable} (solve-rate {sr:.0%}) "
          f"produced {produced}/{len(outcomes)} spent=${eng.governor.spent_usd:.4f} "
          f"cost/flag=${cpf:.4f}\n  data -> {_dump(outcomes, args.label)}\n  report -> {rep}",
          flush=True)


def cmd_profiles(_args) -> None:
    print("registered profiles:", ", ".join(available()))


def main() -> None:
    ap = argparse.ArgumentParser(prog="farm")
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="ingest + solve a competition")
    r.add_argument("--profile", default="ctf",
                   help=f"one of: {', '.join(available()) or 'ctf, generic'}")
    r.add_argument("--source", choices=["ctfd", "local"], default="local")
    r.add_argument("--path", default="", help="local source root (for --source local)")
    r.add_argument("--category-hint", default=None)
    r.add_argument("--flag-format", default="flag{...}",
                   help="CTF flag wrapper shown to the agent")
    # strategy: prototype bundle + explicit overrides
    r.add_argument("--prototype", choices=list(_PROTOTYPES), default=None,
                   help="p1 single | p2 ensemble | p3 cascade+recon | p4 +adaptive")
    r.add_argument("--ensemble", type=int, default=None, help="parallel attempts/task")
    r.add_argument("--escalate", action=argparse.BooleanOptionalAction, default=None,
                   help="allow Flash->Pro escalation on stall")
    r.add_argument("--recon", action=argparse.BooleanOptionalAction, default=None,
                   help="auto file/exif/OCR recon before solving")
    r.add_argument("--adaptive", action=argparse.BooleanOptionalAction, default=None,
                   help="adaptive effort: conclude fast on low-signal tasks")
    # budgets
    r.add_argument("--limit", type=float, default=2.0, help="max REAL spend, USD (hard cap)")
    r.add_argument("--per-task", type=float, default=0.25, help="per-task USD cap")
    r.add_argument("--max-tasks", type=int, default=None)
    r.add_argument("--categories", nargs="*", default=None)
    r.add_argument("--only", nargs="*", default=None,
                   help="keep only tasks whose id/name contains any substring")
    r.add_argument("--answer-key", default=None,
                   help="path to an answer-key json (default data/answer_key.json)")
    r.add_argument("--offline-only", action="store_true", help="skip live-instance tasks")
    r.add_argument("--label", default=None)
    r.add_argument("--base-url", default="")
    r.add_argument("--header", default="")
    r.add_argument("--reg-code", default="")
    r.set_defaults(func=cmd_run)

    p = sub.add_parser("profiles", help="list registered profiles")
    p.set_defaults(func=cmd_profiles)

    args = ap.parse_args()
    if getattr(args, "label", None) is None and hasattr(args, "prototype"):
        args.label = args.prototype or "custom"
    args.func(args)


if __name__ == "__main__":
    main()
