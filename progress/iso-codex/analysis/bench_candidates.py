from pathlib import Path
from flint import fmpz,fmpz_poly
import json,time
for d in [2,4]:
 N=fmpz(int(Path(f'analysis/cofactor{d}.txt').read_text()))
 coeff=[fmpz(int(x)) for x in json.loads(Path(f'analysis/candidate_A{d}.json').read_text())]
 poly=fmpz_poly(coeff);cc=[c%N for c in coeff]
 J=int.from_bytes(b'ctfcup{0000000000000000000}','little')
 vals=[fmpz(-3*(J+i*256**7)*(J+i*256**7-1728)*2**(128+2*d)) for i in range(1000)]
 t=time.time()
 results=[poly(c)%N for c in vals]
 print(d,'raw-poly1000',time.time()-t,flush=True)
 t=time.time();results2=[]
 for c in vals:
  v=fmpz(0)
  for co in reversed(cc):v=(v*c+co)%N
  results2.append(v)
 print(d,'modular1000',time.time()-t,'equal',results==results2,flush=True)
 t=time.time();g=[v.gcd(N) for v in results]
 print(d,'gcd1000',time.time()-t,flush=True)
