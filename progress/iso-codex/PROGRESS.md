# Iso — detailed progress and resumption handoff

**Status: UNSOLVED. No verified flag has been recovered. Solving was stopped at the user's request on 2026-10-31. Only the separately requested ten-minute GitHub synchronization should remain running.**

This is a progress report, not a successful writeup. `writeup.md` has deliberately not been created: the original request made it conditional on recovering a correct flag. Do not mistake dummy strings in self-tests for the challenge flag.

## Task and files

The actual challenge directory is `/Users/karatinos/Downloads/Staff/fsp/crypto/Iso`. The originally requested `reverse/Iso` path does not exist. The parent workspace is `/Users/karatinos/Downloads/Staff/fsp`.

The statement, `Iso.txt`, says:

> Iso — 964 points / 4 solvers — crypto
>
> Instinct only goes so far, skill covers the rest.

The attachment is `iso.tar.gz`. Its extracted substantive files are `iso/iso.sage` and `iso/output.txt`. The generator is:

```python
#!/usr/bin/env sage
with open('flag.txt', 'rb') as file:
    flag = file.read().strip()
    assert len(flag) == 27

p = next_prime(getrandbits(128))
E = EllipticCurve(GF(p), j = int.from_bytes(flag, 'little'))

for _ in range(64):
    E = choice(E.isogenies_prime_degree(2)).codomain()

print(x^3 + E.a4().lift_centered() * x + E.a6().lift_centered())
```

The complete output is:

```text
x^3 + 6079433314242371108270239373533376748*x - 1779744368654530162000920720207404089
```

Throughout this report:

```text
A = 6079433314242371108270239373533376748
B = -1779744368654530162000920720207404089
```

The expected flag is `ctfcup{` followed by 19 unknown bytes and a final `}`. The source enforces 27 bytes, but does not itself enforce printable text; printability is a reasonable flag-recovery assumption.

Because the printed coefficients are centered representatives, the hidden prime satisfies `p > 2*A`. Since it is the next prime above a 128-bit random integer, its upper bound is essentially `2^128` (allow a tiny next-prime overshoot). Consequently a relevant factor has roughly 124–128 bits, or 38–39 decimal digits. Small factors found below are not candidates for the field prime.

Archive inspection found macOS AppleDouble/PAX metadata but no additional challenge secret. The metadata mentions author username `keltecc`. Source and output modification timestamps were `1792610198.084473776` and `1792610200.689522431`. They do not reveal the RNG seed.

## Established mathematical attack

### Sage's starting model

For generic `j` in a field of characteristic other than 2 or 3, Sage constructs:

```text
k  = j - 1728
a0 = -3*j*k
b0 = -2*j*k^2
```

The input integer is coerced into `GF(p)` before this construction. The special cases `j=0` and `j=1728` use other models; the attack below assumes the generic case. Such special values are overwhelmingly unlikely for an independently sampled prime and ordinary flag, but have not been ruled out by a recovered prime.

The formula was checked against Sage source and actual Sage executions. The constructor's rational-field minimal-twist behavior does not apply to this finite-field call.

If a model is scaled to `a=u^4*a0`, `b=u^6*b0`, put `s=u^2`. It obeys:

```text
F0(a,b,s) = 4*a^3 + 27*b^2 + 31104*s*a*b = 0  (mod p).
```

**31104 is the correct constant. An early exploratory attempt used 10368; that was corrected. Do not revive that incorrect relation.**

### Normalized degree-two isogenies and backtracking

For a rational kernel point `(r,0)`, where `r^3+a*r+b=0`, the normalized degree-two quotient has:

```text
a' = -4*a - 15*r^2
b' = 22*b + 14*a*r
```

The normalized dual has kernel root `-2*r`. A quotient followed by its normalized dual sends `(a,b)` to `(16*a,64*b)`.

Deleting consecutive dual pairs from a 64-step walk leaves an even reduced length `d`. Starting at the observed output and taking the `d` dual steps back reaches a model with:

```text
a = -3*j*(j-1728)   * 2^(128 + 2*d)
b = -2*j*(j-1728)^2 * 2^(192 + 3*d)
s = 2^(64+d).
```

These powers are important: at `d=2`, use `s=2^66`, not `2^64`.

Ordinary 2-isogeny graphs often cause extensive backtracking. A small simulation of randomly generated instances found many reduced lengths zero, several two, and occasional four or larger. This motivates trying `d=0,2,4,6`; it does not prove that the real instance has any particular reduced length. A simulated walk also reached length 10, so a longer real path remains possible.

`analysis/validate_walk.sage` directly generated Sage curves and 64-step walks, reduced paths by comparing j-invariants, and verified the derived relations modulo the generated primes. Tests included the zero-, two-, and four-step relations. They passed.

### Norm recurrence

`analysis/walk_relations.py` uses python-flint multivariate polynomials in `(r,A,B,s)`, lexicographic order. It starts from `H0=F0`.

For a polynomial `H`, substitute the quotient coefficients and reduce modulo `r^3+A*r+B`, obtaining `q=c0+c1*r+c2*r^2`. Its norm is:

```text
c0^3 - 2*A*c0^2*c2 + A^2*c0*c2^2 + A*c0*c1^2
+ 3*B*c0*c1*c2 + B^2*c2^3 - B*c1^3 - A*B*c1*c2^2.
```

This enumerates the three possible first degree-two isogenies algebraically. To remove backtracking when constructing `H2`, divide by the primitive part of `H0(16*A,64*B,s)^3`. When constructing `H_(d+1)` for `d>=2`, divide by the primitive part of `H_(d-1)(16*A,64*B,s)^2`. Normalize the resulting polynomial to primitive coefficients and positive leading coefficient.

The hidden prime must divide:

```text
N_d = abs(H_d(A,B,2^(64+d)))
```

if `d` is the actual reduced path length. The recurrence generated `H1.json` through `H6.json` and `primitive_n1.txt` through `primitive_n6.txt`. Sizes are:

- `H1`: 13 terms; evaluated integer 346 decimal digits.
- `H2`: 42 terms; 710 digits.
- `H3`: 149 terms; 1,441 digits.
- `H4`: 561 terms; 2,924 digits.
- `H5`: 2,177 terms; 5,934 digits.
- `H6`: 8,577 terms; 12,039 digits.

Generation through degree six took a few minutes; the final stage alone took about 248 seconds in the first run. `H6.json` is about 9 MB locally. The Git snapshot can omit that large generated file because the generation script and evaluated integers are retained.

The two-step result was also derived independently with SymPy resultants in `analysis/resultant.py`. That older script's `n2.txt` includes an extra constant factor `2^36`; prefer `primitive_n2.txt`. Re-evaluation of `H2.json` at the published A, B and `s=2^66` exactly reproduced the saved primitive integer. The current cofactor was separately checked against that integer and all removed factors.

Factoring the symbolic `H2` over the integers, and again after substituting `s=2^66`, returned a single irreducible factor. There was no easy rational polynomial factorization that reduced the integer-factorization problem.

## Factoring results and exact checkpoint

### Reduced length zero is ruled out under the generic-model assumption

The integer

```text
4*A^3 + 27*B^2 + 31104*2^64*A*B
```

has complete factorization:

```text
3^6
* 2756099
* 38647261059053
* 849730274370727147067
* 13621568982086690577957595834791154260655747086184118105900367481087
```

The last factor is prime and has 224 bits. None is in the required 124–128-bit interval. The 224-bit factor was additionally tried as an out-of-range diagnostic: its recovered j-value does not decode to a flag and it contradicts the generator's prime size.

Several alternative scaling exponents were queried as diagnostics in `other_scalings.json`. They did not produce a solution and are not substitutes for the correctly derived exponent 64.

### Reduced length two: current primary candidate

The complete removed factor is:

```text
3^36
* 4517
* 43385229945689
* 200573683479693692659464438760837
* 2260875122210404084952664589
```

The last three factors were found with GMP-ECM. They have 14, 33 and 28 decimal digits, respectively, and are too small to be p.

The remaining **616-digit composite** is saved in `analysis/n2_current.txt`:

```text
1457506062875932817869177975145756628778829486130694151675619410000045233025452318197087491186659039504564609855820125742244854384953937587718871938163914748886160827115674300836373948031539315693609126200833021512260426564405247620393241717756612569519174506217307654295046339196604177967426998112643020893194149880926399070708798100193542243954578877626636216188267061594182902222212311125262838762245222060004758747396821275609416435361794797593067428291811253805770902740232478897198198644156741483763383085132396412471374750529542481663134137726652394951656939253795325420794562139234602187068800874902822025171
```

Verified exactly:

```text
primitive_n2 = n2_current * 3^36 * 4517
              * 43385229945689
              * 200573683479693692659464438760837
              * 2260875122210404084952664589.
```

Intermediate files preserve earlier checkpoints:

- `cofactor2.txt` / `n2_cofactor.txt`: 689 digits, after removing `3^36*4517`.
- `n2_work.txt`: 675 digits, after also removing the 14-digit factor.
- `n2_next.txt`: 643 digits, after also removing the 33-digit factor.
- `n2_current.txt`: 616 digits, after also removing the 28-digit factor.

FactorDB queries did not supply a target-sized factor. The latest query of the 616-digit cofactor returned status `C`. The JSON responses are saved locally.

### Reduced lengths four and six

- `cofactor4.txt` is the 2,855-digit cofactor after removing `3^144` from the four-step relation. FactorDB additionally identified `212923`; check divisibility before removing it from the saved file, which was not necessarily updated with that factor.
- `cofactor6.txt` is the 11,764-digit cofactor after removing `3^576` from the six-step relation.

Neither has been factored sufficiently to test a field prime. No evidence proves that the real prime divides the two-step candidate rather than one of these or a longer-path relation.

### ECM and p±1 work performed

Initial ECM used a Debian ARM container with GMP-ECM 7.0.6. Runs included about 80 curves at B1=250,000 on an earlier cofactor, plus runs at B1=1,000,000. The saved `ecm_work.log`, `ecm_big.log`, `ecm_next_1.log`, and `ecm_next_2.log` record the actual work and factors.

A four-process container run on the 616-digit cofactor used two workers at B1=1,000,000 and two at B1=3,000,000. It found no additional factor before being replaced by a native build.

Homebrew GMP-ECM 7.0.7 was then installed and used natively, with `OMP_NUM_THREADS=1` per process. `factor_native.py` ran three B1=1,000,000 workers and one B1=3,000,000 worker. Typical stage-one times ranged from about 24 to 40 seconds for B1=1,000,000 as CPU load changed. The run was stopped at the user's request without finding another factor. Consult `factor_native.log` for exact completed curves; an interrupted curve is not a completed test.

`residues_0.txt` through `residues_3.txt` save completed stage-one residues. They can potentially be resumed with a larger second-stage bound. These files are valuable: restarting the script otherwise selects new curves and does not automatically continue the saved residues.

A larger native Pollard p-1 run used B1=30,000,000 and requested B2=300,000,000,000; GMP-ECM selected B2=364,641,377,340. It completed without a factor. The log and residue are `pm1_native.log` and `pm1_native.residue`. Earlier smaller p-1 and p+1 attempts are `pm1.log` and `pp1.log`; they did not find the required prime.

The remaining factorization is computationally expensive. Failure of these limited randomized runs is not evidence that the two-step relation lacks the correct prime.

## Recovery once a candidate p is found

`analysis/recover_from_p.sage` is prepared for this step:

1. Check primality and that p exceeds twice the largest absolute output coefficient.
2. Construct `EllipticCurve(GF(p), [A,B])`.
3. Enumerate non-backtracking degree-two paths through depth six.
4. At even depth d, compute each endpoint's j and test BOTH exact scaled-model equations given above.
5. Lift each matching j to printable 27-byte flags with the required prefix and suffix.
6. Save matches and path kernel roots in `analysis/recovered.json`.

It accepts a decimal prime as an argument, or reads `analysis/candidate_p.txt`. No target `candidate_p.txt` or verified `recovered.json` was produced during the work.

Example for a future resumed session:

```sh
docker start iso-sage
cd /Users/karatinos/Downloads/Staff/fsp/crypto/Iso
docker exec iso-sage sage analysis/recover_from_p.sage DECIMAL_PRIME
```

The script has not been exercised against the real challenge prime, since that prime remains unknown. It should be reviewed and any candidate independently verified before reporting a flag.

### Lattice lift

`analysis/lift_flag.sage` implements bounded closest-vector enumeration for the 19 unknown bytes. Write:

```text
M = int.from_bytes(b'ctfcup{' + 19 zero bytes + b'}', 'little')
    + 256^7 * sum(x_i * 256^i, i=0..18).
```

Given `M ≡ j (mod p)`, the unknown byte vector satisfies one modular linear equation. The script builds a rank-19 integer lattice with first row `(p,0,...,0)` and rows having `-256^i mod p` in the first coordinate and 1 in coordinate i. It LLL-reduces the basis, shifts toward the printable-byte center 79, performs exact rational nearest-plane reduction to avoid floating-point loss on a large target, and enumerates with fpylll within squared radius `19*47^2+1`. Candidates are filtered to bytes 32–126 and checked against the modular equation.

A self-test using a fixed random-looking 128-bit prime recovered exactly one printable candidate, the chosen dummy flag. An earlier test prime unusually close to a power of two produced many artificial collisions; it was replaced. This was a self-test, not a challenge solution. The implementation caps enumeration at 100,000 candidates; if future input produces excessive solutions, revisit this bound and the character assumptions.

After finding a plausible flag, also construct an explicit valid 64-step forward path, using the recovered reduced path and the required dual backtracks, and compare both centered output coefficients exactly. Mathematical verification should precede the requested final `writeup.md`.

## Dictionary checks and performance work

These are optional shortcuts, not the main proof. No tested text has verified.

`candidate_polys.py` constructs cyclic-isogeny norm polynomials starting from `A-s` or `B-s`. For a guessed full flag integer J, evaluate the A-polynomial at:

```text
C = -3*J*(J-1728)*2^(128+2*d).
```

A correct guess at the correct reduced depth must give a gcd with `N_d` containing p. The B-polynomial and actual graph/model checks would then reject unrelated matches.

Completed searches included:

- About 114,028 initial phrase/leet variants at d=2, and the same initial set at d=4; no hit.
- An expanded per-character leet search of 1,693,020 additional candidates at d=2; no hit.
- A grammar-generated collection of 37,510 phrases, producing 2,351,704 global leet variants at d=2; no hit.
- A later common-variant scan at d=4 and d=6 was **interrupted at the user's request**. Its last observed progress was at least 238,134 candidates / phrase index 31,000 of 37,510; it had reported no hit. Do not describe this scan as complete.

Files: `dictionary.py`, `dictionary_expanded.py`, `dictionary_grammar.py`, `dictionary_fast.py`, and `grammar_phrases.json`.

`candidate_polys_deep.py` generated A-polynomials through d=6. `candidate_A1.json` through `candidate_A6.json`, and B-polynomials through d=4, are available.

An implementation improvement was to evaluate the integer polynomial directly with `flint.fmpz_poly` and reduce once, rather than perform modular reduction after every Horner step. Batch 256 values by multiplying modulo N, then compute one gcd and inspect the batch only on a hit. This substantially improves throughput. `bench_candidates.py` checks direct evaluation against the older modular implementation.

The flag might be a phrase outside these guesses, use a different substitution/capitalization, contain arbitrary bytes, or correspond to a longer path. Dictionary failure does not rule out the algebraic attack.

## Other investigated approaches

- Confirmed source/output bytes rather than relying on copied numbers.
- Inspected archive metadata; no flag or modulus was present.
- Examined Sage constructors, degree-two isogeny formulas, and RNG initialization. Normal Sage initialization obtains entropy from the OS, not just a timestamp.
- Tested Sage seeds 0–19,999 and selected familiar constants/timestamps near the archive times against the saved zero-, two-, four- and six-step relations. No match. See `seeds.sage`.
- Searched public material for the exact coefficients/task and the author's related repositories. No matching public solution was found.
- The statement is an Iso/Valorant quote; no additional mathematical clue was established from it.
- SageCell requests timed out; local Sage was installed and used instead.
- No remote challenge server, login, or submission endpoint is provided by the statement. The flag has not been submitted anywhere.

## Software and environment

Host: macOS ARM, zsh, eight logical CPUs. Useful installed environments:

- `analysis/mathenv/bin/python`: Python 3.10, python-flint 0.9.0, sympy and requests. This is the preferred native algebra environment.
- `analysis/venv`: older Python 3.9/python-flint environment; avoid it for the newer multivariate APIs.
- `/opt/homebrew/bin/ecm`: native GMP-ECM 7.0.7.
- Docker/OrbStack container `iso-sage`: Debian bookworm ARM, SageMath 9.5 and fpylll. The challenge directory is mounted at `/work`, which is its working directory.
- Container `iso-math`: Debian 13 ARM with PARI/GP and GMP-ECM 7.0.6. It has no task-directory mount; earlier jobs used `docker cp` or stdin.

Both containers were stopped, not deleted, when solving was halted. All artifacts and installed environments were retained.

Typical regeneration commands, **only if the user later resumes solving**:

```sh
cd /Users/karatinos/Downloads/Staff/fsp/crypto/Iso
analysis/mathenv/bin/python analysis/walk_relations.py
analysis/mathenv/bin/python analysis/candidate_polys_deep.py
docker start iso-sage
docker exec iso-sage sage analysis/validate_walk.sage
docker exec iso-sage sage analysis/lift_flag.sage
```

`factor_native.py` starts long-running jobs; do not run it merely to inspect progress. It was stopped by request. Before restarting it, review its factor handling and saved residue files, and consider whether more work on d=2 is justified versus other depths.

## Git synchronization and ownership constraints

The user explicitly requested a GitHub push every ten minutes and reading other agents' contributions, then explicitly stopped solving while keeping that synchronization active until the Codex tab is closed. They also instructed: **never delete files or edit files this agent did not add**.

The working directory inherits an unrelated Git repository rooted in the user's home directory. A separate checkout was therefore created at `analysis/collaboration`; never use a broad `git add` from the workspace/home repository. The remote is `https://github.com/Karatinos/git-slopi-farm.git`.

The dedicated progress branch is `ctf-progress/iso-codex`, with task material under `progress/iso-codex/`. Only explicitly selected files created during this work are copied there. Virtual environments, the nested checkout, unrelated home files, credentials, and task binaries are excluded.

`git_sync.py` is the only continuing work: it fetches remote branches without pruning, reads newly observed text contributions, appends a local contribution journal, copies the allowlisted Iso progress artifacts, commits changes on the dedicated branch, and pushes. It does not resume ECM, guessing, curve enumeration, or any other solving action. The loop runs as an attached terminal session and handles termination signals. Its PID, latest status and logs are retained under `analysis/`.

The initial remote inspection found `main` with a small README and `master` with the pre-existing CTF-farm framework. No Iso-specific contribution was visible at that point. Subsequent agent contributions should appear in `OTHER_AGENTS_UPDATES.md` and the sync log as the loop fetches them.

## Recommended next actions if explicitly resumed

1. Read this report, `n2_current.txt`, the factor logs and the latest contribution journal. Do not restart completed derivations or retest the same seeds blindly.
2. Decide whether to continue ECM on the 616-digit d=2 cofactor, resume stored residues with a larger second-stage bound, or investigate a different reduced depth/attack. The current bottleneck is recovering p, not lifting a known j to text.
3. For every factor in the allowed range, run the endpoint model checks and lattice lift. A size match alone is insufficient.
4. Independently verify the recovered flag against a full valid 64-step construction and the exact published A and B.
5. Only then return the flag and create `writeup.md` in this directory.

**Again: there is currently no verified Iso flag. Solving is stopped; only Git synchronization is authorized to continue.**
