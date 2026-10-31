import pickle,struct,z3,sys,json
from capstone import *
from capstone.x86 import *
t,patches=pickle.load(open('driver_analysis_trace.pkl','rb'));t=t[:23929];md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
names=['rax','rcx','rdx','rbx','rsp','rbp','rsi','rdi','r8','r9','r10','r11','r12','r13','r14','r15','eflags'];aliases={}
for i,r in enumerate(names[:16]):
 aliases[r]=(i,64,0)
 if i<8:
  aliases['e'+r[1:]]=(i,32,0);aliases[r[1:]]=(i,16,0)
  aliases[(r[1]+'l') if i<4 else r[1:]+'l']=(i,8,0)
  if i<4:aliases[r[1]+'h']=(i,8,8)
 else:
  for suf,bits in [('d',32),('w',16),('b',8)]:aliases[r+suf]=(i,bits,0)
C,K,I,A,F=[z3.BitVec(n,32) for n in ['cipher','key','index','rva','flags']]
sregs={14:z3.ZeroExt(32,I-1),15:z3.ZeroExt(32,K)};smem={};written=set();roots={};cache={};log=[];unknown=[]
def bv(x,bits):
 if isinstance(x,int):return z3.BitVecVal(x&((1<<bits)-1),bits)
 if x.size()==bits:return x
 return z3.Extract(bits-1,0,x) if x.size()>bits else z3.ZeroExt(bits-x.size(),x)
def clean(x):
 if isinstance(x,int):return x
 x=z3.simplify(x)
 return x.as_long() if z3.is_bv_value(x) else x
def readreg(name):
 i,b,o=aliases[name];v=sregs.get(i,rs[i]);return clean(z3.Extract(o+b-1,o,bv(v,64))) if not isinstance(v,int) else (v>>o)&((1<<b)-1)
def writereg(name,v):
 i,b,o=aliases[name]
 if isinstance(v,int) and (b>=32 or i not in sregs):sregs.pop(i,None);return
 v=bv(v,b)
 if b==32:v=z3.ZeroExt(32,v)
 elif b<64:
  old=bv(sregs.get(i,rs[i]),64);v=(old&z3.BitVecVal(~(((1<<b)-1)<<o)&((1<<64)-1),64))|(z3.ZeroExt(64-b,v)<<o)
 v=clean(v)
 if isinstance(v,int):sregs.pop(i,None)
 else:sregs[i]=v

def readmem(addr,sz):
 events=[m for m in mm if m[0]==16 and m[1]==addr]
 if events:con=events[0][3]
 else:raise ValueError(('missingread',hex(addr),sz,mm))
 if not any(addr+i in written for i in range(sz)):
  val=None
  if sz==4 and 0x141671008<=addr<0x14172a000:
   pos=(addr-0x141671008)%12
   if pos==0:val=A
   elif pos==4:val=C
   elif pos==8:val=F
  elif sz in (4,8):
   if con==0x7580794a:val=bv(K,sz*8)
   elif con==0x286f:val=bv(I-1,sz*8)
  if val is not None:
   for j in range(sz):smem[addr+j]=z3.Extract(j*8+7,j*8,bv(val,sz*8))
 if '--state' in sys.argv and 0x10fef390<=addr<0x10fef600:
  for j in range(sz):
   p=addr+j
   if p not in written and p not in smem:
    block=p&~7;rn=f's_{block:x}';word=z3.BitVec(rn,64);smem[p]=z3.Extract((p-block)*8+7,(p-block)*8,word)
    roots.setdefault(rn,{});roots[rn][p-block]=(con>>(j*8))&255
 vals=[smem.get(addr+i,(con>>(8*i))&255) for i in range(sz)]
 if all(isinstance(v,int) for v in vals):return sum(v<<(8*i) for i,v in enumerate(vals))
 return clean(z3.Concat(*[bv(v,8) for v in reversed(vals)])) if len(vals)>1 else vals[0]
def writemem(addr,sz,val):
 if isinstance(val,int):
  for i in range(sz):smem.pop(addr+i,None);written.add(addr+i)
  return
 val=bv(val,sz*8)
 for i in range(sz):
  p=addr+i;v=clean(z3.Extract(8*i+7,8*i,val));written.add(p)
  if isinstance(v,int):smem.pop(p,None)
  else:smem[p]=v

def addr(o):
 m=o.mem;res=m.disp
 for r,mul in [(m.base,1),(m.index,m.scale)]:
  if r:
   n=ins.reg_name(r)
   if n=='rip':res+=(a+len(bs))*mul
   elif n!='riz':res+=rs[aliases[n][0]]*mul
 return res&((1<<64)-1)
def operand(o):
 if o.type==X86_OP_IMM:return o.imm
 if o.type==X86_OP_REG:return readreg(ins.reg_name(o.reg))
 if o.type==X86_OP_MEM:return readmem(addr(o),o.size)
def write(o,v):
 if o.type==X86_OP_REG:writereg(ins.reg_name(o.reg),v)
 elif o.type==X86_OP_MEM:writemem(addr(o),o.size,v)
def sym(v):return not isinstance(v,int)
for ix,(a,bs,rs,mm) in enumerate(t):
 if ix%5000==0:print('PROGRESS',ix,flush=True)
 if a not in cache:cache[a]=next(md.disasm(bs,a))
 ins=cache[a];ops=ins.operands;n=ins.mnemonic;handled=False;vals=[]
 try:
  if n in ['mov','movabs','movzx','movsx','movsxd']:
   v=operand(ops[1]);vals=[v]
   if n in ('movsx','movsxd'):v=z3.SignExt(ops[0].size*8-ops[1].size*8,bv(v,ops[1].size*8))
   write(ops[0],v);handled=True
  elif n=='lea':
   # Only data taints in base/index, never include concrete addressing machinery.
   m=ops[1].mem;v=m.disp
   for rr,mul in [(m.base,1),(m.index,m.scale)]:
    if rr:
     rn=ins.reg_name(rr);x=(a+len(bs)) if rn=='rip' else (0 if rn=='riz' else readreg(rn));vals.append(x);v=bv(v,64)+bv(x,64)*mul
   write(ops[0],v);handled=True
  elif n=='push':
   v=operand(ops[0]);vals=[v];w=[m for m in mm if m[0]==17][0];writemem(w[1],w[2],v);handled=True
  elif n=='pop':
   m=[m for m in mm if m[0]==16][0];v=readmem(m[1],m[2]);vals=[v];write(ops[0],v);handled=True
  elif n in ('imul','mul') and len(ops)==1:
   w=ops[0].size*8;x=operand(ops[0]);y=readreg('eax' if w==32 else 'rax');vals=[x,y]
   if n=='imul':v=z3.SignExt(w,bv(x,w))*z3.SignExt(w,bv(y,w))
   else:v=z3.ZeroExt(w,bv(x,w))*z3.ZeroExt(w,bv(y,w))
   writereg('eax' if w==32 else 'rax',z3.Extract(w-1,0,v));writereg('edx' if w==32 else 'rdx',z3.Extract(2*w-1,w,v));handled=True
  elif n in ['add','sub','xor','or','and','shl','shr','sar','sal','rol','ror','imul','neg','not','inc','dec','bswap']:
   if n=='imul' and len(ops)==3:x,y=operand(ops[1]),operand(ops[2])
   else:x=operand(ops[0]);y=operand(ops[1]) if len(ops)>1 else None
   vals=[v for v in (x,y) if v is not None]
   if any(sym(v) for v in vals):
    w=ops[0].size*8;x=bv(x,w);y=bv(y,w) if y is not None else None
    if n=='add':v=x+y
    elif n=='sub':v=x-y
    elif n=='xor':v=x^y
    elif n=='or':v=x|y
    elif n=='and':v=x&y
    elif n in ['shl','sal']:v=x<<(y&(63 if w==64 else 31))
    elif n=='shr':v=z3.LShR(x,y&(63 if w==64 else 31))
    elif n=='sar':v=x>>(y&(63 if w==64 else 31))
    elif n=='rol':v=z3.RotateLeft(x,y&(63 if w==64 else 31))
    elif n=='ror':v=z3.RotateRight(x,y&(63 if w==64 else 31))
    elif n=='imul':v=x*y
    elif n=='neg':v=-x
    elif n=='not':v=~x
    elif n=='inc':v=x+1
    elif n=='dec':v=x-1
    elif n=='bswap':v=z3.Concat(*[z3.Extract(i+7,i,x) for i in range(0,w,8)])
    write(ops[0],v)
   else:
    if ops[0].type==X86_OP_REG:
     rn=ins.reg_name(ops[0].reg);i,w,o=aliases[rn]
     nxt=t[ix+1][2] if ix+1<len(t) else patches[-1][3]
     writereg(rn,(nxt[i]>>o)&((1<<w)-1))
    else:
     m=[m for m in mm if m[0]==17][0];writemem(m[1],m[2],m[3])
   handled=True
  elif n.startswith('j') or n in ('nop','cmp','test','ret','call','pushfq','popfq','clc','stc'):handled=True
  if not handled:
   rr,ww=ins.regs_access();tainted=[]
   for r in rr:
    rn=ins.reg_name(r)
    if rn in aliases and sym(readreg(rn)):tainted.append(rn)
   if tainted:unknown.append((ix,hex(a),n,ins.op_str,tainted))
   for r in ww:
    rn=ins.reg_name(r)
    if rn in aliases:
     i,w,o=aliases[rn];nxt=t[ix+1][2] if ix+1<len(t) else patches[-1][3];writereg(rn,(nxt[i]>>o)&((1<<w)-1))
  if any(sym(v) for v in vals):log.append((ix,hex(a),n,ins.op_str))
 except Exception as e:print('ERROR',ix,hex(a),n,ins.op_str,e);raise
open('driver_analysis_update_roots.json','w').write(json.dumps(roots,indent=2));print('UNKNOWN',unknown[:50],len(unknown));print('Tainted operations',len(log));res=clean(bv(sregs.get(1,patches[-1][3][1]),32));print('RESULT',res)
open('driver_analysis_update_expr.txt','w').write(str(res));pickle.dump(log,open('driver_analysis_update_ops.pkl','wb'))
s=z3.Solver();s.add(z3.BitVec('result',32)==res);open('driver_analysis_update.smt','w').write(s.to_smt2())
print('EVAL',z3.simplify(z3.substitute(res,(C,z3.BitVecVal(0xa7b8c0ea,32)),(K,z3.BitVecVal(0x7580794a,32)),(I,z3.BitVecVal(0x2870,32)),(A,z3.BitVecVal(0x1654e40,32)),(F,z3.BitVecVal(0,32)))))
