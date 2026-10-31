from pathlib import Path
import z3 as z,time
cs=z.parse_smt2_file('cc2_block0.smt2')
s=z.Then('simplify','propagate-values','solve-eqs','bit-blast','sat').solver();s.set(timeout=60000);s.add(cs)
s.add(z.BitVec('state_00',32)==0xc49415c3,z.BitVec('state_04',32)==0x9b98bc82)
for i in range(2):
 w=z.BitVec('input_word_%02d'%i,32)
 for j in range(4):
  x=z.Extract(j*8+7,j*8,w);s.add(z.UGE(x,32),z.ULE(x,126))
t=time.time();r=s.check();print(r,time.time()-t,flush=True)
if r==z.sat:
 m=s.model();print(b''.join(m.eval(z.BitVec('input_word_%02d'%i,32)).as_long().to_bytes(4,'little') for i in range(2)),flush=True)
