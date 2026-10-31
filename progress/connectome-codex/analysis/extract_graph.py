import csv,gzip,struct,collections,sys
from pathlib import Path
import numpy as np
import pyarrow as pa
p=Path(__file__).resolve().parent
edges=np.array([tuple(map(int,r)) for r in list(csv.reader(gzip.open(p.parent/'adjacency.csv.gz','rt')))[1:]],dtype=np.int64)
nodes=np.unique(edges)
nmax=int(nodes[-1])+1
idx=np.full(nmax,-1,dtype=np.int32);idx[nodes]=np.arange(len(nodes))
version = sys.argv[1] if len(sys.argv)>1 else 'v0.9'
reader=pa.ipc.open_file(str(p/('weights-v1.0-traced.feather' if version=='v1.0' else 'weights-v0.9.feather')))
found=[];incoming=np.zeros(len(nodes),np.int64);outgoing=incoming.copy();fullin=incoming.copy();fullout=incoming.copy()
for j in range(reader.num_record_batches):
    b=reader.get_batch(j);u,v,w=[c.to_numpy() for c in b.columns[:3]]
    ui=np.full(len(u),-1,dtype=np.int32);vi=ui.copy()
    mask=u<nmax;ui[mask]=idx[u[mask]]
    mask=v<nmax;vi[mask]=idx[v[mask]]
    mu=ui>=0;mv=vi>=0;mask=mu&mv
    np.add.at(fullout,ui[mu],w[mu]);np.add.at(fullin,vi[mv],w[mv])
    np.add.at(outgoing,ui[mask],w[mask]);np.add.at(incoming,vi[mask],w[mask])
    if mask.any():found.append(np.column_stack([ui[mask],vi[mask],w[mask]]))
es=np.concatenate(found)
np.savez(p/('graph-v1.0.npz' if version=='v1.0' else 'graph.npz'),nodes=nodes,edges=es,incoming=incoming,outgoing=outgoing,fullin=fullin,fullout=fullout)
expected=set(map(tuple,idx[edges]));actual=set(map(tuple,es[:,:2]))
print('nodes',len(nodes),'source edges',len(es),'challenge edges',len(edges),'missing',len(expected-actual),'extra',len(actual-expected),flush=True)
path=struct.unpack('<69I',(p.parent/'message.bin').read_bytes())
for label,vals in [('in',incoming),('out',outgoing),('total',incoming+outgoing),('fullin',fullin),('fullout',fullout),('fulltotal',fullin+fullout)]:
    for reverse in [False,True]:
        order=sorted(range(len(nodes)),key=lambda n:(-int(vals[n]) if reverse else int(vals[n]),int(nodes[n])))
        rank={n:i for i,n in enumerate(order)}
        rs=[rank[n] for n in path]
        print(label,reverse,rs[:15],bytes(n%256 for n in rs),flush=True)
    print(label,'values',bytes(int(vals[n])%256 for n in path),flush=True)
