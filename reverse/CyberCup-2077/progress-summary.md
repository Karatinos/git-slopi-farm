> Update 2026-10-31: CyberCup-2077 is now solved and locally verified. See `writeup.md`, `cc3_progress.md`, and `cc3_verify_full.json`. The historical stopped-work snapshot below is preserved.

# CyberCup-2077 — paused progress and handoff

Recorded 2026-10-31 (Europe/Moscow). **The user requested that solving stop. It has stopped. No flag has been recovered or confirmed.** This is a progress record, not a successful writeup. Do not resume solving without a new instruction. The separately requested ten-minute Git synchronization/contribution review is allowed to continue.

## User instructions and scope

- Current challenge: `reverse/CyberCup-2077`. Earlier prompts named Noise-in-space, 21-century-man and GhostVector; those are separate tasks and are not the subject of this checkpoint.
- Recover a real `ctfcup{...}` flag; only write the final `writeup.md` after confirmation. No `writeup.md` was created for this challenge.
- Save detailed progress in this directory and on GitHub.
- Every ten minutes, publish progress and read other agents' contributions, until the Codex tab is closed.
- **Never delete files or edit files you did not add.** Original attachments remain unchanged. Work by other agents is retained as theirs; new checkpoint copies and this summary do not replace originals.
- The root agent and three collaborating agents worked on unpacking, driver semantics, and the checker. All solving agents were interrupted. The outstanding all-block symbolic/export and inverse-solving processes were stopped. Subsequent work is archival and Git synchronization only.

## State at the stop

Completed and supported by concrete checks:

1. Unpacked the protected EXE and completed its first TLS callback. A usable mapped image, a disassembler PE, and a matching initialized Unicorn context/heap are saved.
2. Reversed the driver's custom CPUID interface, ARM64 interpreter and x86 override machinery, hypercall protocols, hidden read/control transfers, SipHash-based sessions and ticket transform.
3. Recovered the actual length check and transform pipeline. The input must have **67 bytes**; the pipeline transforms nine independent eight-byte blocks into 72 output bytes.
4. Classified its arithmetic lookup tables and removed substantial inert protection code.
5. Obtained and concretely validated symbolic equations for the first block.
6. Found that expected ciphertext values come through driver-assisted hidden reads, and identified a further XOR mask in the first comparison.

**Main unresolved dependency:** the real backing values for the hidden reads. The readiness/registration path does not yet run correctly in the emulator. A full flag was never produced. Neither direct XOR of the static metadata pair nor that XOR plus the comparison mask is the expected first-block ciphertext.

## Challenge and environment

Statement, from `CyberCup-2077.txt`:

> CyberCup 2077  
> 1000 points / 1 solvers  
> reverse, windows  
> Wake up, Samurai. We've got a ctf to slop.  
> Flag format: ctfcup{[a-zA-Z0-9_]+}  
> cybercup.zip

Inputs:

- `cybercup.zip`: SHA-256 `056d94d8e7e5b119caf800219a056a20d19691b15e78cb0e8de4d1b8407a1213`.
- `cybercup.exe`: 16,291,840 bytes; SHA-256 `7482217acb62ed2329b3386e404b7e798a3d4c1c0d69d7c1e84e7e72b8088f84`.
- `cybercup.sys`: 27,024 bytes; SHA-256 `9e73a1beb71ec4171450caeb059be48c452c6633da7990566dd8eb8f6d5405ac`.

Host: macOS ARM64. Local project path: `/Users/karatinos/Downloads/Staff/fsp`. Challenge path: `reverse/CyberCup-2077`. Python dependencies observed: pefile 2024.8.26, capstone 6.0.0a6, unicorn 2.1.1, z3-solver 5.1.0.0. A project `.venv` was used during analysis; system Python also reports these packages. The driver was modeled/emulated, not loaded into the host kernel. Pickled Unicorn contexts are tied to the Python/Unicorn implementation; keep their matching environment in mind when restoring.

The EXE is a Windows x64 GUI program, with Rust GUI code and a native protected checker. The driver is an AMD SVM / SimpleSvm-derived hypervisor. The protector has VMProtect-style mutation/virtualization and custom driver integration; that identification is descriptive, not a claim of a particular verified product/version.

## Executable layout and unpacking

Image base: `0x140000000`. Mapped image size: `0x25fc000` (39,829,504 bytes). Packed entry point: `0x1425fa93c`.

TLS callbacks:

- `0x142419ae5`: protector/unpacker.
- `0x140396380`: Rust CRT callback; observed to return immediately for attach reason EDX=1, with detach cleanup elsewhere.

Relevant decompressed regions:

- `.text`: VA `0x140001000`, length `0x6e2e00`.
- `.rdata`: VA `0x1406e4000`, length `0xb2ae00`.
- `.data`: VA `0x14120f000`, length `0xc00`.
- `.pdata`: VA `0x141219000`, length `0x31400`; it still looks unusual/random and was not needed for the fixup recovery.
- `.ygzqwaa`: VA `0x14124b000`, length `0x425200`; mutated/virtualized native code.

The original packed PE has zero raw sizes for these sections. Static analysis of the original file alone misses the runtime contents.

### Loader strategy

`unpack_emu.py` uses Unicorn, a synthetic PEB/TEB, Windows API stubs and custom CPUID answers. The obfuscated API resolver at `0x14246778f` was intercepted. An encrypted export-name byte at index i is decoded as:

```text
byte ^ low8(ROL32(0x17a206fd, i) + i)
```

`wine_get_version` must resolve to NULL. An early “Initialization error 5” was caused by missing custom CPUID responses in the model.

An expensive CRC routine was accelerated while preserving its computation. The main decompression routine at `0x1424661cb` was identified as raw LZMA1:

- RCX points to lc/lp/pb dwords (3, 0, 2).
- RDX points to the compressed stream.
- Output pointer is at [RSP+0x28].
- R9 points to consumed-byte output.
- Output-length pointer is at [RSP+0x38].
- Python raw LZMA1 with dictionary size 1<<26 decodes through the end marker; return RAX=0.
- First stream source `0x14209ff97`, consumed `0x295610`, output `0x6e2e00`.

This replaced hundreds of millions of emulated decompressor instructions.

### Metadata decoder

Metadata header at `0x141671000`: magic `0x2db95856`, count word `0xc000edfa`. Starting at `0x141671008` are **60,922** records, each `(rva32, cipher32, kind32)`. All target four-byte fields in `.ygzqwaa`, not the original .text/.rdata/.pdata.

`unpack_fixups.py` implements the exact chained recurrence, with 32-bit arithmetic:

```python
def H(a, b):
    x = a ^ b ^ 0x9e3779b9
    x = ROL32(x, 13)
    x = x * 0x85ebca6b & 0xffffffff
    x ^= x >> 15
    x = x * 0xc2b2ae35 & 0xffffffff
    return x ^ (x >> 16)

mask = 0xd5b3498a
plaintext0 = ciphertext0 ^ mask  # 0x228
for i in range(1, count):
    key = [0xa29a6108, 0x7580794a][i & 1]
    state = H(mask, previous_cipher ^ key ^ 0xaf201288)
    mask = H(state ^ key, i)
    plaintext = cipher ^ mask
    previous_cipher = cipher
```

There are 36 nonzero-kind environment records: kind<32 XORs an environment word, otherwise the operation adds env[kind&31]. The current script copies these 36 already naturally decoded fields from `unpack_memory.bin`, instead of recomputing their environment. Preserve that file if regenerating offline fixups.

Observed environment words:

```text
env[1,13,20] = 1234
env[2,14,21] = 0x20
env[3,15,22] = 0xe04000ff
env[16] = 0
env[17] = 0x6000
env[18,23] = 0xa29a6108
env[19] = 0x4eb00f29
env[24] = 0x4eb06f29
env[31] = 0x0c6a0a2c
```

**Validation:** 42,232 naturally modified fields matched the offline decoder, with zero mismatches. Random-access/index-skipping attempts were wrong because the mask chains through the previous record.

### Final initialization and dependencies

`unpack_finish.py` resumes an input checkpoint supplied as its first argument, overlays the decoded .ygzqwaa region from `unpack_final.bin`, and continues TLS. It writes `unpack_initialized.bin` and `unpack_initialized_state.pkl.gz`. `unpack_finish2.log` records successful TLS completion with RAX=1 and RIP=0 sentinel.

The initialized pickle contains:

- `ctx`: Unicorn CPU context.
- `mem`: (address, bytes) segments, including image, stack at 0x10000000, heap at 0x30000000, and TEB/PEB at 0x7ff00000.
- `apis`, `reverse`: API stub maps.
- `heap`: current allocation position.

**Critical:** global `0x14134d552` must point to initialized heap `0x30010000`. A bare image without that heap faults at address 0x10 in virtualized code. Never overwrite initialized runtime data with `unpack_final.bin`; it is a pre-TLS snapshot.

Environment used: PID/TID 1234; PEB 0x7ff01000; process heap 0x30000000. Normal CPU leaves:

```text
leaf 0: EAX=13 EBX=756e6547 ECX=6c65746e EDX=49656e69
leaf 1: EAX=306a9 EBX=10800 ECX=7ffafbff EDX=bfebfbff
```

The driver's normal leaf-1 handling ORs ECX bit 31. Trying the resulting ECX=fffafbff did not fix the later readiness failure. Changing CPU/PID/PEB values can invalidate environment-dependent fields.

`unpack_initialized.exe` is a convenience reconstructed PE (raw section offsets equal RVAs). The initialized mapped binary and matching heap/context are the authoritative execution artifacts. CRT/OEP startup is not fully completed by the TLS checkpoint.

## Driver results

Useful implementation files: `driver_analysis_arm.py`, `driver_analysis_hv.py`, `check_hypercall.py`, with native comparison tests in `driver_analysis_validate.py`, `driver_analysis_hv_validate.py`, `driver_analysis_cpuid_validate.py` and `check_validate.py`.

### Custom CPUID

Native driver emulation verified:

```text
(EAX, ECX input)                    -> (EAX, EBX, ECX, EDX output)
(0x4ffffffd, 0xacf2077)             -> (4ffffffd, a29a6108, 41434631, 0)
(0x4ffffffd, 0xacf2078)             -> (4ffffffd, 7580794a, 41434631, 0)
(0x4fffffff, 4)                    -> (4fffffff, 43453032, 4241434b, 414c4953)
```

General leaf 0x4ffffffd returns EBX = mix32(subleaf ^ 0x9c3017a5) ^ 0x43453032 ^ 0x73d45bc1. mix32 uses XOR>>16, multiplication by 0x7feb352d, XOR>>15, multiplication by 0x846ca68b, XOR>>16. Constant 0x43453032 comes from driver alias-backing initialization.

### Hypercalls and instruction emulation

VMMCALL ABI:

```text
RCX = 0x43434248564c4142
RDX = operation
R8/R9/R10 = a/b/c
RAX = additional argument
```

The driver's ARM64 interpreter is at `0x140001260` in the driver image. It accepts 1–64 instructions and executes at most 256 steps, modeling 32 64-bit registers and NZCV. Relevant operations include MOVZ/MOVK, AND/OR/XOR, CMP and B/B.cond. **200 randomized programs matched native driver execution in Unicorn.**

- Operations 0x3100–0x3106 manage ARM sessions; 0x31ff returns version 0x20000.
- Operations 0x3201–0x3203 register ARM-backed x86 instruction overrides, with target next-RIP + R10 delta (1..64).
- Descriptor fields: register index bits 0..3; width bits 8..10; flag behavior bit 11; boolean operation bits 12..13.
- Register numbering: rax, rcx, rdx, rbx, rsp, rbp, rsi, rdi, r8..r15.

Operations 0x3301 and 0x3302 register hidden control/read traps. Decoded target:

```text
ROR64(((encoded1 ^ encoded2) - base * 0x9e3779b97f4a7c15) mod 2^64, 17)
```

For 0x3302: source instruction RIP=R8, base/fault key=R9, encoded pair=(R10,RAX).

**Kind-3 read-fault semantics:** set R10 to the decoded backing address, then retry the MOV load. Do not substitute the backing pointer itself for the loaded value. `driver_analysis_hv.py` exposes `Hypervisor`, `hook_code`, `handle_exception`, `resolve_fault`, `.traps` and `.overrides`.

EXE generic hypercall wrapper: `0x14005cff0`. Trap-registration wrapper: `0x14005cf80`; parameters RCX=source, RDX=fault key, R8=encoded1, R9=encoded2; VMMCALL at `0x14005cfdf`. No direct E8 call reference to that wrapper was found; calls may be virtualized.

### Cryptographic sessions

`check_hypercall.py` models SipHash-2-4, dynamically keyed capability/check sessions, and tickets. Capability channels use four steps around operation 0x3000; check sessions use nine steps around 0x3050. Ticket operations 0x2077/0x2078 include:

```text
ROL32(value ^ 0xa3c59ac3, 9) + op * 0x045d9f3b  (mod 2^32)
```

Model comparisons against the original driver succeeded. Some hardware counters are simplified in the emulator; these tests do not prove all surrounding Windows startup behavior.

The nine-step routine at `0x141617298` (original 0x14005d220) is a **GUI heartbeat**, not the flag checker. Its identified caller `0x141623322` updates app state+0x1b4. Do not spend more time mistaking that routine for flag verification.

## Deobfuscation artifacts

- `driver_analysis_deobf.py`: removes 225 inert save-all/restore-all CPUID/capability guards and folds 32 valid ARM instruction overrides into equivalent x86.
- `driver_analysis_thunks.py`: evaluates 24 environment-dependent constant thunks under two distinct initial register sets; all 24 resolved on the fully restored image.
- Useful outputs: `driver_analysis_initialized_deobf.bin`, `driver_analysis_initialized_thunks.bin`.
- Root `checker_ready.bin` is a deobfuscated initialized image.
- `check_unmutate.py`: cancels inverse operations in reachable checker control flow, removing **61,206 identity instructions in 4,706 PUSHFQ/POPFQ regions**.
- `check_clean.bin` is the latest convenient analysis image. The known first-block output is preserved.

Earlier `*_final_*` outputs are based on the pre-initialized image, so retain their distinction. A simplified image alone is not a replacement for the initialized runtime heap when running virtualized readiness code.

## Actual flag checker

Call path identified:

1. GUI routine `0x14161d399` (original 0x1400661d0) reads input pointer [state+0xe8] and length [state+0xf0], trims Unicode whitespace.
2. Calls wrapper `0x141614b34` with pointer and length.
3. Actual checker entry `0x14166fe79` (original stub 0x140698990).
4. Prologue saves input pointer in RDI and length in RBX; invokes anti-debug `0x14161345b` and timing helper `0x140698930`.
5. Native length check at `0x1406989ca`: CMP RBX,0x43.
6. Readiness call `0x1406987c0` redirects into virtualized `0x141492b91`.
7. The isolated transform body starts at **`0x140698a19`**.

Harness layout:

- 72-byte state buffer at RSP+0x50, initially zero.
- 0x20b0-byte workspace at RBP-0x60, equivalently RSP+0xa0.
- Isolated harness sets RBP=RSP+0x100.
- Stage ABI: RCX=input pointer, RDX=state, R8=workspace.
- Approximately 70 calls comprise transforms, hidden loads, comparisons and reduction.
- Nine independent eight-byte blocks; final input block begins at byte 64 and contains three input bytes plus padding.

First five transform stages: original entries 0x140601e80, 0x1406052b0, 0x140608660, 0x14060bb60, 0x14060f150. First redirects to 0x14126f3ea.

First hidden-load helper: `0x14060fd90`; faulting MOV at **`0x14060fd9a`**. It reads sentinel 0x600d00000000 through R10 and stores a QWORD at workspace+0x348. First comparison helper: `0x14060fdb0`.

Final stage: original 0x140697d50 -> `0x1413f20a8`; result observed at `0x140698edb`. A unary lookup maps zero to one and all other values to zero, so **EAX=1 is the expected success value**. The initial EAX=0 interpretation was incorrect. Downstream code inverts this into an error boolean. A real recovered candidate still needs end-to-end validation.

Known concrete vector, first eight input bytes `ctfcup{A`:

```text
state_00 = 0xc4941923
state_04 = 0x9b305062
combined QWORD = 0x9b305062c4941923
```

`probe_first_block.py` / `probe_first_block.json` enumerate all 63 possible eighth characters from [a-zA-Z0-9_] with prefix ctfcup{. These are probes, not flag candidates.

## Arithmetic lookup tables

The tables are plaintext and implement elementary arithmetic:

- Global 0x140f33558 -> row pointers 0x140f33560 -> data 0x140f33d60: XOR8.
- Global 0x140f43d68 -> rows 0x140f43d70 -> data 0x140f44570: AND8.
- Global 0x140f54578 -> rows 0x140f54580 -> data 0x140f54d80: OR8.
- Seven globals from 0x140f64d88 through 0x140fc7de8: funnel shifts `((x << n) | (y >> (8-n))) & 255`, n=1..7.
- Global **0x140fd85f8** -> row-pointer array **0x140fd8600**, 131072 pointers; each is `0x1410d8600 + 4*x`.
- Data at 0x1410d8600 is uint32 identity 0..131071. Indexing row[x][y] implements x+y, not a collection of unrelated tables.
- Unary global **0x141158608** -> **0x141158610** has [1,0,0,...] and tests zero.

First-block workspace constants: +0x14=c0de2034, +0x18=6a09a567, +0x1c=bb24ae85, +0x20=a5a5d31f.

Useful files: `lut_catalog.py/json`, `check_scan_tables.py`, `check_tables.json`, `check_luts.py`. **`lut_all_rows.json` contains a misleading decomposition of the large addition table into 512 chunks; do not adopt that interpretation.**

## Symbolic model and last executed work

`check_symbolic.py` runs concrete Unicorn execution alongside Z3 shadow registers/memory. It handles partial-register writes and translates LUT access to arithmetic. It tracks unsupported/junk instruction counts; concrete validation is essential.

Verified:

- First two stages: 18,558 instructions; no symbolic-memory validation mismatch.
- Latest first complete block in `check_clean5fast.log`: 33,166 instructions, 518 symbolic memory bytes, **VALIDATION_BAD 0**.
- `check_state.smt2`: latest verified first-block model, approximately 190 KiB.
- Inputs use 32-bit `input_word_00` / `input_word_01` (with byte extraction); output names in the current model are `state_00`, `state_04`.
- `check_solve_block.py`, given the known first-block target and the seven-character prefix, recovered eighth character A in approximately 0.65 s.
- An unrestricted 64-bit inverse query timed out at 30 s. That is a solver limitation/result, not evidence that the ciphertext is invalid.

Last all-block command:

```bash
python check_symbolic.py check_clean.bin \
  --transforms-only --word-input --no-workspace --validate \
  --output check_all_states.smt2
```

`--transforms-only` skips missing hidden loads and comparisons; it extracts transform equations and does not verify a flag.

At stop, `check_all_states.log` ended:

```text
STAGE 55 PC 0x140698dd7 ... SYMBYTES 3731 UNKNOWN 7251
STAGE 56 PC 0x140698de8 ... SYMBYTES 3748 UNKNOWN 7257
FINISHED 173.8435618877411 INSTRUCTIONS 273082
```

The process was stopped before validation/export completed. **`check_all_states.smt2` did not exist at the archival check.** Native execution finishing is not the same as a completed validated symbolic artifact. No independent block files have been generated.

Other useful files:

- `check_stage_map.py/json/log`: stage inputs, outputs and offsets.
- `check_split_states.py`: would split a complete symbolic state into independent block equations.
- `unpack_graph.py/txt`: expression inspection.
- `unpack_reduce.py`, `unpack_reduce_report.json`, `unpack_reduced.smt2`: sampled/proved SSA simplifications, reduced first-block model ~104 KiB.
- First-block transform was tested and is not GF(2)-affine.
- A final inverse query on the reduced model was interrupted/stopped; no solution was observed. Do not report it as successful.

## Precise unresolved hidden-read problem

At **0x141158710** are eleven static triples `(QWORD A, QWORD B, sentinel)`. Sentinels are 0x600d00000000 + i*0x200000. Repeated sentinel globals appear at 0x141158818..0x141158868.

First pair:

```text
A = 0xbe0a53af617f3043
B = 0xb166f4c5b87e2e61
```

Second pair:

```text
A = 0x5a5f26ac37da7acf
B = 0xe73afa319942293d
```

Direct application of the driver's 0x3302 pointer decoder to these table triples produces noncanonical garbage. Some initializer performs additional processing; the table is not directly a ready-made trap map.

The first comparison helper unmasks the actual loaded QWORD:

```text
expected_low32  = loaded_low32  ^ 0xc47eb41e
expected_high32 = loaded_high32 ^ 0x638acb6f
expected_ciphertext = loaded_qword ^ 0x638acb6fc47eb41e
```

It compares this to computed words at workspace+0x334 / +0x344. `check_compare0.asm` preserves the evidence.

Two rejected hypotheses, with prefix ctfcup{ and every possible eighth character:

- expected = A ^ B = **0x0f6ca76ad9011e22**: UNSAT; concrete probes also reject it.
- expected = (A ^ B) ^ mask = **0x6ce66c051d7faa3c**: UNSAT.

**Need the actual QWORD read from backing memory.** Neither the encoded pair nor the decoded backing address is automatically that QWORD.

### Attempts to obtain the registration map

`checker_emu.py` can run the isolated transform and obtain the known first-block result. Without a valid map it stops at the first sentinel read.

- `checker_traps.json` is currently **{}**, not a working solution.
- `driver_analysis_traps.pkl` is an empty map.
- `checker_events.json` is not evidence of successful target registration.
- `--init` restores the initialized checkpoint and enters readiness at 0x1406987c0.
- `--full` enters checker 0x14166fe79 with raw RCX=input, RDX=67 and bypasses timing helper 0x140698930 with RAX=1.

Readiness redirects into 0x141492b91 and eventually reaches virtualized return at **0x141541b37**. Observed RAX=0xdeadc0de; RSP is one QWORD below the expected return, with zero on top and the expected return address intact at RSP+8. Execution returns to zero. No 0x3302 registration events were observed. This occurs in both direct readiness and whole-checker entry.

- Restoring initialized heap fixed the earlier address-0x10 fault, but not this later failure.
- Matching normal CPUID to the loader did not fix it.
- Adding the driver's leaf-1 hypervisor bit did not fix it.
- No RDTSC/RDTSCP executes before this failing return, so changing deterministic timing alone did not explain this path.

Anti-debug function 0x14161345b calls GetCurrentProcess, CheckRemoteDebuggerPresent, NtQueryInformationProcess classes 7/30/31, and IsDebuggerPresent. It returns without registering the needed hidden reads.

CRT exploration:

- C++ init array 0x1406e4a50..0x1406e4a78 includes 0x140699e75, 0x14069914c and **0x1405e3670**.
- init_e array 0x1406e4a80..0x1406e4a98 includes 0x140699084 and 0x14069913c.
- Calling 0x1405e3670 directly only reached GetCurrentThreadId, without 0x3302.
- OEP/CRT emulation reaches Rust startup and AddVectoredExceptionHandler(handler **0x14038d7c0**); it stops at the unmodeled API. No trap registrations before that point.
- These are incomplete startup attempts, not proof that startup contains no required registration.

Logs/scripts: `driver_analysis_ready.py/log`, `driver_analysis_init.py/log`, `driver_analysis_constructor.py/log`, `driver_analysis_crt.py/log`.

## Suggested continuation, only if the user resumes solving

1. Restore the initialized image **and** initialized memory/context.
2. Locate/execute the true trap-mapping initializer, lazy readiness path, or exception-based setup.
3. Explain the 0xdeadc0de / displaced-stack return before changing assumptions about the ciphertext.
4. Collect actual 0x3302 registrations and read the backing QWORDs for all nine comparisons.
5. Apply each comparison's own mask; do not assume the first block's mask applies globally without checking.
6. Finish validated independent block extraction. Invert each block; use prefix, closing brace and allowed alphabet.
7. Check the candidate in the full native/model pipeline with negative controls and, if possible, the actual challenge interface.
8. Only then report a flag and create the requested successful writeup.

Do not resume unrelated heartbeat analysis or assume A^B is the answer.

## Artifact priorities and archival policy

The local task directory contains about 1.4 GiB, mostly duplicate 38-MiB image snapshots and checkpoint variants. Nothing was deleted.

Highest priority:

- Original challenge attachment and extracted driver/EXE.
- `unpack_initialized_state.pkl.gz`: matching complete runtime state, including the initialized image in its memory list.
- `unpack_initialized.bin` and `unpack_initialized.exe`: local ready-to-use convenience forms.
- `check_clean.bin`: current simplified checker image.
- All task-created Python scripts, small JSON/SMT files, useful validation/disassembly logs.
- This handoff and the artifact inventory.

Offline unpacker regeneration additionally depends on `unpack_resolved.bin`, `unpack_memory.bin`, `unpack_final.bin` and `unpack_decomp_state.pkl.gz`. Those are preserved locally. The archived initialized state makes rerunning this fragile sequence unnecessary for immediate continuation.

Known exploratory/wrong snapshots: `unpack_targeted.bin`, `unpack_target32.bin`, `unpack_keyprobe.bin` and index-skipping attempts such as `unpack_skip*`. Retained for provenance, never preferred over initialized state.

The Git checkpoint stores selected critical compressed binary snapshots, original inputs, scripts, small models and evidence. An inventory records all local files without copying every duplicated large dump. Packaging/decompression helpers must create new files and refuse to overwrite existing ones.

## Git context and contribution review

The workspace unexpectedly inherits a Git repository rooted at the user's home directory, not at this challenge. It has unrelated untracked personal files and a pre-existing README deletion. **Do not run git add . or stage the home repository.**

To avoid touching those files, a separate clone was created at:

`/private/tmp/cybercup-progress-repo`

Remote:

`https://github.com/Karatinos/git-slopi-farm.git`

Dedicated branch:

`ctf/cybercup-2077-progress`

Base origin/main at checkpoint preparation: `3076b7e006a68242f9fa0e675b4d138ba5b9220d`. Only explicit challenge paths are staged/published. No force-push or destructive synchronization is authorized. If another agent updates the same branch, fetch/read it and stop publication on divergence instead of overwriting their work.

Other contributions reviewed during checkpoint preparation:

- origin/master at `13444a623e693714abf6395d6b02b52cdb3af235`: archive-member reconnaissance, PNG metadata extraction, apex CLI prototype, hardened endpoint parsing, additional decoders and MCP tooling. These are general CTF automation changes, not a CyberCup solution.
- New origin/ctf-progress/iso-codex at `a69154568abf0edaf35460f7258dff4f47b61a75`: separate Iso challenge progress and analysis checkpoint. Read in its own branch; no modifications to its files and no claim that its task is solved.

This file describes analysis state at the stop. Git commit IDs, synchronization status and subsequent remote contribution observations belong in separate checkpoint/sync records, so the paused solving findings remain distinguishable from later repository activity.

