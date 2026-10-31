from pathlib import Path
import sys,time
from pyboolector import Boolector,BtorOption
idx=int(sys.argv[1]);src=Path(f'cc2_query{idx}.smt2').read_text().replace('(check-sat)','');p=Path(f'cc2_query{idx}_btor.smt2');p.write_text(src)
b=Boolector();b.Set_opt(BtorOption.BTOR_OPT_MODEL_GEN,1)
print('PARSE',b.Parse(str(p)),flush=True);t=time.time();r=b.Sat();print('RESULT',r,'TIME',time.time()-t,flush=True)
if r==b.SAT:
 b.Print_model('smt2',f'cc2_btor{idx}_model.smt2')
 for i in range(17):
  try:
   w=b.Match_by_symbol(f'input_word_{i:02}');print(i,int(w.assignment,2).to_bytes(4,'little'),flush=True)
  except Exception:pass
