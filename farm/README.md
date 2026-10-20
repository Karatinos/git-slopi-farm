# slopi-farm

A **universal, orchestrated competition-solving farm** — a coordinated swarm of
cheap **DeepSeek V4.1-Flash** agents (via OpenRouter) with rare escalation to
**V4-Pro**, built from the two blueprints in `../plan-of-work/`.

Guiding principle (blueprint §1, DARPA AIxCC 2025): **the win comes from
engineering reliability, coordination and tool quality — not a bigger model.**
~60–70% of the value is the agent–computer interface (ACI), orchestration,
isolation, dedup and budget control.

> **Reading this and nothing else?** Good — this README is the single source of
> truth. The project root also has `CLAUDE.md` (auto-loaded by Claude Code; holds
> the autonomy/"nap mode" contract) and `MIGRATION_GUIDE.md` (the long-form
> handover). Everything you need to be productive is below.

---

## 1. What it solves — both task modes

Task-based (jeopardy) CTF, in **two modes that both matter**:

- **Offline / file tasks** (reverse, crypto, forensics): a challenge is just
  files. The farm stages them into a sandbox, runs recon, and solves locally.
- **Live-instance tasks** (web, pwn): a challenge is a running service
  (`nc host port` or a URL). The farm probes it, finds the bug, and attacks it.

A task carries both `files` and an `endpoint`; a pure-instance challenge with no
downloadable file is ingested and attempted through the **same path** — no
special case, no `if web: … else: …`.

---

## 2. Architecture — one engine, many competitions

A single domain-agnostic engine runs the whole pipeline; a pluggable **Profile**
supplies everything competition-specific. A new kind of contest is a new Profile,
never an edit to the engine.

```
                ┌──────────────────────── core (domain-agnostic) ───────────────────────┐
  source ──►    │  Engine → Scheduler(knapsack) → Ensemble → ReAct agent → verdict/submit │   ──► Outcome
 (adapter)      │     gateway(Flash↔Pro)   sandbox(ephemeral)   blackboard   governor      │
                └───────────────────────────────────────────────────────────────────────┘
                                   ▲ calls, polymorphically ▲
                        Profile:  ingest · toolset · system_prompt · verdict · submit
```

- **`core/`** — the engine, written once: `contracts` (Task/Candidate/Verdict/
  Outcome), `profile` (protocol + registry), `toolset` (shared ACI toolbelt +
  terminal-tool factory), `agent` (thin ReAct loop), `ensemble` (diverse attempts,
  first-to-candidate / majority / consensus, shared blackboard, **hard per-task
  wall-clock deadline**), `scheduler` (knapsack + admission + prefix-cache
  grouping), `net` (reachability + **`probe_instance`** live recon), `engine`
  (composition root + driver), `triage`, `report`.
- **`profiles/`** — `ctf` (success signal = flag, live-scoreboard submit,
  per-category playbooks) and `generic` (answer/program, majority vote).
  `@register`-ed by name.
- **`adapters/`** — `CTFdSource` (live scoreboard: instances + files, real
  grading, **own account per run**) and `LocalSource` (a directory of tasks;
  quarantines solution files, redacts gold).
- **`agent/`** — `recon` (stdlib recon: types/entropy/strings, pcap flow
  reassembly, ELF symbols/imports/`.rodata`), `image_inspect`.
- **`gateway/`** — model gateway: `providers` (DeepSeekProvider via OpenRouter,
  MockProvider, ScriptedSolverProvider), `client`, `types`.
- **`sandbox/`** — `factory` → docker/local; the offline corpus runs in a LOCAL
  fallback if docker is unavailable.
- **`pipeline/`** — `verify` (flag canonicalization), `triage`.
- **`memory/`** — `blackboard` (findings shared across attempts),
  `solution_bank` + `embeddings` (RAG bank), `store`.
- **`observability/`** — `governor` (budget kill-switch), `metrics`, `charts`,
  `tracing`, `report`.
- **`orchestration/`** — `ctfd_client` (register/login/submit, retries).

---

## 3. Development workflow (20/80 · pretest → test)

The working split: **~80% of effort improving the farm, ~20% on paid testing.**
Work smart, not hard. Never let a paid run fail on a bug a free run would catch.

**1 — Build / change (free).** One focused improvement at a time, preferably on
the biggest lever: **ACI / recon** (see §7). Keep edits small and reversible.

**2 — Pretest (free, offline — must pass before any paid run):**
```bash
# a) unit suite green (mock provider, $0)
python3 -m pytest -q                                   # 36 passed

# b) recon signal coverage on the REAL cached files (want high on all offline tasks)
#    (ad-hoc: seed files into a sandbox and inspect run_recon output)

# c) full-engine DRY RUN through the exact code path, no LLM, gold-graded ($0)
SLOPI_PROVIDER=scripted python3 -m farm.cli run --source local \
  --path research/clean_bench --answer-key data/answer_key_clean.json \
  --prototype p3 --limit 1.0 --label dryrun            # expect 8/8 correct

# d) validate launchers / argparse / compare offline
python3 -m farm.compare --glob 'clean_p*' --out /tmp/cmp_test
```
Providers for free pretesting: `mock` (deterministic) and `scripted` (no-LLM
autosolver that exercises the real pipeline). Both cost $0.

**3 — Version control.** Commit every green step (git). Each commit is a
known-good checkpoint; tests stay green.

**4 — Test (paid, bounded — only from a real terminal / local machine):**
- Run prototypes against the live CTFd, **both modes**, each under its **own
  CTFd account**, each with a **hard `$` cap**.
- Budget discipline: **≤ ~$1.5 per prototype, < $6 total** per comparison. The
  governor enforces caps; **never raise a cap to "finish" a run.**
- One click: `START_COMPARE.command` runs p1/p3/p5/p7 and builds the KPI
  table + chart via `farm.compare`.

**5 — Measure & iterate.** Read the KPIs — solve-rate, **cost-per-flag**,
time-to-flag, escalation-rate — in `data/runs/compare_live.{md,png}`. Pick the
winner, feed findings back into step 1. **Don't blind-tune offline without live
feedback.**

---

## 4. Quickstart

```bash
cd farm
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

python3 -m farm.cli profiles            # -> ctf, generic  (what it can solve)
python3 -m pytest -q                    # 36 tests, mock provider, $0

# CTF against a local corpus (offline, gold-graded if an answer key exists)
python3 -m farm.cli run --profile ctf --source local --path ../tasks

# CTF against the live CTFd (files + instances, real grading) — REAL TERMINAL ONLY
python3 -m farm.cli run --profile ctf --source ctfd \
  --base-url "$CTFD_URL" --header "$CTFD_HEADER" --reg-code "$CTFD_REGCODE" \
  --prototype p3 --limit 1.5 --label live_p3
```

Runs with **no API key** end-to-end via the deterministic `mock` provider; set
the OpenRouter env (below) and `SLOPI_PROVIDER=deepseek` for the real model.

### Launchers (double-click in a real Terminal.app)

| Launcher | What it does |
| :- | :- |
| `START_COMPARE.command` | **main** — runs p1/p3/p5/p7 (files + instances), each own account, capped so the total stays < $6, then writes `data/runs/compare_live.{md,png}` |
| `START_LIVE_RUN.command` | single run: `START_LIVE_RUN.command <proto> <cap$>`, both modes |
| `START_CTFD_PULL.command` | refresh the offline CTFd catalog cache |
| `START_RUN.command` | local corpus run |

---

## 5. Environment, secrets & the egress constraint

**Where it can spend money.** Any cloud-hosted agent environment (this chat's
container, a cloud Claude Code session) sits behind an **egress allowlist**:
only package registries + GitHub are reachable; **OpenRouter and the CTFd are
NOT.** So paid/live runs cannot run there — they run from a **real terminal on a
machine with network** (the launchers). **Local Claude Code on the Mac has the
Mac's network**, so there it can hit OpenRouter and the LAN CTFd directly — no
launcher needed. The live CTFd instances live on `192.168.1.108` (user's LAN),
unreachable from any cloud session.

**Secrets** live in `farm/.secrets/*.env` (git-ignored — recreate them in a new
environment). The model gateway reads them from the process env:

| File | Vars |
| :- | :- |
| `farm/.secrets/openrouter.env` | `OPENROUTER_API_KEY`, `DEEPSEEK_API_KEY` (= same OpenRouter key), `DEEPSEEK_BASE_URL`=`https://openrouter.ai/api/v1`, `DEEPSEEK_FLASH_MODEL`=`deepseek/deepseek-v4.1-flash`, `DEEPSEEK_THINK_MODEL`, `DEEPSEEK_PRO_MODEL`=`deepseek/deepseek-v4-pro`, `DEEPSEEK_REASONING_EFFORT`=`low`, `SLOPI_PROVIDER`=`deepseek` |
| `farm/.secrets/ctfd.env` | `CTFD_URL`, `CTFD_HEADER` (bypasses Authelia, header `x-benchmark`), `CTFD_REGCODE` (throwaway-account registration code) |

`SLOPI_PROVIDER`: `deepseek` (live, OpenRouter) · `mock` (deterministic, $0) ·
`scripted` (no-LLM autosolver / pipeline validator, $0) · `auto`.
Template: `farm/env.openrouter.sh` (reads the key from the env; no key in the repo).

---

## 6. Benchmark & integrity

- **Live CTFd:** `https://ctfd.snowyx.dev` behind Authelia (bypass with the
  `x-benchmark` header). **72 challenges**: 12 each in crypto/forensics/misc/
  pwn/reverse/web. **32 offline (files) + 40 live instances.**
- **Cache:** `data/ctf_bench/` (catalog + 80 files, **not in git** — re-pull with
  `START_CTFD_PULL.command`); accounts logged to `data/ctf_bench/accounts.log`.
- **Integrity trap:** `../tasks-with-writeups/` (and parts of `../tasks/`) are
  **solution write-ups with flags and solver scripts**, not clean tasks. A direct
  run over them yields a **bogus** solve-rate. `LocalSource` defends this: takes
  the statement from page 1 of a task PDF only, redacts gold, and quarantines
  solver files (by name and by gold-flag text). Gold is kept for grading in
  `data/answer_key*.json` and is **never staged to an agent.**

---

## 7. Recon = the ACI lever (biggest driver of solve-rate)

- **File recon → high signal on all 32 offline tasks.** `strings` catches
  base64/hex/UUID exfil blobs (memory dumps); for stripped ELF it extracts
  imported libc calls (ptrace/memcmp/mmap…) and `.rodata` literals; pcap is
  reassembled into TCP/UDP flows.
- **Instance recon** (`net.probe_instance`): first-contact probe of a live
  service — HTTP (status/headers/`<title>`/forms+inputs/comments/robots.txt) and
  raw-TCP banner grab. The web/pwn playbooks consume it (chase robots paths,
  submit discovered form fields, read the service banner before scripting).
- Gated by the prototype's `recon` flag; runs per-task (budget-aware), with short
  timeouts and instant fail on an unreachable endpoint.

---

## 8. Prototypes (strategy knobs on one engine = fair A/B)

Defined in `farm/cli.py:_PROTOTYPES`; any knob overridable by flag
(`--ensemble/--escalate/--recon/--adaptive/--consensus`).

| # | ensemble | escalate F→Pro | recon | adaptive | consensus | role |
| :- | :- | :- | :- | :- | :- | :- |
| p1 | 1 | — | — | — | 1 | baseline (control) |
| p2 | 4 | — | ✓ | — | 1 | ensemble + recon |
| p3 | 3 | ✓ | ✓ | — | 1 | smart cascade |
| p4 | 4 | ✓ | ✓ | ✓ | 1 | cascade + adaptive |
| p5 | 5 | — | ✓ | — | 2 | precision (self-consistency) |
| p6 | 2 | ✓ | ✓ | ✓ | 1 | lean cascade |
| p7 | 6 | — | ✓ | ✓ | 1 | broad cheap coverage |

The paid comparison uses **p1 / p3 / p5 / p7** (most distinct approaches).

---

## 9. Config & budgets (`farm/config.py`)

| Knob | Value / note |
| :- | :- |
| `max_tokens_per_call` | 6144 — **critical**: V4.1-Flash reasons by default; at 1024 it returned empty |
| `per_task_usd_cap` | $1.20 per task; `--limit` is the hard per-run ceiling |
| `max_seconds` | 180 per trajectory; ensemble adds a **hard per-task wall-clock deadline** (killed 2–3 h hangs) |
| `request_timeout` / `max_retries` | 45s / 1 (trimmed for responsiveness) |
| `tool_timeout` | 50s per tool |
| `hard_categories` | `("pwn",)` |
| PRICING / models | OpenRouter: Flash $0.04/$0.144, Pro $0.209/$0.418 per 1M; models from env |

---

## 10. Nuances & hard-won lessons

- **ACI/recon is the lever** — improve it before model/ensemble tweaks.
- **Hangs:** model retries + hanging connects once caused 2–3 h/task. Fixed by the
  ensemble hard deadline + trimmed timeouts. Don't restore large timeouts.
- **pcap endianness:** the magic→endian map was once reversed — re-verify recon on
  Party Line / Records / Careless Beacon after touching it.
- **Flag submit:** wrap in try/except + retries (catches `httpx.RemoteProtocolError`,
  which otherwise crashes the whole run).
- **Per-prototype accounts:** each run registers its own `slopi_<label>_<uid>` and
  logs creds — flags used to land on an anonymous account. Keep one account per prototype.
- **ScriptedSolver:** `research/autosolve.py` must NOT have
  `from __future__ import annotations` (it broke the `os.environ[...]` endpoint injection).
- **Git on the bridged Mac folder:** deletion is blocked by default, so git leaves
  `.lock`/tmp files that break later git commands. Grant delete permission for the
  folder, then clean the locks.
- **Realistic expectations:** strong on web/forensics/templated steps; weak on
  hard-pwn and advanced crypto (NYU CTF Bench ~13.5% for EnIGMA). Optimize
  **cost-per-flag**, not 100%.

---

## 11. Cost & safety

- Triple budget per trajectory (steps / tokens / wall-time) + a global cost
  governor and a real-balance guard (kill-switch).
- Ephemeral sandbox per attempt; API keys never enter the sandbox.
- Only sanctioned/training targets; the farm reads task content as **data, not
  instructions** (prompt-injection discipline, blueprint §10).
