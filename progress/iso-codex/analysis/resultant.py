import sympy as S, requests,json
from pathlib import Path
A,B,s,r=S.symbols('A B s r')
f=4*A**3+27*B**2+31104*s*A*B
a=-4*A-15*r*r;b=22*B+14*A*r
g=S.resultant(S.Poly(f.subs({A:a,B:b},simultaneous=True),r).rem(S.Poly(r**3+A*r+B,r)).as_expr(),r**3+A*r+B,r)
g=S.factor(g);print('g=',g,flush=True)
aa=6079433314242371108270239373533376748;bb=-1779744368654530162000920720207404089
expr=g.subs({A:-4*aa-15*r*r,B:22*bb+14*aa*r,s:2**66},simultaneous=True)
n=int(S.resultant(expr,r**3+aa*r+bb,r));n=abs(n)//abs(int(f.subs({A:16*aa,B:64*bb,s:2**66})))**3
Path('analysis/n2.txt').write_text(str(n))
print('digits',len(str(n)),flush=True)
facs=S.factorint(n,limit=10000);print(facs,flush=True)
for fac in facs:
 if fac.bit_length()>120:
  resp=requests.get('https://factordb.com/api',params={'query':str(fac)},timeout=30);print(resp.text,flush=True)
