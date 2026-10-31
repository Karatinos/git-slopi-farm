import collections
import csv
import gzip
import json
import struct
from pathlib import Path

import numpy as np
import pyarrow as pa

p = Path(__file__).resolve().parent
nodes = sorted({int(x) for row in list(csv.reader(gzip.open(p.parent / 'adjacency.csv.gz', 'rt')))[1:] for x in row})
path = [nodes[i] for i in struct.unpack('<69I', (p.parent / 'message.bin').read_bytes())]
targets = sorted(set(path[:-1]))
blocks = json.loads((p / 'batches.json').read_text())
schema = pa.ipc.open_file(str(p / 'weights-partial.feather')).schema
src = p / 'weights-v0.9.feather'
size = src.stat().st_size
out = collections.defaultdict(list)
with src.open('rb') as f:
    for j, (off, meta, n) in enumerate(blocks):
        if off + meta + n > size:
            break
        f.seek(off)
        batch = pa.ipc.read_record_batch(pa.ipc.read_message(f), schema)
        u, v, w = [col.to_numpy() for col in batch.columns]
        mask = np.isin(u, targets)
        for a, b, value in zip(u[mask], v[mask], w[mask]):
            out[int(a)].append((int(b), int(value)))
print('Read batches', j+1, 'of', len(blocks), flush=True)
(p / 'full-out-weights.json').write_text(json.dumps(out))
for name, key in [('file', None), ('id', lambda x:x[0]), ('weight_id', lambda x:(x[1],x[0])), ('negweight_id',lambda x:(-x[1],x[0]))]:
    a = {n: [b for b,w in (sorted(rows,key=key) if key else rows)] for n,rows in out.items()}
    vals = [a[x].index(y) if y in a[x] else -1 for x,y in zip(path,path[1:])]
    print(name, vals, flush=True)
    print(bytes(v%256 for v in vals), flush=True)
print('full degrees', [len(out[n]) for n in path[:10]], flush=True)
