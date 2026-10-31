import collections,csv,gzip,json,struct,math,sys
from pathlib import Path
from fractions import Fraction
import pyarrow.feather as pf
p=Path(__file__).resolve().parent
edges=[tuple(map(int,r)) for r in list(csv.reader(gzip.open(p.parent/'adjacency.csv.gz','rt')))[1:]]
adj=collections.defaultdict(list);ind=collections.Counter()
for a,b in edges:adj[a].append(b);ind[b]+=1
nodes=sorted(set(x for e in edges for x in e));path=[nodes[i] for i in struct.unpack('<69I',(p.parent/'message.bin').read_bytes())]
new=len(sys.argv)>1 and sys.argv[1]=='v1.0'
full={int(a):{int(b):w for b,w in r} for a,r in json.loads((p/('mb-out-weights-v1.0.json' if new else 'full-out-weights.json')).read_text()).items()}
ann=pf.read_table(p/'annotations-v0.9.feather').to_pandas().set_index('bodyId')
types=ann['type'].astype(str).to_dict();instances=ann['instance'].astype(str).to_dict()
target=b'ctfcup{';best=[]
def inspect(label,bits):
 for off in range(8):
  for reverse in [False,True]:
   chunks=[bits[i:i+8] for i in range(off,len(bits)-7,8)]
   raw=bytes(int(c[::-1] if reverse else c,2) for c in chunks)
   if b'ctfcup' in raw or b'ctfcup' in raw[::-1] or sum(32<=c<127 for c in raw)>len(raw)*.9:print('FOUND',label,off,reverse,raw,flush=True)
   score=sum((x^y).bit_count() for x,y in zip(raw,target))
   best.append((score,label,off,reverse,raw))
for mode in ['uniform','weight','logweight','sqrtweight','indegree','outdegree']:
 for ordering in ['file','original','id','str','weight','negweight','type','instance','indegree','outdegree']:
  for reverse in [False,True]:
   triples=[]
   for a,b in zip(path,path[1:]):
    def key(v):
     w=full[a][v]
     return {'id':v,'str':str(v),'weight':(w,v),'negweight':(-w,v),'type':(types[v],v),'instance':(instances[v],v),'indegree':(ind[v],v),'outdegree':(len(adj[v]),v)}[ordering]
    ns=adj[a][:] if ordering=='file' else [v for v in full[a] if v in adj[a]] if ordering=='original' else sorted(adj[a],key=key)
    if reverse:ns.reverse()
    ws=[{'uniform':1,'weight':full[a][v],'logweight':full[a][v].bit_length(),'sqrtweight':math.isqrt(full[a][v]),'indegree':ind[v],'outdegree':len(adj[v])}[mode] for v in ns]
    i=ns.index(b);triples.append((sum(ws[:i]),ws[i],sum(ws)))
   for rev in [False,True]:
    ts=triples[::-1] if rev else triples
    n=0
    for start,w,total in ts:n=n//w*total+start+n%w
    bits=f'{n:b}';bits='0'*((-len(bits))%8)+bits
    inspect(f'ans {mode} {ordering} {reverse} {rev}',bits)
   lo=Fraction(0);span=Fraction(1)
   for start,w,total in triples:
    lo+=span*Fraction(start,total);span*=Fraction(w,total)
   val=lo+span/2;nbits=max(8,int(-math.log2(float(span))));n=val.numerator*(1<<nbits)//val.denominator
   inspect(f'arithmetic {mode} {ordering} {reverse}',f'{n:0{nbits}b}')
print(*sorted(best)[:10],sep='\n')
