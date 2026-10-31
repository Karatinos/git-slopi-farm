# Connectome investigation — unresolved

No flag has been recovered. Do not treat any probe's incidental `ctf{` match as a solution. The user requested `writeup.md` only after a correct flag is confirmed; that file has not been created.

## Latest checkpoint (2026-10-31)

- The user confirmed there are no additional hints: only the two original attachments.
- **The platform rejected `ctfcup{key_in_the_fly_brain}`. Do not resubmit or report it as solved.** This was a language-based candidate, not a cryptographically recovered plaintext.
- Under a plausible shortest-path segmentation, that candidate also has an internal inconsistency: the `y` in `key` would map to index 3953, while the `y` in `fly` would map to index 1362. A one-to-one static character codebook cannot do that.
- `routes.py` compares path segments against unweighted and weighted shortest paths, and against canonical BFS routes under several neighbor orders. The minimum unweighted segmentation has 27 destinations; sorted-ID unidirectional BFS needs 30. Ordinary weighted and inverse-weight shortest paths fail to explain every supplied edge.
- `bidirectional_probe.py` now tests the usual bidirectional BFS algorithm with six neighbor orders. Sorted-ID order matches 24 of the 28 tentative segments. The four mismatches are positions 7–10, 35–39, 44–47, and 47–51. Thus the tentative segmentation plus that routing rule is not an exact reconstruction.
- Selecting visited nodes among the 256 lowest values of `indegree * outdegree` gives a remarkably coherent candidate destination set. This is a heuristic, not a proven selection rule. Removing the intermediate index 3987 at position 8 gives 28 destinations.
- The tentative 28 endpoint positions are: `1,4,5,7,10,13,15,18,19,21,24,27,29,32,34,35,39,42,44,47,51,54,56,58,61,64,66,68`.
- If the prefix is `ctfcup{`, the corresponding tentative mappings are `c=3967, t=3964, f=95, u=3941, p=2096, {=3942`. Repeated node 3564 plausibly means `_`, but neither this nor the whole segmentation is verified.
- `centrality_probe.py` computed weighted/unweighted left/right eigenvector centrality, PageRank at several damping factors, and HITS hub/authority scores. Their global ranks, shifts, reversals, and residues did not yield a convincing prefix. Results: `centralities.npz`, `centrality-results.txt`.
- `full-degrees.npz` now contains **unweighted** incoming/outgoing degrees from the complete public v1.0 traced graph. These are distinct from the weighted strengths already cached in `graph-v1.0.npz`. Direct byte values do not explain the flag. For example node 3967 has full in/out degrees 283/145, not ASCII `c`.
- Node order by first appearance in the CSV/public edge list (source, destination, or both) was checked and gives no simple readable mapping.
- `stat_probe.py` tested 1,008 graph statistics (degree/strength and combinations, exact weights, weight thresholds, bit predicates, including full traced graph threshold degrees). Direct values, global ranks, additive/XOR offsets, and residues did not yield a convincing prefix. One five-character partial match was accidental; see `stat-results.txt`.
- The cipher and character mapping remain unknown. Next useful work: identify the character-to-neuron mapping from graph or public metadata, and check routing restrictions or alternate segment boundaries. Avoid further unconstrained flag guesses.

## Verified facts

- Original files are `../connectome.txt`, `../adjacency.csv.gz`, and `../message.bin`.
- The clue *corpora pedunculata* means mushroom bodies.
- CSV has 692,164 distinct directed edges, no self-loops, and 4,096 distinct neuron IDs.
- `message.bin` is exactly 276 bytes: 69 little-endian uint32 values.
- These values index the **numerically sorted union of all CSV node IDs**. Every one of the 68 consecutive transitions is a directed CSV edge.
- Start index is 0 (bodyId 10013).
- The graph is the induced **MaleCNS v1.0** connectome on 4,003 Kenyon cells and 93 MBONs. The selected IDs appear to be the first 4,096 sorted IDs from these classes.
- The public v1.0 induced graph matches every challenge edge. Its only extra edges are self-loops `(523060,523060)` and `(157281,157281)`, explaining their removal.
- The challenge CSV is globally sorted by decreasing synapse weight. Equal-weight ordering differs from the public source row order.
- v0.9 is close but not exact; use v1.0 for further work.

Message indices:

```text
0,3967,7,94,3964,95,2083,3967,3987,11,3941,5,100,2096,11,3942,15,11,2488,3824,1,3953,3,3356,3564,5,1338,1227,11,121,1005,2923,3564,5,3964,62,1958,3971,2401,3824,1,914,3564,1,95,1,11,3813,15,11,1,1362,1,914,3564,5,64,3771,155,11,899,3475,5,1338,1227,11,121,808,3235
```

Actual neuron IDs:

```text
10013,520395,10816,36043,520186,36094,93017,520395,524893,11402,513387,10704,36482,93325,11402,513391,11805,11402,108072,190056,10079,519128,10495,147040,161865,10704,76436,74368,11402,38859,69501,128467,161865,10704,520186,26485,89461,521526,104448,190056,10079,67282,161865,10079,36094,10079,11402,187741,11805,11402,10079,76688,10079,67282,161865,10704,26853,180332,41692,11402,66865,154509,10704,76436,74368,11402,38859,64023,141007
```

Corresponding public edge weights:

```text
1,1,1,5,3,1,2,1,1,1,1,1,1,4,8,1,1,1,6,21,1,1,4,1,3,1,1,18,3,1,1,4,3,11,4,1,2,1,1,21,1,1,5,54,1,29,1,14,1,15,3,29,1,1,3,1,1,3,1,1,1,2,1,1,18,3,1,1
```

## Useful files and sources

- Official download page: https://male-cns.janelia.org/download/
- Public bucket prefix: `https://storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/`
- `annotations-v1.0.feather`: complete correct neuron metadata, 211,577 rows.
- `neurotransmitters-v1.0.feather`: complete neurotransmitter predictions.
- `weights-v1.0-traced.feather`: complete correct 508 MB file, official name `connectome-weights-male-cns-v1.0-minconf-0.5-traced-only.feather`.
- `graph-v1.0.npz`: cached graph. `nodes` is sorted actual IDs; `edges` is an N×3 array of **local indices** `(src,dst,weight)`, includes the two self-loops; `incoming/outgoing` are weighted induced-graph strengths; `fullin/fullout` are weighted strengths in the complete traced dataset.
- `mb-out-weights-v1.0.json`: actual source ID → list of `[actual destination ID, weight]`, preserving public source row order, includes the two self-loops.
- `weights-v0.9.feather` is a complete older 1.1 GB dataset; most other unversioned graph/weight files use v0.9.
- `weights-partial.feather` is a **sparse incomplete** v0.9 file; never interpret it as complete.
- Python: use repository `.venv/bin/python`; numpy, scipy, pyarrow, pandas are installed.

## Rejected hypotheses / existing probes

No listed method produced a readable flag. Read scripts before repeating tests.

- Direct low bytes of message indices or body IDs, differences, simple affine edge formulas.
- Outgoing neighbor ranks in supplied CSV order, sorted ID order, reversed orders, string ID order, metadata order, degree/strength order, source-public row order. Incoming and undirected ranks were also tried in early ad hoc experiments.
- Mixed-radix integer reconstruction in both traversal directions, big/little byte orders, and several output alphabets.
- `prefix_probe.py v1.0`: local Huffman, Shannon–Fano, Shannon, Fano–Elias codes with uniform/synapse/degree/strength weights and many neighbor orders; bit reversal, offsets, 7/8-bit text. Also run on v0.9. `prefix-hits.json` has only a false positive inside garbage.
- `order_probe.py`: 274 distinct neighbor orders based on all annotation and neurotransmitter fields, numeric/string field values, hashes of values, and soma coordinate permutations. Tests mixed radix, uniform/weighted Huffman, and character-rank modulo degree. Completed without hits; `order-results.txt`, `order-hits.json`.
- `ans_probe.py v1.0`: weighted ANS reconstruction and exact arithmetic interval coding; uniform/synapse/log/sqrt/degree models; file/public/ID/type/instance/degree orders and reversals. Completed without hits; `ans-results.txt` contains nearest accidental prefix distances only.
- `group_probe.py`: codes over neighbor groups by type, instance, class, group, supertype, side, lineage, birthtime, NT category, and weight residues. Failed.
- `edge_hash_probe.py`: common hashes of edge IDs/indices/types/instances/weights in numerous encodings; digest bytes and alphabet residues. Failed.
- Hashes of node attributes as byte labels allowing short intervening paths were tried; no convincing known-prefix subsequence.
- Direct node degrees, weighted strengths, coordinate components and their global ranks modulo 256/128/39/95 do not supply a plausible `ctfcup{` subsequence near the start.
- v0.9 full outgoing-neighbor lists (including untraced segments), filtered in several ways, did not produce simple neighbor-rank plaintext.

## Structural observations for further reasoning

- Most repeated small indices are MBON hubs: 1=10079 MBON06, 5=10704 MBON11, 11=11402 MBON11.
- Node 3967 (520395 MBON15) has only five outgoing neighbors, all weight 1: sorted `[10816,13728,21242,520151,524893]`. Its two early visits choose the first and last neighbors.
- Total unweighted walk information `sum(log2(outdegree))` is about 455.7 bits. A 68-byte arbitrary payload cannot be encoded injectively with one transition per byte on this walk; variable-length or restricted-alphabet encoding remains possible.
- The repeated path `[5,1338,1227,11,121]` appears at positions 25–29 and 62–66 (offset 37). This matters when testing nibble encodings because parity changes.
- Some low-index vertices could be routing steps between encoded destinations, but this remains unproven. Plain sorted-neighbor BFS does not match all plausible boundaries for a `ctfcup{` prefix.
- Example early shortest paths: 0→3967 direct; 3967→94 via 7; 95→3967 via 2083. But 94→95 would route through index 5 under sorted-neighbor BFS, whereas the actual walk goes through 3964. Thus that simple segmentation/order is rejected.
- No encryption source, known key derivation, or verified decoding rule is available yet. Avoid presenting speculative mappings as evidence.
