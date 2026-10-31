import numpy as np, csv, gzip, struct, collections
from pathlib import Path
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
p=Path(__file__).resolve().parent
g=dict(np.load(p/'graph-v1.0.npz')); nodes=g['nodes']; ix={v:i for i,v in enumerate(nodes)}
path=struct.unpack('<69I',(p.parent/'message.bin').read_bytes())
edges=g['edges']; w={(int(a),int(b)):int(c) for a,b,c in edges if a!=b}
adj=collections.defaultdict(list)
for a,b in list(csv.reader(gzip.open(p.parent/'adjacency.csv.gz','rt')))[1:]:adj[ix[int(a)]].append(ix[int(b)])
starts=list(dict.fromkeys(path)); start_ix={v:i for i,v in enumerate(starts)}
def report(valid,mode):
 dp=[999]*len(path); ways=[[] for _ in path];dp[0]=0
 for j in range(1,len(path)):
  for i in range(j):
   if valid[i,j] and dp[i]+1<dp[j]:dp[j]=dp[i]+1;ways[j]=ways[i]+[j]
 print(mode,'min',dp[-1],'cuts',ways[-1], 'nodes',[path[i] for i in ways[-1]],flush=True)
 print('early routes',[(i,[j for j in range(i+1,min(len(path),i+10)) if valid[i,j]]) for i in range(16)],flush=True)
 np.save(p/('routes-'+mode+'.npy'),valid)
for mode,ws in [('unit',np.ones(len(edges))),('weight',edges[:,2].astype(float)),('inverse',1/edges[:,2]),('invlog',1/np.log1p(edges[:,2]))]:
 A=csr_matrix((ws,(edges[:,0],edges[:,1])),shape=(4096,4096)); dist=dijkstra(A,indices=starts)
 costs=[A[a,b] for a,b in zip(path,path[1:])]; valid=np.zeros((len(path),len(path)),bool)
 for i in range(len(path)):
  cost=0
  for j in range(i+1,len(path)):
   cost+=costs[j-1];valid[i,j]=np.isclose(dist[start_ix[path[i]],path[j]],cost,atol=1e-10,rtol=1e-10)
 report(valid,mode)
for mode in ['file','id','weight','reverseid','reversefile']:
 ad={a:vs if mode=='file' else vs[::-1] if mode=='reversefile' else sorted(vs,reverse=mode=='reverseid',key=lambda b:(-w[a,b],b) if mode=='weight' else b) for a,vs in adj.items()}
 valid=np.zeros((len(path),len(path)),bool)
 for a in starts:
  pred={a:-1};q=collections.deque([a])
  while q:
   u=q.popleft()
   for v in ad[u]:
    if v not in pred:pred[v]=u;q.append(v)
  for i,n in enumerate(path):
   if n!=a:continue
   for j in range(i+1,len(path)):
    route=[path[j]]
    while route[-1]!=a:route.append(pred[route[-1]])
    valid[i,j]=route[::-1]==list(path[i:j+1])
 report(valid,mode)
