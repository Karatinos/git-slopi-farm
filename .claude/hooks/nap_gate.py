#!/usr/bin/env python3
"""PreToolUse gate for 'nap mode' (codephrase: "i will take a nap").

While .claude/.nap_active exists, auto-approve every tool call so Claude Code
runs fully autonomously -- EXCEPT a tiny CATASTROPHIC denylist that stays blocked
even in nap mode. When nap mode is OFF, this hook does nothing and Claude Code's
normal permission prompts apply.

To auto-approve literally everything, empty the CATASTROPHIC list below.
"""
import json, os, re, sys

# Irreversible, machine-wide actions kept BLOCKED even in nap mode. Small on
# purpose -- a safety net so a stray command can't brick the Mac while you sleep.
CATASTROPHIC = [
    r"\brm\s+-[rf]{1,2}\s+(/|~|/Users|/home|\$HOME)(\s|/|$)",  # wipe home/root
    r":\(\)\s*\{\s*:\|:",                                       # fork bomb
    r"\bmkfs\b", r"\bdiskutil\s+erase", r"\bdd\b[^\n]*\bof=/dev/",
    r">\s*/dev/disk", r">\s*/dev/sd",
    r"\b(shutdown|reboot|halt)\b",
    r"\bsudo\b",
    r"\bgit\s+push\b[^\n]*(--force\b|-f\b)",                    # don't rewrite shared history
]

def emit(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason}}))

def main():
    proj = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    active = os.path.join(proj, ".claude", ".nap_active")
    if not os.path.exists(active):
        sys.exit(0)                      # nap OFF -> normal prompting
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    blob = json.dumps(data.get("tool_input", {}), ensure_ascii=False)
    for pat in CATASTROPHIC:
        if re.search(pat, blob, re.I):
            emit("deny", "nap mode: blocked by catastrophic-guard /%s/ -- do it yourself when awake" % pat)
            sys.exit(0)
    emit("allow", "nap mode active (codephrase: i will take a nap)")
    sys.exit(0)

main()
