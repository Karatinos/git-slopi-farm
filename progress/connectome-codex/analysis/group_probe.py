import csv,gzip,json,struct,collections,heapq,math,itertools,string
from pathlib import Path
import pyarrow.feather as pf
p=Path(__file__).resolve().parent
adj=collections.defaultdict(list)
for a,b in list(csv.reader(gzip.open(p.parent/'adjacency.csv.gz','rt')))[1:]:adj[int(a)].append(int(b))
nodes=sorted(set(adj)|{n for vs in adj.values() for n in vs});ix={n:i for i,n in enumerate(nodes)}
path=[nodes[i] for i in struct.unpack('<69I',(p.parent/'message.bin').read_bytes())]
w={int(a):dict(vs) for a,vs in json.loads((p/'mb-out-weights-v1.0.json').read_text()).items()}
ann=pf.read_table(p/'annotations-v1.0.feather').to_pandas().set_index('bodyId')
fields={col:ann[col].astype(str).to_dict() for col in ['type','instance','class','group','supertype','somaSide','itoleeHl','birthtime']}
nt=pf.read_table(p/'neurotransmitters-v1.0.feather').to_pandas().set_index('body')
for col in ['predicted_nt','ground_truth','celltype_predicted_nt','consensus_nt']:
 fields[col]=nt[col].astype(str).to_dict()
def label(a,b,col):
 if col=='weight':return w[a][b]
 if col=='logweight':return w[a][b].bit_length()
 if col.startswith('mod'):return w[a][b]%int(col[3:])
 return str(fields[col][b])
def inspect(bits,tag):
 for bs in [bits,bits[::-1]]:
  for width in [8,7]:
   for off in range(width):
    for rev in [False,True]:
     raw=bytes(int(bs[i:i+width][::-1] if rev else bs[i:i+width],2) for i in range(off,len(bs)-width+1,width))
     for val in [raw,raw[::-1],bytes(c^((1<<width)-1) for c in raw),bytes(c^((1<<width)-1) for c in raw[::-1])]:
      if b'ctf' in val:print('HIT',tag,width,off,rev,val,flush=True)
for col in [*fields,'weight','logweight','mod2','mod4','mod8','mod16','mod32','mod64','mod128','mod256']:
 print(col,flush=True)
 groups={}
 for a in set(path[:-1]):
  gs=collections.defaultdict(list)
  for b in adj[a]:gs[label(a,b,col)].append(b)
  groups[a]=gs
 for mode in ['uniform','count','weight','invcount']:
  for order in ['file','label','count','weight']:
   for rev in [False,True]:
    all_codes={};digits=[]
    for a,gs in groups.items():
     ks=list(gs)
     if order=='label':ks.sort()
     if order=='count':ks.sort(key=lambda k:(len(gs[k]),k))
     if order=='weight':ks.sort(key=lambda k:(sum(w[a][b] for b in gs[k]),k))
     if rev:ks.reverse()
     weights=[{'uniform':1,'count':len(gs[k]),'weight':sum(w[a][b] for b in gs[k]),'invcount':1/len(gs[k])}[mode] for k in ks]
     h=[(v,i,k) for i,(v,k) in enumerate(zip(weights,ks))];heapq.heapify(h);c=len(h)
     while len(h)>1:
      x,y=heapq.heappop(h),heapq.heappop(h);heapq.heappush(h,(x[0]+y[0],c,(x[2],y[2])));c+=1
     codes={}
     def walk(t,bits):
      if isinstance(t,tuple):walk(t[0],bits+'0');walk(t[1],bits+'1')
      else:codes[t]=bits
     walk(h[0][2],'');all_codes[a]=codes
    seq=[all_codes[a][label(a,b,col)] for a,b in zip(path,path[1:])]
    for reverse in [False,True]:inspect(''.join(s[::-1] if reverse else s for s in seq),(col,mode,order,rev,reverse))
print('done')
