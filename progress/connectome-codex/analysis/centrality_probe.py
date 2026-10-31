import numpy as np, struct, collections
from pathlib import Path
from scipy.sparse import csr_matrix,diags
from scipy.sparse.linalg import eigs
p=Path(__file__).resolve().parent;g=dict(np.load(p/'graph-v1.0.npz'));es=g['edges'];m=struct.unpack('<69I',(p.parent/'message.bin').read_bytes());path=list(m[1:]);out=[]
def check(name,v):
 if v.sum()<0:v=-v
 order=sorted(range(4096),key=lambda i:(v[i],i));r=np.zeros(4096,dtype=int);r[order]=np.arange(4096)
 print(name,'first ranks',[int(r[n]) for n in m[:16]],flush=True)
 out.append((name,np.array(v)))
 for vals,kind in [(r,'rank'),(4095-r,'rankrev')]:
  for mod in [128,256]:
   for shift in range(mod):
    s=bytes(int((vals[n]+shift)%mod) for n in path);idx=0;loc=[]
    for i,c in enumerate(s):
     if c==b'ctfcup{'[idx]:idx+=1;loc.append(i+1)
     if idx==7:break
    if idx>=5:print('PREFIX',name,kind,mod,shift,idx,loc,s,flush=True)
for weighted in [False,True]:
 A=csr_matrix((es[:,2] if weighted else np.ones(len(es)),(es[:,0],es[:,1])),shape=(4096,4096),dtype=float)
 for reverse in [False,True]:
  B=A.T.tocsr() if reverse else A
  d=np.asarray(B.sum(axis=1)).ravel();P=diags(1/d)@B
  ev,evec=eigs(B,k=1,which='LM');check(f'eigen {weighted=} {reverse=}',evec[:,0].real)
  for damping in [.5,.85,.95,1.0]:
   x=np.full(4096,1/4096)
   for it in range(5000):
    y=damping*(P.T@x)+(1-damping)/4096
    if np.abs(x-y).sum()<1e-13:break
    x=y
   check(f'pagerank {weighted=} {reverse=} {damping=}',x)
 for method in ['hub','authority']:
  B=A@A.T if method=='hub' else A.T@A
  ev,evec=eigs(B,k=1,which='LM');check(f'hits {weighted=} {method}',evec[:,0].real)
np.savez(p/'centralities.npz',**{k:v for k,v in out})
