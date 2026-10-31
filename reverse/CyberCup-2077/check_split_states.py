from pathlib import Path
import z3 as z,json,sys
path=sys.argv[1] if len(sys.argv)>1 else 'check_all_states.smt2'
cs=z.parse_smt2_file(path);defs={}
for c in cs:
 if z.is_eq(c) and z.is_const(c.arg(0)) and c.arg(0).decl().kind()==z.Z3_OP_UNINTERPRETED:defs[str(c.arg(0))]=c

def variables(x):
 todo=[x];seen=set();result={}
 while todo:
  n=todo.pop();h=n.get_id()
  if h in seen:continue
  seen.add(h)
  if z.is_const(n) and n.decl().kind()==z.Z3_OP_UNINTERPRETED:result[str(n)]=n
  else:todo.extend(n.children())
 return result
for block in range(9):
 need=[f'state_{block*8:02d}',f'state_{block*8+4:02d}'];seen=set();out=[];inputs=set()
 while need:
  name=need.pop()
  if name in seen:continue
  seen.add(name)
  if name.startswith('input_'):inputs.add(name)
  c=defs.get(name)
  if c is not None:
   out.append(c);need.extend(variables(c.arg(1)))
 s=z.Solver();s.add(out);Path(f'check_block{block}.smt2').write_text(s.to_smt2())
 print(block,'nodes',len(out),'inputs',sorted(inputs),flush=True)
