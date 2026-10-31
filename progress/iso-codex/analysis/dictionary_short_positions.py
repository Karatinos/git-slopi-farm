from pathlib import Path
from flint import fmpz,fmpz_poly
import json,itertools,time,sys
sys.set_int_max_str_digits(0)
D=[int(x) for x in sys.argv[1].split(',')]
mode=sys.argv[2] if len(sys.argv)>2 else 'common'
ns={d:fmpz(int(Path('analysis/n2_current.txt' if d==2 else f'analysis/cofactor{d}.txt').read_text())) for d in D}
polys={d:fmpz_poly([int(x) for x in json.loads(Path(f'analysis/candidate_A{d}.json').read_text())]) for d in D}
acc={d:fmpz(1) for d in D};batch=[];vs={d:[] for d in D};count=0;start=time.time()
phrases=json.loads(Path('analysis/short_phrase_set.json').read_text())
leet={'a':['a','4'],'e':['e','3'],'i':['i','1'],'l':['l','1'],'o':['o','0'],'s':['s','5'],'t':['t','7'],'g':['g','9'],'b':['b','8']}
def flush():
 global acc,batch,vs
 for d in D:
  g=acc[d].gcd(ns[d])
  if g>1:
   for flag,v in zip(batch,vs[d]):
    h=v.gcd(ns[d])
    if h.bit_length()>=120:
     print('HIT',d,flag,str(h),flush=True)
     with open('analysis/dictionary_hits.txt','a') as f:f.write(f'{d} {flag!r} {h}\n')
 acc={d:fmpz(1) for d in D};batch=[];vs={d:[] for d in D}
def check(body):
 global count
 flag=b'ctfcup{'+body.encode()+b'}';assert len(flag)==27
 j=fmpz(int.from_bytes(flag,'little'));c=-3*j*(j-1728)
 for d in D:
  v=polys[d](c*(fmpz(2)**(128+2*d)))%ns[d]
  vs[d].append(v);acc[d]=acc[d]*v%ns[d]
 batch.append(flag);count+=1
 if len(batch)==256:flush()
common=[]
for keyset in ['','aeio','aeios','aeiost','aeiostl','aeiostlg','aeiostlgb','aeiol','aeiosl','aeioslg','aeiostg','eo','eio','aelo']:
 common.append(str.maketrans({k:leet[k][1] for k in keyset}))
print('START',D,mode,'phrases',len(phrases),flush=True)
for pi,phrase in enumerate(phrases):
 if mode=='common':variants={phrase.translate(table) for table in common}
 elif mode=='all':
  keys=sorted(set(phrase)&leet.keys())
  variants=(phrase.translate(str.maketrans(dict(zip(keys,combo)))) for combo in itertools.product(*(leet[k] for k in keys)))
 elif mode=='position':variants=(''.join(c) for c in itertools.product(*(leet.get(c,[c]) for c in phrase)))
 for body in variants:check(body)
 if pi%100==0:print('progress',pi,'candidates',count,'seconds',round(time.time()-start,1),flush=True)
flush();print('DONE',D,mode,count,round(time.time()-start,1),flush=True)
