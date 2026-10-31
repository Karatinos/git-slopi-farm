import json,struct,itertools
from pathlib import Path
M=2**32-1
rol=lambda x,n:((x<<n)|(x>>(32-n)))&M
def H(a,b):
 x=rol(a^b^0x9e3779b9,13);x=x*0x85ebca6b&M;x^=x>>15;x=x*0xc2b2ae35&M;return x^(x>>16)
def inv(x):
 x^=x>>16;x=x*pow(0xc2b2ae35,-1,1<<32)&M;x^=x>>15;x^=x>>30;x=x*pow(0x85ebca6b,-1,1<<32)&M;return rol(x,19)
b=Path('unpack_resolved.bin').read_bytes();rows=[];p=None
for line in Path('unpack_frame_samples.jsonl').read_text().splitlines():
 r=json.loads(line);i=r['regs']['R14'];rv,c,k=struct.unpack_from('<III',b,0x1671008+i*12);plain=r['value'];s=c^plain;key=[0xa29a6108,0x7580794a][i&1]
 if p:
  state=inv(s)^key^i^0x9e3779b9;a=inv(state)^p['s']^0x9e3779b9
  rows.append(dict(i=i,rv=rv,c=c,plain=plain,prev_s=p['s'],prev_c=p['c'],prev_p=p['plain'],prev_rv=p['rv'],key=key,arg=a))
 p=dict(s=s,c=c,plain=plain,rv=rv)
vs={k:tuple(r[k] for r in rows) for k in rows[0] if k!='arg'}
for c in [0,1,12,60922,0x783a0aca,0x2db95856,0xa29a6108,0x7580794a,0xacf2077,0xacf2078,0x9e3779b9,0x85ebca6b,0xc2b2ae35,0x27d4eb2d,0x7feb352d,0x846ca68b]:vs[hex(c)]=(c,)*len(rows)
arg=tuple(r['arg'] for r in rows)
def check(k,v):
 if v==arg:print('FOUND',k,flush=True)
 xor=[x^y for x,y in zip(v,arg)]
 if len(set(xor))==1:print('CONSTXOR',k,hex(xor[0]),flush=True)
 sub=[(x-y)&M for x,y in zip(v,arg)]
 if len(set(sub))==1:print('CONSTSUB',k,hex(sub[0]),flush=True)
for k,v in vs.items():check(k,v)
for (a,av),(b,bv) in itertools.combinations_with_replacement(list(vs.items()),2):
 for name,fun in [('xor',lambda x,y:x^y),('add',lambda x,y:(x+y)&M),('sub',lambda x,y:(x-y)&M),('mul',lambda x,y:x*y&M),('H',H)]:
  v=tuple(fun(x,y) for x,y in zip(av,bv));check(f'{name}({a},{b})',v)
