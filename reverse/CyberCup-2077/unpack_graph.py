import z3 as z
from pathlib import Path
exprs=list(z.parse_smt2_file('check_state.smt2'))
def vars(x):
 todo=[x];seen=set();v={}
 while todo:
  n=todo.pop();nid=n.get_id()
  if nid in seen:continue
  seen.add(nid)
  if z.is_const(n) and n.decl().kind()==z.Z3_OP_UNINTERPRETED:v[str(n)]=n
  else:todo.extend(n.children())
 return v
supports={};deps={}
with open('unpack_graph.txt','w') as f:
 for e in exprs:
  if not z.is_eq(e):continue
  l,r=e.children();name=str(l);vs=vars(r);deps[name]=set(vs)
  su=set()
  for v in vs:su.update(supports.get(v,{v}))
  supports[name]=su
  f.write('%s %s [%s] = %s\n' %(name,','.join(sorted(su)),','.join(vs),str(r).replace('\n',' ')))
for name in supports:
 if name.startswith('state'):print(name,supports[name],deps[name])
