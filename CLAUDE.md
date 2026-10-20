# slopi-farm — orientation for Claude Code

Autonomous farm that solves task-based (jeopardy) CTF with a swarm of cheap
DeepSeek V4.1-Flash agents (OpenRouter) + rare escalation to V4-Pro. Code lives
in `farm/`. Read `farm/MIGRATION_GUIDE_RU.pdf` and `farm/README.md` first; the
live status is in the claude.ai project doc `claude/implementation-status.md`.

Key facts:
- One domain-agnostic engine (`farm/core/`) + pluggable profiles (`farm/profiles/`).
- Secrets in `farm/.secrets/*.env` (git-ignored). The model gateway reads
  `DEEPSEEK_API_KEY` (= OpenRouter key), `DEEPSEEK_BASE_URL`, `DEEPSEEK_*_MODEL`,
  `SLOPI_PROVIDER`. CTFd creds in `farm/.secrets/ctfd.env`.
- Hard money caps are real: `--limit` (per run), `per_task_usd_cap`, and the
  budget governor. NEVER raise them to "finish" a run — stop at the cap.
- Each paid run registers its OWN CTFd account (per-prototype). Keep it that way.
- Running locally here, the Mac's network reaches OpenRouter and the LAN CTFd
  directly — paid runs can execute without the `.command` launchers.
- Tests: `cd farm && python3 -m pytest -q` (must stay green).

## Nap mode (codephrase: "i will take a nap")

When the user types **"i will take a nap"**, a hook enables autonomous mode and
tool calls stop prompting (see `.claude/hooks/`). In this mode you MUST:
- Not ask for any confirmation, approval, or check-in — the user is asleep.
- Take the most reasonable reading of any ambiguity and proceed; only stop for a
  decision that is irreversible AND could reasonably go either way — prepare it
  and leave it for waking, continuing with everything else.
- Keep working until the task is done or a $ budget cap is hit.
- Version every step (git commit), log actions to files, and leave a PDF or
  markdown report before going idle.
- Respect the hard $ caps and the catastrophic-guard (it stays on by design).
- A standing nightly job is the prototype comparison: `START_COMPARE.command`'s
  logic — run p1/p3/p5/p7 (files + instances), each own account, each capped so
  the total stays < $6, then `python3 -m farm.compare --glob 'cmp_p*'`.

The user ends nap mode with "i am awake" / "good morning" / "wake up".
When nap mode is OFF, behave normally and let Claude Code ask for confirmations.
