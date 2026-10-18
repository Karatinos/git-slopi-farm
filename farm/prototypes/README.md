# Farm prototypes — one engine, four strategies

All prototypes are the SAME engine (gateway→OpenRouter, ensemble, ephemeral
sandbox, ReAct agent, cost governor) differing only in a bundle of strategy
knobs. This is a fair A/B: identical harness, identical tasks, one variable set.

Select with `--prototype`; explicit flags override the bundle.

| Proto | ensemble | Flash→Pro escalate | recon | adaptive | thesis it tests |
|-------|----------|--------------------|-------|----------|-----------------|
| **p1** | 1 | off | off | off | baseline: a single Flash ReAct agent |
| **p2** | 4 | off | off | off | diversity: does a parallel Flash ensemble + first-to-flag beat p1? |
| **p3** | 3 | **on** | **on** | off | cascade: Flash workers + rare Pro escalation + auto recon (the blueprint thesis) |
| **p4** | 4 | on | on | **on** | p3 + adaptive effort: conclude fast on low-signal tasks to cut cost |

## Running (REAL terminal only — the OpenRouter egress is blocked inside Claude)

```bash
export OPENROUTER_API_KEY=sk-or-...        # your key
cd /Users/karatinos/slopi-popi/farm

# 1) PRETEST each prototype cheaply on 2 mid-complexity offline tasks (<~$0.30)
./run.sh p1 --only "Счет" "classic" --limit 0.5 --label p1_pretest

# 2) Then the fuller offline run within the $2.50 ceiling
./run.sh p1 --limit 2.5 --label p1_full
```

Outputs: `data/runs/outcomes_<label>.json` + `report_<label>.md`.
KPIs printed: solve-rate, cost, cost/flag. The global `--limit` is a HARD cap
(governor kill-switch); OpenRouter returns exact per-call cost so it is precise.

## Model & cost
- worker `deepseek/deepseek-v4.1-flash` $0.04 in / $0.144 out per 1M
- escalation `deepseek/deepseek-v4-pro` $0.209 / $0.418 per 1M
- reasoning effort via `DEEPSEEK_REASONING_EFFORT` (default low)

## Scoring
Gold flags live in `data/answer_key.json` (extracted from `tasks-with-writeups/`,
quarantined — NEVER staged to an agent). 20/21 tasks scorable; `web/Слушалка`
is unscored (its flag exists only in a writeup screenshot).

## Isolation note
No Docker on this Mac → the sandbox falls back to LocalSandbox (temp dir, scrubbed
env, timeouts) which runs model-generated shell/python **as your user, unisolated**.
Fine for the offline crypto/misc/forensic corpus. Do NOT run untrusted-binary pwn
tasks or live-web tasks this way without Docker.
