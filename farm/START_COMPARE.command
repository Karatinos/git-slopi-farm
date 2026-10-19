#!/bin/bash
# =============================================================================
#  ONE-CLICK PROTOTYPE COMPARISON  (paid — DeepSeek V4.1-Flash via OpenRouter)
# =============================================================================
#  Runs 4 curated farm prototypes against ctfd.snowyx.dev, BOTH file tasks and
#  live instances, each under its OWN CTFd account, each hard-capped so the
#  WHOLE comparison stays < $6.  Then writes a KPI table + chart.
#
#    p1  baseline         single Flash, no recon        (control)
#    p3  smart cascade     ensemble 3 + recon + Flash->Pro escalation
#    p5  precision         ensemble 5 + recon + consensus=2 (self-consistency)
#    p7  broad coverage    ensemble 6 + recon + adaptive effort
#
#  Just double-click. Leave it running; it prints a summary at the end.
#  Per-prototype cap below; 4 x $1.40 = $5.60 total ceiling.
# =============================================================================
cd "/Users/karatinos/slopi-popi/farm" || exit 1
source ./.secrets/ctfd.env
source ./.secrets/openrouter.env
python3 -m pip install --user --quiet openai httpx pypdf pycryptodome sympy numpy pillow requests scapy capstone pyelftools pwntools matplotlib 2>/dev/null \
  || python3 -m pip install --user --break-system-packages --quiet openai httpx pypdf pycryptodome sympy numpy pillow requests scapy capstone pyelftools pwntools matplotlib 2>/dev/null

CAP="${1:-1.40}"            # per-prototype hard cap (USD)
PROTOS="p1 p3 p5 p7"
mkdir -p data/ctf_bench data/runs
echo "=================================================================="
echo " PROTOTYPE COMPARISON   protos=[$PROTOS]  cap=\$$CAP each  (<\$6 total)"
echo " each prototype registers its own account (saved to data/ctf_bench/accounts.log)"
echo "=================================================================="
for P in $PROTOS; do
  echo; echo ">>>>>> $P  (hard-cap \$$CAP) >>>>>>"
  python3 -m farm.cli run --source ctfd \
    --base-url "$CTFD_URL" --header "$CTFD_HEADER" --reg-code "$CTFD_REGCODE" \
    --profile ctf --prototype "$P" --limit "$CAP" --label "cmp_${P}" \
    2>&1 | tee "data/ctf_bench/cmp_${P}.log"
done
echo; echo ">>>>>> building comparison table + chart >>>>>>"
python3 -m farm.compare --glob 'cmp_p*' --out data/runs/compare_live 2>&1
echo
echo "=================================================================="
echo " DONE.  Results:"
echo "   table : data/runs/compare_live.md"
echo "   chart : data/runs/compare_live.png"
echo "   accts : data/ctf_bench/accounts.log   (which account solved what)"
echo "   logs  : data/ctf_bench/cmp_p*.log"
echo "=================================================================="
echo " (you can close this window)"
