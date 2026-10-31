# Independent CyberCup approach

User requested a different solution route. The earlier branch is retained. The solution was recovered on ctf/cybercup-2077-independent with new cc3_* artifacts and verified on 2026-10-31.

**Verified flag:** `ctfcup{d3v3l0pm3n7_0f_7h1S_t4sk_w4s_sp0ns0r3d_by_v01C3s_1n_my_h34d}`

The native checker returns EAX=1 for the flag and EAX=0 for two altered inputs. All eleven hidden reads are registered afresh during verification. Both readiness-entry and public-checker-entry runs reach the final comparison, including the two aggregate checks. The public-entry harness stubs the Windows exception/timing probe and emulates APIs/hypervisor services. Evidence: `cc3_verify_native.json` and `cc3_verify_full.json`. Full explanation and reproduction commands: `writeup.md`.

Starting only from verified concrete evidence: unpacked executable; initialized environment; eleven registered hidden-read addresses; concrete expected block values. Large symbolic inversion attempts are stopped. New route: derive an executable high-level transform from concrete instruction/dataflow traces, test it against native code, then invert it algorithmically.

## Compact model recovered

`cc3_lut_trace.py` records the actual byte-table and addition-table reads during checker execution. `cc3_model.py` derives seeds and byte preprocessing parameters, then implements four transform families selected by block index modulo four. `cc3_params.json` contains the recovered parameters. All nine block outputs match native execution for both the baseline and a different randomized input (18 matches). Initial seeds are constant across the two traces.

Preprocessing produces s = c XOR mask, p = (c + constant) modulo 256, q = s XOR p XOR constant, and r = (q + c) modulo 256. All round keys add 257 + 65*i. Family 0 has eight reversible two-word rounds. Family 1 has six two-word rounds followed by swapped output words and byte-dependent whitening. Families 2 and 3 update the first word with the first four characters, then the second word with the last four; final whitening uses r of the last four characters and q of the first four.

Completed: C++ meet-in-the-middle searches gave one candidate each for blocks 2, 3, 4, 6, and 7 in approximately 2.7–3.5 seconds per block. Short searches recovered blocks 0 and 8. The recovered phrase suggested hypotheses for blocks 1 and 5; case enumeration matched their exact targets. No unrestricted SMT result is claimed for those two blocks. `cc3_solve.py` reproduces the block recovery and validates all targets, and `cc3_verify_native.py` validates the combined flag in the native checker. No solving computations need to remain running. The requested Git read/publish loop remains separate.
