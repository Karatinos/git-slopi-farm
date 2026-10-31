# CyberCup resumed — 2026-10-31

Solving resumed by explicit user instruction. Prior progress-summary.md records the earlier pause.
Git remote contributions checked every 120 seconds; own checkpoints published every 300 seconds.

Current objective: recover hidden expected ciphertext backing values by fixing readiness or locating registration initialization.

## First resumed checks

Reproduced readiness failure with 45,185-instruction traces. Clearing versus setting CPUID leaf-1 hypervisor bit gives exactly the same instruction path. The dead marker is pushed by a virtual immediate handler at 0x1415b4c46; tracing bytecode/global setup next. Full native transform extraction reached stage 56; symbolic export still being generated. System Python 3.9 Unicorn crashes (SIGBUS); use ../../.venv/bin/python (3.14) for emulation.

## Readiness breakthrough

The emulator omitted the saved PEB OS-build fields, causing a fail path. Additionally check_clean.bin has zero at the initialized runtime pointer 0x14134d552, while unpack_initialized.bin has 0x30010000. Restoring the saved PEB plus that pointer reaches VirtualQuery. Modeling VirtualQuery for the unmapped sentinel range as MEM_FREE now registers real 0x3302 hidden-read traps. First backing address is 0x140f43d60. See cc2_init.py/log; registration run is in progress.

All 11 hidden read registrations recovered in cc2_init_0x1406987c0_traps.json. First backing QWORD is 0xf81277ed00eaa1dd, first expected ciphertext after comparison mask is 0x9b98bc82c49415c3. Existing 63-character concrete probe matches eighth character d, establishing prefix ctfcup{d. Running full symbolic checker including real trap reads and comparisons.
