import numpy as np,struct,pyarrow as pa,pyarrow.feather as pf
from pathlib import Path
p=Path(__file__).resolve().parent;g=dict(np.load(p/'graph-v1.0.npz'));nodes=g['nodes'];m=struct.unpack('<69I',(p.parent/'message.bin').read_bytes());features={}
def add(name,inc,out):
 for label,vals in [('in',inc),('out',out),('sum',inc+out),('diff',inc-out),('product',inc*out),('xor',inc^out),('min',np.minimum(inc,out)),('max',np.maximum(inc,out))]:features[name+'/'+label]=vals
def inspect(name,v):
 for mod in [128,256]:
  for values,kind in [(v,'value'),(np.argsort(np.argsort(v,kind='stable'),kind='stable'),'rank')]:
   for shift_mode in ['none','add','xor']:
    target=ord('c');first=int(values[m[1]])%mod
    raw=bytes(((int(values[n])+target-first) if shift_mode=='add' else (int(values[n])^target^first) if shift_mode=='xor' else int(values[n]))%mod for n in m[1:])
    idx=0;pos=[]
    for i,c in enumerate(raw[:20]):
     if c==b'ctfcup{'[idx]:idx+=1;pos.append(i+1)
     if idx==7:break
    if idx>=5:print('MATCH',name,kind,mod,shift_mode,idx,pos,raw,flush=True)
u,v,w=g['edges'].T
for q in list(range(1,32))+[32,64,99,100,128,256]:
 for mode,mask in [('eq',w==q),('ge',w>=q),('bit',(w&q)!=0)]:
  inc=np.bincount(v[mask],minlength=4096);out=np.bincount(u[mask],minlength=4096);add(f'induced/{mode}{q}',inc,out)
for power in [1,2,3]:
 inc=np.bincount(v,weights=w**power,minlength=4096).astype(np.int64);out=np.bincount(u,weights=w**power,minlength=4096).astype(np.int64);add(f'induced/power{power}',inc,out)
for bit in range(8):
 mask=(w>>bit)&1;inc=np.bincount(v,weights=mask,minlength=4096).astype(np.int64);out=np.bincount(u,weights=mask,minlength=4096).astype(np.int64);add(f'induced/bit{bit}',inc,out)
for k,x in features.items():inspect(k,x)
print('induced done',len(features),flush=True)
# Aggregate full traced graph degree/strength, separated by weight thresholds.
nmax=int(nodes[-1])+1;ix=np.full(nmax,-1,np.int64);ix[nodes]=np.arange(4096)
qs=[1,2,3,4,5,8,10,16,32,64,128];counts=np.zeros((len(qs),2,4096),np.int64)
reader=pa.ipc.open_file(str(p/'weights-v1.0-traced.feather'))
for j in range(reader.num_record_batches):
 b=reader.get_batch(j);us,vs,ws=[c.to_numpy() for c in b.columns[:3]]
 for direction,ids in [(0,vs),(1,us)]:
  mask=ids<nmax;ids=ids[mask];ww=ws[mask];local=ix[ids];mask=local>=0;local=local[mask];ww=ww[mask]
  for qi,q in enumerate(qs):np.add.at(counts[qi,direction],local[ww>=q],1)
for qi,q in enumerate(qs):add(f'full/ge{q}',counts[qi,0],counts[qi,1])
for k,x in features.items():
 if k.startswith('full'):inspect(k,x)
np.savez(p/'statistics.npz',**features)
print('all done',len(features),flush=True)
