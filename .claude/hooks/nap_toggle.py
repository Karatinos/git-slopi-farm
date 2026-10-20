#!/usr/bin/env python3
"""UserPromptSubmit toggle for nap mode.

  "i will take a nap"  -> ENABLE autonomous mode (create .claude/.nap_active)
  "i am awake" / "good morning" / "wake up" / "stop nap" -> DISABLE it

Prints a one-line confirmation that Claude Code adds to the conversation context.
"""
import json, os, sys

SLEEP = "i will take a nap"
WAKE  = ("i am awake", "i'm awake", "im awake", "good morning", "wake up", "stop nap", "end nap")

def main():
    proj = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    active = os.path.join(proj, ".claude", ".nap_active")
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    prompt = (data.get("prompt") or "").lower()
    if SLEEP in prompt:
        os.makedirs(os.path.dirname(active), exist_ok=True)
        with open(active, "w") as f:
            f.write("nap mode on\n")
        print("[NAP MODE ON] Autonomous mode enabled: do NOT ask for any confirmation or "
              "check-in. Work end-to-end, take the most reasonable reading of ambiguity, keep "
              "going until the task or the $ budget cap is reached, log actions to files, commit "
              "each step, and leave a PDF/markdown report. Respect the farm's hard $ caps "
              "(per_task_usd_cap, --limit, governor). Only a tiny catastrophic-guard "
              "(rm -rf /, sudo, git push -f, disk wipes, shutdown) stays blocked.")
    elif any(w in prompt for w in WAKE):
        try:
            os.remove(active)
            print("[NAP MODE OFF] Normal confirmations restored.")
        except FileNotFoundError:
            pass
    sys.exit(0)

main()
