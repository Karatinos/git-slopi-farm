# Independent CyberCup approach

User requested a different solution route. The earlier branch is retained. Work continues on ctf/cybercup-2077-independent with new cc3_* artifacts. No flag has been recovered.

Starting only from verified concrete evidence: unpacked executable; initialized environment; eleven registered hidden-read addresses; concrete expected block values. Large symbolic inversion attempts are stopped. New route: derive an executable high-level transform from concrete instruction/dataflow traces, test it against native code, then invert it algorithmically.

## Compact model recovered

`cc3_lut_trace.py` records the actual byte-table and addition-table reads during checker execution. `cc3_model.py` derives seeds and byte preprocessing parameters, then implements four transform families selected by block index modulo four. `cc3_params.json` contains the recovered parameters. All nine block outputs match native execution for both the baseline and a different randomized input (18 matches). Initial seeds are constant across the two traces.

Preprocessing produces s = c XOR mask, p = (c + constant) modulo 256, q = s XOR p XOR constant, and r = (q + c) modulo 256. All round keys add 257 + 65*i. Family 0 has eight reversible two-word rounds. Family 1 has six two-word rounds followed by swapped output words and byte-dependent whitening. Families 2 and 3 update the first word with the first four characters, then the second word with the last four; final whitening uses r of the last four characters and q of the first four.

Next step: meet-in-the-middle searches for families 0/2/3 and a compact inversion for family 1. The full checker still needs to accept the combined flag, including its two aggregate comparisons. No complete flag is claimed yet.
