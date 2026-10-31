from flint import fmpz_mpoly_ctx
from pathlib import Path
import json,time,sys,math
sys.set_int_max_str_digits(0)
ctx=fmpz_mpoly_ctx.get(('r','A','B','s'),'lex')
r,A,B,s=ctx.gens()
f=r**3+A*r+B
ap=-4*A-15*r*r
bp=22*B+14*A*r
h=[4*A**3+27*B*B+31104*s*A*B]
aa=6079433314242371108270239373533376748
bb=-1779744368654530162000920720207404089
for d in range(1,7):
 t=time.time();print('composing',d,'terms',len(h[-1]),flush=True)
 q=h[-1].compose(r,ap,bp,s)%f
 c0=q.subs({'r':0})
 c1=q.derivative('r').subs({'r':0})
 c2=q.derivative('r').derivative('r').subs({'r':0})//2
 norm=c0**3-2*A*c0*c0*c2+A*A*c0*c2*c2+A*c0*c1*c1+3*B*c0*c1*c2+B*B*c2**3-B*c1**3-A*B*c1*c2*c2
 print('norm',d,'terms',len(norm),'time',time.time()-t,flush=True)
 if d>=2:
  den=h[-2].compose(r,16*A,64*B,s).primitive()[1]**(3 if d==2 else 2)
  assert (norm%den).is_zero()
  norm=norm//den
 hd=norm.primitive()[1]
 if hd.leading_coefficient()<0:hd=-hd
 h.append(hd)
 Path(f'analysis/H{d}.json').write_text(json.dumps([([int(x) for x in k],str(v)) for k,v in hd.to_dict().items()]))
 n=abs(int(hd(0,aa,bb,2**(64+d))))
 Path(f'analysis/primitive_n{d}.txt').write_text(str(n))
 print('DONE',d,'terms',len(hd),'degrees',hd.degrees(),'digits',len(str(n)),'seconds',time.time()-t,flush=True)
