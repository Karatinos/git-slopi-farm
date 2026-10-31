# Independent CyberCup approach

User requested a different solution route. The earlier branch is retained. Work continues on ctf/cybercup-2077-independent with new cc3_* artifacts. No flag has been recovered.

Starting only from verified concrete evidence: unpacked executable; initialized environment; eleven registered hidden-read addresses; concrete expected block values. Large symbolic inversion attempts are stopped. New route: derive an executable high-level transform from concrete instruction/dataflow traces, test it against native code, then invert it algorithmically.
