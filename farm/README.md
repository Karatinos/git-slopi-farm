# slopi-farm

A **universal, orchestrated competition-solving farm** — a coordinated swarm of
cheap **DeepSeek V4-Flash** agents with rare escalation to **V4-Pro**, built
strictly from the two blueprints in `../plan-of-work/`.

Guiding principle (blueprint §1, DARPA AIxCC 2025): **the win comes from
engineering reliability and coordination, not a bigger model.** ~60–70% of the
value is orchestration, isolation, dedup and budget control.

## One engine, many competitions (no `if ctf: … else: …`)

The farm is **goated for task-based (jeopardy) CTF** but not *limited* to it. A
single domain-agnostic engine runs the whole pipeline; a pluggable **Profile**
supplies everything competition-specific. Adding a new kind of contest is a new
Profile — never an edit to the engine, never a branch.

```
                ┌──────────────────────── core (domain-agnostic) ───────────────────────┐
  source ──►    │  Engine → Scheduler(knapsack) → Ensemble → ReAct agent → verdict/submit │   ──► Outcome
 (adapter)      │     gateway(Flash↔Pro)   sandbox(ephemeral)   blackboard   governor      │
                └───────────────────────────────────────────────────────────────────────┘
                                   ▲ calls, polymorphically ▲
                        Profile:  ingest · toolset · system_prompt · verdict · submit
```

* **`core/`** — the engine written once: `contracts` (Task/Candidate/Verdict/
  Outcome), `profile` (the Profile protocol + registry), `toolset` (one shared
  ACI toolbelt + a terminal-tool factory), `agent` (the thin ReAct loop),
  `ensemble` (diverse attempts, first-to-candidate / majority-select, shared
  blackboard), `scheduler` (priority knapsack + admission + prefix-cache
  grouping), `engine` (composition root + driver).
* **`profiles/`** — `ctf` (flag success signal, live scoreboard submit) and
  `generic` (answer/program deliverables, majority vote). `@register`-ed by name.
* **`adapters/`** — input sources: `CTFdSource` (live scoreboard, instances +
  files, real grading) and `LocalSource` (a directory of tasks).
* Reused primitives (unchanged): `gateway`, `sandbox`, `memory`, `observability`,
  `pipeline/verify` (flag canonicalization), `orchestration/ctfd_client`.

## Files **and** instances, through the same path

A task carries both `files` (staged into the sandbox) and an `endpoint` (a live
service/instance like `nc host port` or a URL). The CTF profile injects a clear
"Live service" block; the sandbox runs with network access so the agent can
`curl`/`nc`/`pwntools` the target. A pure-instance challenge with no downloadable
file is ingested and attempted exactly like a file challenge — no special case.

## Quickstart

```bash
cd farm
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# list what the farm can solve
.venv/bin/python -m farm.cli profiles            # -> ctf, generic

# CTF against a live CTFd (files + instances, real grading)
.venv/bin/python -m farm.cli run --profile ctf --source ctfd \
  --base-url https://... --header 'x-benchmark: ...' --reg-code ... \
  --flag-format 'swarm{...}' --limit 2.0 --per-task 0.10

# CTF against a local corpus (offline, gold-graded if a flag sidecar exists)
.venv/bin/python -m farm.cli run --profile ctf --source local --path ../tasks

# a different competition (answers/programs) — same engine, different profile
.venv/bin/python -m farm.cli run --profile generic --source local --path ../work-on
```

Runs with **no API key** (deterministic mock provider) end-to-end; set
`DEEPSEEK_API_KEY` in `.env` for the real model.

## Tests

The engine, profiles, scheduler, triage, reachability gate and KPI report have a
dependency-free unit suite (stdlib `unittest`, mock provider, zero API cost):

```bash
.venv/bin/python -m unittest farm.tests.test_farm -v   # 25 tests
```

## Cost & safety

* Triple budget per trajectory (steps / tokens / wall-time) + a global cost
  governor and a real-balance guard (kill-switch).
* Ephemeral sandbox per attempt; API keys never enter the sandbox.
* Only sanctioned/training targets; the farm reads task content as **data, not
  instructions** (prompt-injection discipline, blueprint §10).

## Config

Key knobs in `farm/config.py` (budgets, cascade policy, ensemble size, sandbox
limits). Env: `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`, `DEEPSEEK_FLASH_MODEL`,
`DEEPSEEK_PRO_MODEL`, `SLOPI_PROVIDER` (auto|deepseek|mock).
