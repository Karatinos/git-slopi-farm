"""Check hypothesized character boundaries; this does not establish plaintext."""
import csv,gzip,struct,collections,json
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parent
g=dict(np.load(p/'graph-v1.0.npz'));ix={n:i for i,n in enumerate(g['nodes'])}
path=list(struct.unpack('<69I',(p.parent/'message.bin').read_bytes()))
es=[(ix[int(a)],ix[int(b)]) for a,b in list(csv.reader(gzip.open(p.parent/'adjacency.csv.gz','rt')))[1:]]
w={(int(a),int(b)):int(v) for a,b,v in g['edges']}
cuts=[0,1,4,5,7,10,13,15,18,19,21,24,27,29,32,34,35,39,42,44,47,51,54,56,58,61,64,66,68]
def route(adj,rev,source,target):
 if source==target:return [source]
 pred={source:None};succ={target:None};f=[source];r=[target];meet=None
 while f and r and meet is None:
  if len(f)<=len(r):
   old=f;f=[]
   for v in old:
    for u in adj[v]:
     if u not in pred:f.append(u);pred[u]=v
     if u in succ:meet=u;break
    if meet is not None:break
  else:
   old=r;r=[]
   for v in old:
    for u in rev[v]:
     if u not in succ:r.append(u);succ[u]=v
     if u in pred:meet=u;break
    if meet is not None:break
 if meet is None:return None
 left=[];n=meet
 while n is not None:left.append(n);n=pred[n]
 out=left[::-1];n=succ[meet]
 while n is not None:out.append(n);n=succ[n]
 return out
for mode in ['file','public','id','weight','reverseid','reversefile']:
 adj=collections.defaultdict(list);rev=collections.defaultdict(list)
 for a,b in es if mode!='public' else g['edges'][:,:2]:
  a=int(a);b=int(b)
  if a==b:continue
  adj[a].append(b);rev[b].append(a)
 for a in adj:
  if mode=='id':adj[a].sort();rev[a].sort()
  if mode=='reverseid':adj[a].sort(reverse=True);rev[a].sort(reverse=True)
  if mode=='reversefile':adj[a].reverse();rev[a].reverse()
  if mode=='weight':adj[a].sort(key=lambda b:(-w[a,b],b));rev[a].sort(key=lambda b:(-w[b,a],b))
 bad=[]
 for i,j in zip(cuts,cuts[1:]):
  found=route(adj,rev,path[i],path[j]);actual=path[i:j+1]
  if found!=actual:bad.append((i,j,actual,found))
 print(mode,'matches',28-len(bad),'/ 28', 'mismatches',bad,flush=True)
 valid=np.zeros((69,69),bool)
 for i in range(69):
  for j in range(i+1,min(69,i+8)):
   valid[i,j]=route(adj,rev,path[i],path[j])==path[i:j+1]
 np.save(p/('routes-bidir-'+mode+'.npy'),valid)
