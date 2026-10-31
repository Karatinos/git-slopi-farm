import z3 as z,random,time,json
from pathlib import Path
exprs=list(z.parse_smt2_file('check_state.smt2'))
def vs(x):
 todo=[x];seen=set();v={}
 while todo:
  n=todo.pop();nid=n.get_id()
  if nid in seen:continue
  seen.add(nid)
  if z.is_const(n) and n.decl().kind()==z.Z3_OP_UNINTERPRETED:v[str(n)]=n
  else:todo.extend(n.children())
 return list(v.values())
def simp(x):return z.simplify(x,mul2concat=True,bv_extract_prop=True,bv_sort_ac=True,sort_sums=True,local_ctx=True)
def width(x,n):return x if x.size()==n else z.ZeroExt(n-x.size(),x) if x.size()<n else z.Extract(n-1,0,x)
repls=[];outputs=[];report=[]
for idx,e in enumerate(exprs):
 if not z.is_eq(e):outputs.append(e);continue
 l,r=e.children();r=simp(z.substitute(r,*repls)) if repls else simp(r);v=vs(r);n=l.size();mask=(1<<n)-1
 candidates=[]
 def add(c):
  c=simp(c)
  if not any(z.eq(c,x) for x in candidates):candidates.append(c)
 if len(v)<=3:
  samples=[]
  for t in range(7):
   vals=[z.BitVecVal((0 if t==0 else 1 if t==1 else (1<<x.size())-1 if t==2 else random.getrandbits(x.size())),x.size()) for x in v]
   result=simp(z.substitute(r,*zip(v,vals)))
   if not z.is_bv_value(result):break
   samples.append((list(zip(v,vals)),result.as_long()))
  if len(samples)==7:
   atoms=[]
   for x in v:
    atoms.append(width(x,n))
    if x.size()>n:
     for off in range(n,x.size(),n):
      if off+n<=x.size():atoms.append(z.Extract(off+n-1,off,x))
   add(z.BitVecVal(samples[0][1],n))
   for x in atoms:
    c=samples[0][1];add(x+c);add(x^c);add(c-x)
    for sh in range(1,min(n,9)):
     add(x<<sh);add(z.LShR(x,sh));add(z.RotateLeft(x,sh));add(z.RotateRight(x,sh))
   for x in atoms:
    for y in atoms:
     if z.eq(x,y):continue
     for val in [x+y,x-y,x^y,x&y,x|y]:
      add(val+samples[0][1]);add(val^samples[0][1])
   good=[]
   for c in candidates:
    if all(simp(z.substitute(c,*vals)).as_long()==ans for vals,ans in samples):good.append(c)
   for c in good:
    if z.eq(c,r):break
    s=z.Solver();s.set(timeout=500);s.add(r!=c)
    if s.check()==z.unsat:
     r=c;print(idx,l,'=>',r,flush=True);report.append((str(l),str(r)));break
 # substitute short expressions to accumulate alias/known constants, but not nonlinear byte ops
 if z.is_bv_value(r) or (z.is_const(r) and r.decl().kind()==z.Z3_OP_UNINTERPRETED):repls.append((l,r))
 outputs.append(l==r)
 if idx%20==0:print('PROGRESS',idx,'repl',len(repls),flush=True)
s=z.Solver();s.add(outputs);Path('unpack_reduced.smt2').write_text(s.to_smt2());Path('unpack_reduce_report.json').write_text(json.dumps(report,indent=2))
