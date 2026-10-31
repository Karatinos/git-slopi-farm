import csv,gzip,json,struct,collections,itertools,hashlib,zlib,string
from pathlib import Path
import pyarrow.feather as pf
p=Path(__file__).resolve().parent
nodes=sorted({int(x) for row in list(csv.reader(gzip.open(p.parent/'adjacency.csv.gz','rt')))[1:] for x in row})
ind=struct.unpack('<69I',(p.parent/'message.bin').read_bytes());path=[nodes[i] for i in ind]
weights={int(a):dict(vs) for a,vs in json.loads((p/'mb-out-weights-v1.0.json').read_text()).items()}
ann=pf.read_table(p/'annotations-v1.0.feather').to_pandas().set_index('bodyId')
pref=b'ctfcup{';hexpref=[int(c,16) for c in pref.hex()]
alphabet=[('byte',None,pref),('7bit',None,pref),('nibble',None,hexpref)]
for chars in [string.ascii_lowercase+string.digits+'{}_',string.ascii_lowercase+string.digits+'_{}',string.digits+string.ascii_lowercase+'{}_',string.printable,''.join(chr(x) for x in range(32,127))]:
 alphabet.append((chars,chars,[chars.index(chr(c)) for c in pref]))
values=[]
for i,(a,b) in enumerate(zip(path,path[1:])):
 values.append({'a':str(a),'b':str(b),'i':str(ind[i]),'j':str(ind[i+1]),'w':str(weights[a][b]),'ta':str(ann.loc[a,'type']),'tb':str(ann.loc[b,'type']),'na':str(ann.loc[a,'instance']),'nb':str(ann.loc[b,'instance'])})
best=[];count=0
for parts in [('a','b'),('a','b','w'),('w','a','b'),('b','a'),('b','a','w'),('i','j'),('i','j','w'),('ta','tb'),('ta','tb','w'),('na','nb'),('na','nb','w'),('a','b','ta','tb')]:
 for sep in ['',',',':','|',' ',';','-','_','/','->',', ']:
  for wrapping in ['', '()', '[]']:
   ss=[(wrapping[:1]+sep.join(v[k] for k in parts)+wrapping[1:]).encode() for v in values]
   for algo in ['md5','sha1','sha256','sha512','blake2b','blake2s','sha3_256','crc32']:
    ds=[(zlib.crc32(s).to_bytes(4,'big') if algo=='crc32' else hashlib.new(algo,s).digest()) for s in ss]
    for off in list(range(len(ds[0])))+['big','little']:
     nums=[int.from_bytes(d,off) if isinstance(off,str) else d[off] for d in ds]
     for label,chars,target in alphabet:
      mod=16 if label=='nibble' else 128 if label=='7bit' else 256 if chars is None else len(chars)
      vals=[n%mod for n in nums]
      score=sum(a==b for a,b in zip(vals,target))
      if score>=len(target)-1:
       print('CANDIDATE',score,parts,sep,wrapping,algo,off,label,vals,flush=True)
       best.append([score,str((parts,sep,wrapping,algo,off,label)),vals])
   count+=1
print('done',count,flush=True)
(p/'edge-hash-hits.json').write_text(json.dumps(best))
