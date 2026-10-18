#!/usr/bin/env bash
# Runs all four prototypes on the offline-friendly corpus, $1.50 hard cap each
# (<= $6 total). Results -> data/runs/outcomes_<p>_full.json + report_<p>_full.md
set -euo pipefail
cd "$(dirname "$0")"
source ./env.openrouter.sh
TASKS="../tasks/Кубок Федерации. Отборочный CTF TB"
CATS="crypto misc forensic reverse"      # offline-friendly (no live service/Docker)
for P in p1 p2 p3 p4; do
  echo; echo "================= $P ================="
  python3 -m farm.cli run --source local --path "$TASKS" --profile ctf \
    --prototype "$P" --offline-only --categories $CATS \
    --limit 1.5 --label "${P}_full" || echo "[warn] $P stopped (budget or error)"
done
echo; echo "ALL DONE -> data/runs/"
