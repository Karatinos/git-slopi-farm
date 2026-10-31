import collections
import csv
import gzip
import heapq
import json
import math
import struct
from pathlib import Path

import numpy as np
import pyarrow as pa

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
adj = collections.defaultdict(list)
rev = collections.Counter()
with gzip.open(ROOT / 'adjacency.csv.gz', 'rt') as f:
    rows = csv.reader(f)
    next(rows)
    for a, b in rows:
        a, b = int(a), int(b)
        adj[a].append(b)
        rev[b] += 1
nodes = sorted(set(adj) | set(rev))
message = struct.unpack('<69I', (ROOT / 'message.bin').read_bytes())
path = [nodes[x] for x in message]
weights = {a: {b: 1 for b in adj[a]} for a in set(path[:-1])}
cache = HERE / 'out-weights.json'
source = HERE / 'weights-v0.9.feather'
blocks = json.loads((HERE / 'batches.json').read_text())
schema = pa.ipc.open_file(str(HERE / 'weights-partial.feather')).schema
size = source.stat().st_size
cachedata = json.loads(cache.read_text()) if cache.exists() else None
start = 0
if cachedata:
    weights = {int(a): {int(b): w for b, w in d.items()} for a, d in cachedata['weights'].items()}
    start = cachedata['next_batch']
targets = list(weights)
with source.open('rb') as f:
    for j in range(start, len(blocks)):
        off, meta, n = blocks[j]
        if off + meta + n > size:
            break
        f.seek(off)
        batch = pa.ipc.read_record_batch(pa.ipc.read_message(f), schema)
        u, v, w = [col.to_numpy() for col in batch.columns]
        if w[0] == 1:
            print('All weights >1 have been read', flush=True)
            break
        mask = np.isin(u, targets) & (w > 1)
        for a, b, value in zip(u[mask], v[mask], w[mask]):
            if int(b) in weights[int(a)]:
                weights[int(a)][int(b)] = int(value)
    print('last batch', j, 'weight', w[-1] if 'w' in locals() else '?', flush=True)
cache.write_text(json.dumps({'next_batch': j, 'weights': weights}))
print('path weights', [weights[a][b] for a, b in zip(path, path[1:])], flush=True)


def huffman(a, mode, order, ties, canon, flip):
    neighbors = sorted(adj[a]) if order else adj[a]
    h = []
    for i, b in enumerate(neighbors):
        w = {'uniform': 1, 'weight': weights[a][b], 'indegree': rev[b],
             'outdegree': len(adj[b]), 'logweight': math.log2(weights[a][b]+1),
             'inverse': 1 / weights[a][b]}[mode]
        heapq.heappush(h, (w, i, b))
    count = len(neighbors)
    while len(h) > 1:
        p, q = heapq.heappop(h), heapq.heappop(h)
        tie = min(p[1], q[1]) if ties else count
        heapq.heappush(h, (p[0]+q[0], tie, (p[2], q[2])))
        count += 1
    codes = {}
    def walk(t, bits):
        if isinstance(t, int):
            codes[t] = bits
        else:
            walk(t[0], bits + str(flip))
            walk(t[1], bits + str(1-flip))
    walk(h[0][2], '')
    if canon:
        n, last = 0, 0
        for b in sorted(neighbors, key=lambda b: (len(codes[b]), b)):
            length = len(codes[b])
            n <<= length-last
            codes[b] = f'{n:0{length}b}'
            n += 1
            last = length
    return codes


best = []
prefix = b'ctfcup{'
for mode in ['uniform', 'weight', 'indegree', 'outdegree', 'logweight', 'inverse']:
    for order in [False, True]:
        for ties in [False, True]:
            for canon in [False, True]:
                for flip in [0, 1]:
                    codes = {a: huffman(a, mode, order, ties, canon, flip) for a in weights}
                    bits = ''.join(codes[a][b] for a,b in zip(path,path[1:]))
                    for offset in range(8):
                        for reverse in [False, True]:
                            chunks = [bits[i:i+8] for i in range(offset, len(bits)-7, 8)]
                            raw = bytes(int(x[::-1] if reverse else x, 2) for x in chunks)
                            score = sum((a^b).bit_count() for a,b in zip(raw,prefix))
                            best.append((score, mode, order, ties, canon, flip, offset, reverse, len(bits), raw))
                            if b'ctfcup' in raw:
                                print('FOUND', best[-1], flush=True)
print('BEST', *sorted(best)[:10], sep='\n', flush=True)
