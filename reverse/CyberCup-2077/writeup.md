# CyberCup-2077

## Flag

```text
ctfcup{d3v3l0pm3n7_0f_7h1S_t4sk_w4s_sp0ns0r3d_by_v01C3s_1n_my_h34d}
```

The flag is 67 bytes. The uppercase `S` in `7h1S` and uppercase `C` in `v01C3s` matter.

The native checker, executed under Unicorn with the challenge's hypervisor services emulated, returns **EAX=1** for this flag. It returns **EAX=0** for both negative controls. Verification includes the nine block comparisons and the two final aggregate comparisons; it does not stop at matching the first block.

## Files and protected execution

The archive contains a protected x64 Windows executable and a kernel driver:

| File | SHA-256 |
| --- | --- |
| `cybercup.exe` | `7482217acb62ed2329b3386e404b7e798a3d4c1c0d69d7c1e84e7e72b8088f84` |
| `cybercup.sys` | `9e73a1beb71ec4171450caeb059be48c452c6633da7990566dd8eb8f6d5405ac` |

The executable uses an image base of `0x140000000`. Its TLS initialization unpacks code and initializes runtime data. The saved initialized image and environment are in `unpack_initialized_state.pkl.gz`; `check_clean.bin` is the analysis image with previously resolved obfuscation thunks simplified. The unpacking scripts, driver analysis, and detailed earlier investigation are retained alongside this writeup.

The relevant checker is the original stub at `0x140698990`, redirected to `0x14166fe79`. It checks a length of `0x43`, performs readiness checks, and then enters the computation at `0x140698a19`. The final comparison result is observed at `0x140698edb`.

The driver supplies custom CPUID/VMMCALL behavior, instruction overrides, and hidden memory reads. Treating these as ordinary x86 instructions or reading static metadata as ciphertext gives incorrect targets.

## Recovering the real hidden reads

The readiness function at `0x1406987c0` registers eleven reads through hypercall `0x3302`. Correct initialization required restoring both the heap and the TEB/PEB segment from the TLS snapshot. In particular:

- The PEB OS build value at `0x7ff01120` must be restored. Omitting it led to an intentional `0xdeadc0de` failure path.
- The runtime global at `0x14134d552` must point to initialized heap object `0x30010000`.
- The emulated process ID and GS self-pointer must agree with the initialized environment.
- `VirtualQuery` must report the reserved sentinel addresses as free.

Each registered read maps a faulting instruction and a sentinel address to a real backing address. At the faulting read, replacing `R10` with the backing **address** lets the original MOV load the value. Substituting an encoded metadata value, or confusing the address with its contents, is incorrect.

For example, the first backing QWORD is `0xf81277ed00eaa1dd`. The comparison unmasks it with `0x638acb6fc47eb41e`, yielding the first target `0x9b98bc82c49415c3`. The complete recovered registrations are in `cc2_init_0x1406987c0_traps.json`; the expected values and workspace offsets are in `cc2_expected.json`.

The nine input-block targets, represented as little-endian 64-bit integers, are:

```text
0  9b98bc82c49415c3
1  405755ccee721bb8
2  c00165c9c347a011
3  5c7bd0947660b2cc
4  e87034174fcb8cce
5  8b0c584a922a5f7b
6  18af8fb58cb6990f
7  7ec28cc38c66a050
8  089cbd6b277f03e5
```

The last two aggregate targets are `0x9c35b18c6772a166` and `0xa731e5d250bde111`.

## Reducing the checker to arithmetic

The large native computation implements basic arithmetic through lookup tables. These include byte XOR, AND, OR, seven byte funnel-shift tables, and a two-dimensional addition table. The funnel table for shift `n` computes:

```python
((x << n) | (y >> (8 - n))) & 255
```

Four such reads implement a 32-bit rotation. The addition table implements `table[x][y] = x + y`; its identity-value region starts at `0x1410d8600`.

Instead of solving the entire lifted SSA graph, `cc3_lut_trace.py` records the actual table reads. `cc3_model.py` derives compact parameters and implements the resulting arithmetic. The model reproduced all nine native output blocks for two different inputs: **18 matching block outputs**. The second input was randomized, which exposed assumptions that happened to fit the repeated-`A` baseline.

For an input byte `c`, each block first computes four byte values, using constants from `cc3_params.json`:

```python
s = c ^ mask
p = (c + offset) & 255
q = s ^ p ^ constant
r = (q + c) & 255
```

There are four transform families, selected by block index modulo four. All state additions below wrap modulo `2**32`. `ROL` denotes 32-bit rotate-left, and the round index `i` is local to the eight-byte block.

### Family 0: eight reversible two-word rounds

Blocks 0, 4, and 8 use:

```python
k = s[i] + 257 + 65*i
a = ROL((a ^ k) + b, 5 + i%7)
b = a ^ ROL(b + (a ^ k), 11 + i%5)
```

The output is `(a,b)`. Given the input byte, each round is reversible:

```python
old_b = ROR(new_b ^ new_a, 11 + i%5) - (new_a ^ k)
old_a = (ROR(new_a, 5 + i%7) - old_b) ^ k
```

For block 0, the initial state is `(0x8d60e266, 0xa23f2146)`, and the byte masks are `7c 2f e2 69 7c 2f e2 69`. Enumerating the eighth byte after `ctfcup{` gives `d`. Block 8 contains the last two flag-body characters and `}`; the five remaining round keys are fixed by the checker. Enumerating the two unknown characters gives `4d}`.

### Family 1: six rounds and output whitening

Blocks 1 and 5 use the same two-word update, but only six rounds, with rotations `7+i` and `11+i`. They then swap the words and XOR the first output with the packed `r` values of bytes 4–7, and the second output with the packed `q` values of bytes 0–3.

### Families 2 and 3: split updates

For family 2, use `s[i]` for even indices and `p[i]` for odd indices to form `k = value + 257 + 65*i`. Then:

```python
# i = 0..3; b remains the initial value
a = ROL(a ^ (b + k), 5 + i)
# i = 4..7; a remains the value after the first four updates
b = ROL(b + k, 13 + i%7) ^ a
```

Family 3 selects `p[i]` for even indices and `s[i]` for odd indices:

```python
# i = 0..3
a = ROL(a + k, 9 + i) ^ (b ^ k)
# i = 4..7
b = ROL(b ^ k, 11 + i%5) + (a ^ k)
```

Both families finally output `a XOR pack(r[4:8])` and `b XOR pack(q[0:4])`. Byte packing is little-endian.

## Recovering the characters

The statement restricts the body to 63 characters: letters, digits, and underscore. An unrestricted eight-character search would require `63**8` candidates. A four-plus-four meet-in-the-middle search requires about `2 * 63**4` evaluations per block.

For family 0, hash the state after the first four forward rounds, then run the last four rounds backward from the target and look for matching states.

For families 2 and 3, hash `(a_after_four, pack(q_first_four))`. For each candidate last half, recover `a_after_four` from the first target word and its `r` whitening, compute the second word, and recover the required packed `q` from the second target word. This gives the matching lookup key.

`cc3_mitm.cpp` implements these searches with an open-addressed hash table. Each of blocks 2, 3, 4, 6, and 7 had one matching candidate. On this machine each search took approximately 2.7–3.5 seconds.

The recovered chunks suggested the phrase “development of this task was sponsored by voices in my head.” For the two six-round blocks, I tested the corresponding leetspeak hypotheses `3v3l0pm3` and `s0r3d_by`, enumerating letter case and requiring their exact 64-bit targets to match. This was a phrase-assisted step, not a completed unrestricted SMT search. Both chunks were subsequently verified by the complete native checker.

| Block | Recovered bytes |
| --- | --- |
| 0 | `ctfcup{d` |
| 1 | `3v3l0pm3` |
| 2 | `n7_0f_7h` |
| 3 | `1S_t4sk_` |
| 4 | `w4s_sp0n` |
| 5 | `s0r3d_by` |
| 6 | `_v01C3s_` |
| 7 | `1n_my_h3` |
| 8 | `4d}` |

## Reproduction and verification

From this directory, using the workspace Python environment:

```sh
../../.venv/bin/python checkpoint_restore.py
../../.venv/bin/python cc3_model.py
../../.venv/bin/python cc3_solve.py
../../.venv/bin/python cc3_verify_native.py
../../.venv/bin/python cc3_verify_native.py --full
```

The solver requires Python and a C++20 compiler. Native emulation additionally requires Unicorn and the saved initialized checkpoint. The tested environment used Python 3.14; the system Python 3.9 Unicorn build crashed on this host.

`cc3_verify_native.py` starts with an empty hidden-read registration map, runs readiness to register all eleven reads, and executes the native flag computation. The positive input returns 1; changing byte 7 from `d` to `A` returns 0; changing the `S` in `7h1S` to `s` also returns 0. `--full` begins at the public checker prologue and produces the same results.

The Windows APIs and hypervisor services are emulated. In `--full` mode, the Windows exception/timing probe is stubbed and the MSVC cookie helper is skipped; the flag transformations and comparisons are executed. This is local native-code verification, not a claim of submission to an online scoreboard. Evidence is retained in `cc3_candidate_native.log`, `cc3_verify_native.json`, and `cc3_verify_full.json`.

The solution and checkpoint artifacts are published on `ctf/cybercup-2077-independent`; the earlier investigation branch is preserved.
