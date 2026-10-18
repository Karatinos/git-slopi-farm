#!/usr/bin/env bash
# Usage: ./run.sh <prototype p1|p2|p3|p4> [extra farm.cli args...]
# Examples:
#   ./run.sh p1 --only "Счет" "classic" --limit 0.5 --label p1_pretest   # cheap pretest
#   ./run.sh p3 --limit 2.5 --label p3_full                              # full offline run
set -euo pipefail
cd "$(dirname "$0")"
source ./env.openrouter.sh
PROTO="${1:?prototype required: p1|p2|p3|p4}"; shift || true
TASKS="../tasks/Кубок Федерации. Отборочный CTF TB"
exec python3 -m farm.cli run --source local --path "$TASKS" --profile ctf \
  --prototype "$PROTO" --offline-only "$@"
