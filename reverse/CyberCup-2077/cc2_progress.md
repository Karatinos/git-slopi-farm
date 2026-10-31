# CyberCup resumed — 2026-10-31

Solving resumed by explicit user instruction. Prior progress-summary.md records the earlier pause.
Git remote contributions checked every 120 seconds; own checkpoints published every 300 seconds.

Current objective: recover hidden expected ciphertext backing values by fixing readiness or locating registration initialization.

## First resumed checks

Reproduced readiness failure with 45,185-instruction traces. Clearing versus setting CPUID leaf-1 hypervisor bit gives exactly the same instruction path. The dead marker is pushed by a virtual immediate handler at 0x1415b4c46; tracing bytecode/global setup next. Full native transform extraction reached stage 56; symbolic export still being generated. System Python 3.9 Unicorn crashes (SIGBUS); use ../../.venv/bin/python (3.14) for emulation.
