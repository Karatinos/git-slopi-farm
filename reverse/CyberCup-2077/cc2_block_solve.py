import json,sys,time
from pathlib import Path
import z3 as z
idx=int(sys.argv[1]);target=json.loads(Path('cc2_expected.json').read_text())[idx]['target'];cs=z.parse_smt2_file(f'cc2_block{idx}.smt2')
s=z.Solver();s.set(timeout=300000);s.add(cs)
s.add(z.BitVec(f'state_{idx*8:02}',32)==(target&0xffffffff),z.BitVec(f'state_{idx*8+4:02}',32)==target>>32)
for i in range(17):
 w=z.BitVec(f'input_word_{i:02}',32)
 for j in range(4):
  pos=i*4+j
  if pos>=67:continue
  c=z.Extract(j*8+7,j*8,w)
  if pos<8:s.add(c==b'ctfcup{d'[pos])
  elif pos==66:s.add(c==ord('}'))
  else:s.add(z.Or(z.And(c>=48,c<=57),z.And(c>=65,c<=90),z.And(c>=97,c<=122),c==95))
Path(f'cc2_query{idx}.smt2').write_text(s.to_smt2());print('SOLVING',idx,hex(target),flush=True)
t=time.time();r=s.check();print(r,time.time()-t,flush=True)
if r==z.sat:
 m=s.model();print(b''.join(m.eval(z.BitVec(f'input_word_{i:02}',32),model_completion=True).as_long().to_bytes(4,'little') for i in range(17)),flush=True)
