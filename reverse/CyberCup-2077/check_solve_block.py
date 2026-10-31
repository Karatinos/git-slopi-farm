from pathlib import Path
import z3 as z,time,argparse
p=argparse.ArgumentParser();p.add_argument('file');p.add_argument('target',type=lambda x:int(x,16));p.add_argument('--timeout',type=int,default=60000);p.add_argument('--prefix',default='');a=p.parse_args()
s=z.Solver();s.add(z.parse_smt2_file(a.file));s.set(timeout=a.timeout)
s.add(z.BitVec('state_00',32)==(a.target&0xffffffff),z.BitVec('state_04',32)==(a.target>>32))
w=[z.BitVec('input_word_%02d'%i,32) for i in range(2)]
for j,v in enumerate(a.prefix.encode()):s.add(z.Extract(j%4*8+7,j%4*8,w[j//4])==v)
t=time.time();r=s.check();print(r,'TIME',time.time()-t,flush=True)
if r==z.sat:
 m=s.model();b=b''.join(m.eval(x).as_long().to_bytes(4,'little') for x in w);print(b,flush=True)
