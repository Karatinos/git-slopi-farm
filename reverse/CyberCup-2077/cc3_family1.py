"""Solve the small, directly verified six-round family, not lifted SSA."""
from pathlib import Path
import json,sys,time,string
import z3 as z

j=int(sys.argv[1]);p=json.loads(Path('cc3_params.json').read_text())[j]
assert p['kind']==1
t=json.loads(Path('cc2_expected.json').read_text())[j]['target']
c=[z.BitVec(f'c{i}',8) for i in range(8)]
ss=[x^p['masks'][i] for i,x in enumerate(c)]
qq=[ss[i]^(x+p['p'][i])^p['q'][i] for i,x in enumerate(c)]
rr=[x+q for x,q in zip(c,qq)]
a,b=z.BitVecVal(p['a'],32),z.BitVecVal(p['b'],32)
for i in range(6):
    k=z.ZeroExt(24,ss[i])+257+65*i
    a=z.RotateLeft((a^k)+b,7+i)
    b=a^z.RotateLeft(b+(a^k),11+i)
outa=b^z.Concat(*reversed(rr[4:8]))
outb=a^z.Concat(*reversed(qq[:4]))
solver=z.SolverFor('QF_BV');solver.set(timeout=120000)
for x in c:solver.add(z.Or(*[x==ord(k) for k in string.ascii_letters+string.digits+'_']))
solver.add(outa==t&0xffffffff,outb==t>>32)
Path(f'cc3_family1_{j}.smt2').write_text(solver.to_smt2())
start=time.time();results=[]
while True:
    result=solver.check();print('STATUS',j,result,'seconds',time.time()-start,flush=True)
    if result!=z.sat:break
    m=solver.model();v=bytes(m.eval(x).as_long() for x in c).decode()
    results.append(v);print('CANDIDATE',j,v,flush=True)
    Path(f'cc3_family1_{j}.json').write_text(json.dumps(results,indent=2)+'\n')
    solver.add(z.Or(*[x!=ord(k) for x,k in zip(c,v)]))
