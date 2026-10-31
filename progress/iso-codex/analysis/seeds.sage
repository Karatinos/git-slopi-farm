import gmpy2,time
from pathlib import Path
nums=[gmpy2.mpz(Path('analysis/primitive_n%d.txt'%d).read_text()) for d in [2,4,6]]
a=6079433314242371108270239373533376748;b=-1779744368654530162000920720207404089
nums.append(gmpy2.mpz(4*a^3+27*b^2+31104*2^64*a*b))
seeds=list(range(20000))+[31337,65537,123456,1234567,12345678,123456789,2026,20261021,20261031,0xdeadbeef,0xcafebabe]
seeds+=list(range(1792610180,1792610210))
t=time.time()
for i,seed in enumerate(seeds):
 set_random_seed(seed)
 p=gmpy2.next_prime(gmpy2.mpz(getrandbits(128)))
 if p<2*a:continue
 for d,n in zip([2,4,6,0],nums):
  if n%p==0:print('MATCH',seed,p,d,flush=True)
 if i%5000==0:print('progress',i,'seconds',time.time()-t,flush=True)
print('done',time.time()-t,flush=True)
