from pathlib import Path
import requests,sympy as S,json,sys
sys.set_int_max_str_digits(0)
for d in [2,4]:
 n=int(Path(f'analysis/primitive_n{d}.txt').read_text());small={}
 for p in S.primerange(1,100000):
  while n%p==0:
   small[p]=small.get(p,0)+1;n//=p
 print(d,'small factors',small,'cofactor digits',len(str(n)),flush=True)
 Path(f'analysis/cofactor{d}.txt').write_text(str(n))
 try:
  response=requests.get('https://factordb.com/api',params={'query':str(n)},timeout=30)
  Path(f'analysis/factordb{d}.json').write_text(response.text)
  print(d,response.status_code,response.text[:500],flush=True)
 except Exception as e:print(e,flush=True)
