import csv,gzip,json,struct,collections,heapq,math,itertools,string,sys
from pathlib import Path
import numpy as np
import pyarrow.feather as pf
p=Path(__file__).resolve().parent
adj=collections.defaultdict(list)
for a,b in list(csv.reader(gzip.open(p.parent/'adjacency.csv.gz','rt')))[1:]:adj[int(a)].append(int(b))
nodes=sorted(set(adj)|{n for vs in adj.values() for n in vs});ix={n:i for i,n in enumerate(nodes)}
path=[nodes[i] for i in struct.unpack('<69I',(p.parent/'message.bin').read_bytes())]
new=len(sys.argv)>1 and sys.argv[1]=='v1.0'
w={int(a):dict(vs) for a,vs in json.loads((p/('mb-out-weights-v1.0.json' if new else 'full-out-weights.json')).read_text()).items()}
g=np.load(p/('graph-v1.0.npz' if new else 'graph.npz'))
ann=pf.read_table(p/'annotations-v0.9.feather').to_pandas().set_index('bodyId')
fields={col:ann[col].astype(str).to_dict() for col in ['type','instance','class','group','supertype','somaSide']}
stats={col:{n:int(g[col][i]) for i,n in enumerate(nodes)} for col in ['incoming','outgoing','fullin','fullout']}
inc=collections.Counter(b for vs in adj.values() for b in vs)
seen=set();hits=[]
def inspect(bits,label):
 if bits in seen:return
 seen.add(bits)
 for bs in [bits,bits[::-1]]:
  for width in [8,7]:
   for off in range(width):
    for revbyte in [False,True]:
     raw=bytes(int(bs[i:i+width][::-1] if revbyte else bs[i:i+width],2) for i in range(off,len(bs)-width+1,width))
     for raw2 in [raw,raw[::-1]]:
      for xor in [0,255 if width==8 else 127]:
       val=bytes(c^xor for c in raw2)
       if b'ctfcup' in val or b'flag{' in val or b'ctf{' in val:
        print('FOUND',label,width,off,revbyte,xor,val,flush=True);hits.append((str(label),val.decode('latin1')))
def codes_for(a,order,mode,algorithm):
 def key(b):
  if order=='file':return adj[a].index(b)
  if order=='id':return b
  if order=='str':return str(b)
  if order in fields:return (str(fields[order][b]),b)
  if order in stats:return (stats[order][b],b)
  if order=='weight':return(w[a][b],b)
  if order=='negweight':return(-w[a][b],b)
 ns=sorted(adj[a],key=key)
 def weight(b):
  x=w[a][b]
  return {'one':1,'w':x,'invw':1/x,'logw':math.log2(x+1),'in':inc[b],'out':len(adj[b]),'input_norm':x/stats['incoming'][b], 'input_norm2':x/stats['fullin'][b], 'output_dest':x/stats['outgoing'][b], 'sum_in':stats['incoming'][b], 'sum_out':stats['outgoing'][b]}[mode]
 ws=[weight(b) for b in ns]
 codes={}
 if algorithm.startswith('huff'):
  h=[(val,i,b) for i,(b,val) in enumerate(zip(ns,ws))];heapq.heapify(h);count=len(ns)
  while len(h)>1:
   x,y=heapq.heappop(h),heapq.heappop(h);tie=min(x[1],y[1]) if algorithm=='huff_min' else count
   heapq.heappush(h,(x[0]+y[0],tie,(x[2],y[2])));count+=1
  def walk(t,bits):
   if isinstance(t,int):codes[t]=bits
   else:walk(t[0],bits+'0');walk(t[1],bits+'1')
  walk(h[0][2],'')
 elif algorithm=='fano':
  def walk(ns,ws,bits):
   if len(ns)==1:codes[ns[0]]=bits;return
   total=sum(ws);cur=0;opts=[]
   for i in range(1,len(ns)):
    cur+=ws[i-1];opts.append((abs(total-2*cur),i))
   _,i=min(opts);walk(ns[:i],ws[:i],bits+'0');walk(ns[i:],ws[i:],bits+'1')
  walk(ns,ws,'')
 else:
  total=sum(ws);cum=0
  for b,v in zip(ns,ws):
   n=math.ceil(math.log2(total/v))+(algorithm=='fano_elias')
   q=(cum+(v/2 if algorithm=='fano_elias' else 0))/total
   codes[b]=f'{int(q*2**n):0{n}b}';cum+=v
 return codes
for mode in ['one','w','invw','logw','in','out','input_norm','input_norm2','output_dest','sum_in','sum_out']:
 print('mode',mode,flush=True)
 for order in ['file','id','str','weight','negweight',*fields,*stats]:
  for algorithm in ['huff','huff_min','fano','shannon','fano_elias']:
   codes={a:codes_for(a,order,mode,algorithm) for a in set(path[:-1])}
   seq=[codes[a][b] for a,b in zip(path,path[1:])]
   for rev in [False,True]:inspect(''.join(c[::-1] if rev else c for c in seq),(mode,order,algorithm,rev))
(p/'prefix-hits.json').write_text(json.dumps(hits))
print('done',len(seen),'unique bitstreams',flush=True)
