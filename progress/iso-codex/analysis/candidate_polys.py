from flint import fmpz_mpoly_ctx
import json
from pathlib import Path
ctx=fmpz_mpoly_ctx.get(('r','A','B','s'),'lex');r,A,B,s=ctx.gens();f=r**3+A*r+B;ap=-4*A-15*r*r;bp=22*B+14*A*r
aa=6079433314242371108270239373533376748;bb=-1779744368654530162000920720207404089
for name,v in [('A',A),('B',B)]:
 h=[v-s]
 for d in range(1,5):
  q=h[-1].compose(r,ap,bp,s)%f
  c0=q.subs({'r':0});c1=q.derivative('r').subs({'r':0});c2=q.derivative('r').derivative('r').subs({'r':0})//2
  norm=c0**3-2*A*c0*c0*c2+A*A*c0*c2*c2+A*c0*c1*c1+3*B*c0*c1*c2+B*B*c2**3-B*c1**3-A*B*c1*c2*c2
  if d>=2:
   den=h[-2].compose(r,16*A,64*B,s).primitive()[1]**(3 if d==2 else 2)
   assert (norm%den).is_zero();norm=norm//den
  hd=norm.primitive()[1];h.append(hd)
  hd=hd.subs({'A':aa,'B':bb})
  co=[0]*(int(hd.degrees()[3])+1)
  for ex,val in hd.to_dict().items():co[int(ex[3])]=str(val)
  Path(f'analysis/candidate_{name}{d}.json').write_text(json.dumps(co))
 print(name,'done')
