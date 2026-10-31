import csv,gzip,json,struct,collections,heapq,math,itertools,hashlib,zlib,string
from pathlib import Path
import numpy as np
import pyarrow.feather as pf
p=Path(__file__).resolve().parent
adj=collections.defaultdict(list)
for a,b in list(csv.reader(gzip.open(p.parent/'adjacency.csv.gz','rt')))[1:]:adj[int(a)].append(int(b))
nodes=sorted(set(adj)|{n for vs in adj.values() for n in vs});ix={n:i for i,n in enumerate(nodes)}
path=[nodes[i] for i in struct.unpack('<69I',(p.parent/'message.bin').read_bytes())]
w={int(a):dict(vs) for a,vs in json.loads((p/'mb-out-weights-v1.0.json').read_text()).items()}
ann=pf.read_table(p/'annotations-v1.0.feather').to_pandas().set_index('bodyId').loc[nodes]
nt=pf.read_table(p/'neurotransmitters-v1.0.feather').to_pandas().set_index('body').loc[nodes]
fields={col:[str(v) for v in ann[col]] for col in ann.columns}
fields.update({col:[str(v) for v in nt[col]] for col in nt.columns})
fields['bodyId']=[str(n) for n in nodes]
fields['index']=[str(i) for i in range(len(nodes))]
seen=set();hits=[]
def inspect(raw,tag):
 for raw in [raw,raw[::-1]]:
  if b'ctfcup' in raw or (len(raw)>12 and sum(c in b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}' for c in raw)/len(raw)>.92):
   print('HIT',tag,raw,flush=True);hits.append((str(tag),raw.decode('latin1')))
def inspect_bits(bits,tag):
 for bs in [bits,bits[::-1]]:
  for width in [8,7]:
   for off in range(width):
    raw=bytes(int(bs[i:i+width],2) for i in range(off,len(bs)-width+1,width))
    inspect(raw,tag)
    inspect(bytes(c^((1<<width)-1) for c in raw),tag)
def check(keys,tag):
 for reverse in [False,True]:
  ns={a:sorted(vs,key=lambda v:(keys[ix[v]],v),reverse=reverse) for a,vs in adj.items() if a in set(path[:-1])}
  digits=[(ns[a].index(b),len(ns[a])) for a,b in zip(path,path[1:])]
  for alphabet in [None,string.ascii_lowercase+string.digits+'{}_',''.join(chr(c) for c in range(32,127)),string.printable]:
   pref=list(b'ctfcup{') if alphabet is None else [alphabet.index(c) for c in 'ctfcup{']
   if all(d==c%b for (d,b),c in zip(digits,pref)):
    print('MOD PREFIX MATCH',tag,reverse,alphabet,digits,flush=True)
  tup=tuple(digits)
  if tup in seen:continue
  seen.add(tup)
  for flow in [False,True]:
   n=0
   for d,b in digits[::-1] if flow else digits:n=n*b+d
   inspect(n.to_bytes((n.bit_length()+7)//8,'big'),('radix',tag,reverse,flow))
  for weight_mode in ['uniform','weight']:
   for ties in ['count','min']:
    codes={}
    for a,vs in ns.items():
     heap=[(w[a][b] if weight_mode=='weight' else 1,i,b) for i,b in enumerate(vs)];heapq.heapify(heap);n=len(vs)
     while len(heap)>1:
      x,y=heapq.heappop(heap),heapq.heappop(heap)
      heapq.heappush(heap,(x[0]+y[0],min(x[1],y[1]) if ties=='min' else n,(x[2],y[2])));n+=1
     cd={}
     def walk(t,bits):
      if isinstance(t,int):cd[t]=bits
      else:walk(t[0],bits+'0');walk(t[1],bits+'1')
     walk(heap[0][2],'');codes[a]=cd
    bits=''.join(codes[a][b] for a,b in zip(path,path[1:]))
    inspect_bits(bits,('huff',tag,reverse,weight_mode,ties))
for col,values in fields.items():
 print(col,flush=True)
 check(values,(col,'str'))
 try:check([float(v) if math.isfinite(float(v)) else -1 for v in values],(col,'numeric'))
 except ValueError:pass
 for algo in ['sha256','sha1','md5','blake2b','crc32']:
  hashes=[zlib.crc32(v.encode()).to_bytes(4,'big') if algo=='crc32' else hashlib.new(algo,v.encode()).digest() for v in values]
  check(hashes,(col,algo))
coords=[]
for v in ann.somaLocation:
 coords.append([0,0,0] if v is None else list(v))
for perm in itertools.permutations(range(3)):
 check([tuple(c[i] for i in perm) for c in coords],('coords',perm))
(p/'order-hits.json').write_text(json.dumps(hits))
print('done',len(seen),'orders',flush=True)
