"""Symbolic shadow of native checker; table arithmetic is replaced by Z3 operations."""
from pathlib import Path
import argparse,struct,time,json,sys
import unicorn,unicorn.x86_const as ux
from capstone import *
from capstone.x86 import *
import z3 as z
from driver_analysis_hv import Hypervisor
B=0x140000000
mask=lambda n:(1<<n)-1

def norm(v,n):
 if isinstance(v,int):return v&mask(n)
 if v.size()>n:v=z.Extract(n-1,0,v)
 elif v.size()<n:v=z.ZeroExt(n-v.size(),v)
 v=z.simplify(v,mul2concat=True,bv_extract_prop=True,bv_sort_ac=True,sort_sums=True,local_ctx=True)
 return v.as_long() if z.is_bv_value(v) else v

def bv(v,n):return z.BitVecVal(v&mask(n),n) if isinstance(v,int) else norm(v,n)
def join(vals):
 if len(vals)==1:return vals[0]
 if all(isinstance(x,int) for x in vals):return sum(x<<(8*i) for i,x in enumerate(vals))
 return norm(z.Concat(*[bv(x,8) for x in vals[::-1]]),len(vals)*8)

class Shadow:
 def __init__(self,u):
  self.u=u;self.reg={};self.mem={};self.cache={};self.flags=False;self.flagstack={};self.n=0;self.unknown=0;self.tables=[];self.defs=[];self.bindings=[]
  self.md=Cs(CS_ARCH_X86,CS_MODE_64);self.md.detail=True
  for d in json.loads(Path('lut_catalog.json').read_text()):self.tables.append((int(d['rows'],16),int(d['data'],16),d['operation'][0]))
 def desc(self,r):
  s=self.md.reg_name(r)
  if s in ('rip','eip'):return 'rip',64 if s=='rip' else 32,0
  if s.startswith('r') and s[1:].rstrip('dwb').isdigit():
   e=s[-1];return s.rstrip('dwb'),{'d':32,'w':16,'b':8}.get(e,64),0
  names={'rax':['rax','eax','ax','al','ah'],'rbx':['rbx','ebx','bx','bl','bh'],'rcx':['rcx','ecx','cx','cl','ch'],'rdx':['rdx','edx','dx','dl','dh'],'rsp':['rsp','esp','sp','spl'],'rbp':['rbp','ebp','bp','bpl'],'rsi':['rsi','esi','si','sil'],'rdi':['rdi','edi','di','dil']}
  for q,xs in names.items():
   if s in xs:
    i=xs.index(s);return q,[64,32,16,8,8][i],8 if i==4 else 0
  return s,64,0
 def concrete_reg(self,r):return self.u.reg_read(getattr(ux,'UC_X86_REG_'+self.md.reg_name(r).upper()))
 def getreg(self,r):
  k,n,off=self.desc(r);v=self.reg.get(k)
  if v is None:return self.concrete_reg(r)
  return norm(z.LShR(v,off) if off else v,n)
 def setreg(self,r,v):
  k,n,off=self.desc(r);v=norm(v,n)
  if n>=32:new=norm(v,64)
  else:
   old=self.reg.get(k)
   if old is None:old=self.u.reg_read(getattr(ux,'UC_X86_REG_'+k.upper()))
   if isinstance(old,int) and isinstance(v,int):new=(old&~(mask(n)<<off))|(v<<off)
   else:new=norm((bv(old,64)&bv(~(mask(n)<<off),64))|(bv(v,64)<<off),64)
  if isinstance(new,int):self.reg.pop(k,None)
  else:self.reg[k]=new
 def addr(self,o,i):
  m=o.mem;c=m.disp;v=m.disp
  for reg,scale in [(m.base,1),(m.index,m.scale)]:
   if reg:
    cv=i.address+i.size if reg==X86_REG_RIP else self.concrete_reg(reg)
    sv=cv if reg==X86_REG_RIP else self.getreg(reg)
    c+=cv*scale;v=v+sv*scale
  return c&mask(64),norm(v,64)
 def fresh(self,v,n,c,size):
  v=norm(v,n)
  if isinstance(v,int):return v
  x=z.BitVec("lut_%05d"%len(self.defs),n);self.defs.append(x==v);self.bindings.append((x,z.BitVecVal(int.from_bytes(self.u.mem_read(c,size),"little"),n)));return x
 def readmem(self,c,a,size):
  if not isinstance(a,int):
   for rows,data,op in self.tables:
    if rows<=c<rows+2048:
     assert size==8
     return norm(bv(data,64)+(z.LShR(bv(a,64)-rows,3)<<8),64)
    if data<=c<data+65536:
     assert size==1
     off=bv(a,64)-data;x=z.Extract(15,8,off);y=z.Extract(7,0,off)
     if op=='xor':v=x^y
     elif op=='and':v=x&y
     elif op=='or':v=x|y
     elif op.startswith('funnel_left_'):
      n=int(op.rsplit('_',1)[1]);v=(x<<n)|z.LShR(y,8-n)
     return self.fresh(v,8,c,size)
   rows=0x140fd8600;data=0x1410d8600
   if rows<=c<data:
    assert size==8
    return norm(bv(data,64)+(z.LShR(bv(a,64)-rows,3)<<2),64)
   if data<=c<0x141158600:
    assert size==4
    return self.fresh(z.LShR(bv(a,64)-data,2),32,c,size)
   if 0x141158610<=c<0x141158710:
    return self.fresh(z.If(bv(a,64)==0x141158610,z.BitVecVal(1,8),z.BitVecVal(0,8)),8,c,size)
   raise ValueError(('SYMBOLIC ADDRESS',hex(c),a,size))
  data=bytes(self.u.mem_read(c,size));vals=[self.mem.get(c+j,data[j]) for j in range(size)]
  return join(vals)
 def get(self,o,i):
  if o.type==X86_OP_IMM:return o.imm&mask(o.size*8)
  if o.type==X86_OP_REG:return self.getreg(o.reg)
  if o.type==X86_OP_MEM:
   c,a=self.addr(o,i);return self.readmem(c,a,o.size)
  raise ValueError(o.type)
 def put(self,o,v,i):
  if o.type==X86_OP_REG:self.setreg(o.reg,v);return
  c,a=self.addr(o,i)
  if not isinstance(a,int):raise ValueError(('SYMBOLIC WRITE',hex(c),a))
  v=norm(v,o.size*8)
  for j in range(o.size):
   if isinstance(v,int):self.mem.pop(c+j,None)
   else:
    x=norm(z.Extract(j*8+7,j*8,v),8)
    if isinstance(x,int):self.mem.pop(c+j,None)
    else:self.mem[c+j]=x
 def unk(self,n):
  self.unknown+=1;return z.BitVec(f'UNKNOWN_{self.unknown}',n)
 def step(self,pc,size):
  i=self.cache.get(pc)
  if i is None:
   i=next(self.md.disasm(bytes(self.u.mem_read(pc,size)),pc));self.cache[pc]=i
  m=i.mnemonic;o=i.operands;self.n+=1
  if m in ('nop','jmp','ret','call','int3','vmmcall','cpuid'):return
  if m=='pushfq':self.flagstack[self.u.reg_read(ux.UC_X86_REG_RSP)-8]=self.flags;return
  if m=='popfq':self.flags=self.flagstack.get(self.u.reg_read(ux.UC_X86_REG_RSP),False);return
  if m=='push':
   v=self.get(o[0],i);addr=self.u.reg_read(ux.UC_X86_REG_RSP)-8
   for j in range(8):
    if isinstance(v,int):self.mem.pop(addr+j,None)
    else:self.mem[addr+j]=norm(z.Extract(j*8+7,j*8,bv(v,64)),8)
   return
  if m=='pop':
   addr=self.u.reg_read(ux.UC_X86_REG_RSP);self.put(o[0],self.readmem(addr,addr,8),i);return
  if m in ('clc','stc','cmc'):self.flags=False;return
  if m in ('mov','movabs','movzx','movsx','movsxd'):
   v=self.get(o[1],i)
   if m in ('movsx','movsxd'):
    n=o[1].size*8;t=o[0].size*8
    if isinstance(v,int):v=v-(1<<n) if v>>(n-1) else v
    else:v=z.SignExt(t-n,v)
   self.put(o[0],v,i);return
  if m=='lea':self.put(o[0],self.addr(o[1],i)[1],i);return
  if m=='xchg':
   a=self.get(o[0],i);b=self.get(o[1],i);self.put(o[0],b,i);self.put(o[1],a,i);return
  if m in ('xor','and','or','add','sub','neg','not','inc','dec','shl','sal','shr','sar','rol','ror','cmp','test'):
   a=self.get(o[0],i);n=o[0].size*8;b=self.get(o[1],i) if len(o)>1 else None
   sym=not isinstance(a,int) or (b is not None and not isinstance(b,int))
   if m in ('cmp','test'):self.flags=sym;return
   if sym:
    a=bv(a,n)
    if b is not None:b=bv(b,n)
   if m=='xor':v=a^b
   elif m=='and':v=a&b
   elif m=='or':v=a|b
   elif m=='add':v=a+b
   elif m=='sub':v=a-b
   elif m=='neg':v=-a
   elif m=='not':v=-a-1 if sym else ~a
   elif m=='inc':v=a+1
   elif m=='dec':v=a-1
   else:
    b=b&(63 if n==64 else 31)
    if m in ('shl','sal'):v=a<<b
    elif m=='shr':v=z.LShR(a,b) if sym else a>>b
    elif m=='sar':v=a>>b if sym else (a-(1<<n) if a>>(n-1) else a)>>b
    elif m in ('rol','ror'):
     if sym:v=z.RotateLeft(a,b) if m=='rol' else z.RotateRight(a,b)
     else:
      b%=n;v=(a<<b)|(a>>(n-b)) if m=='rol' else (a>>b)|(a<<(n-b))
   self.put(o[0],v,i)
   if m!='not':self.flags=sym
   return
  if m=='bswap':
   a=self.get(o[0],i);n=o[0].size
   if isinstance(a,int):v=int.from_bytes(a.to_bytes(n,'little'),'big')
   else:v=z.Concat(*[z.Extract(x*8+7,x*8,a) for x in range(n)])
   self.put(o[0],v,i);return
  reads,writes=i.regs_access();tainted=self.flags or any(not isinstance(self.getreg(r),int) for r in reads if self.md.reg_name(r) not in ('rflags','eflags'))
  for r in writes:
   s=self.md.reg_name(r)
   if s in ('rflags','eflags'):self.flags=tainted
   elif s.startswith(('xmm','ymm','zmm')):pass
   else:
    if tainted:self.setreg(r,self.unk(self.desc(r)[1]))
    else:self.reg.pop(self.desc(r)[0],None)

def main():
 p=argparse.ArgumentParser();p.add_argument('image');p.add_argument('--stop-stage',type=int,default=1000);p.add_argument('--validate',action='store_true');p.add_argument('--solve',action='store_true');p.add_argument('--word-input',action='store_true');p.add_argument('--no-workspace',action='store_true');p.add_argument('--traps');p.add_argument('--transforms-only',action='store_true');p.add_argument('--output',default='check_state.smt2');a=p.parse_args()
 data=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);u.mem_map(B,(len(data)+4095)&~4095);u.mem_write(B,data)
 u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x20000);u.mem_map(0x7ff00000,0x100000)
 def put(p,x):u.mem_write(p,struct.pack('<Q',x))
 u.reg_write(ux.UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff01010,B);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
 sp=0x10fe0000;u.reg_write(ux.UC_X86_REG_RSP,sp);u.reg_write(ux.UC_X86_REG_RBP,sp+0x100);u.reg_write(ux.UC_X86_REG_RDI,0x20000000)
 concrete=b'ctfcup{'+b'A'*59+b'}';u.mem_write(0x20000000,concrete);u.reg_write(ux.UC_X86_REG_RBX,0);u.reg_write(ux.UC_X86_REG_RSI,0)
 hv=Hypervisor(pid=1234);s=Shadow(u);words=[z.BitVec('input_word_%02d'%x,32) for x in range(17)];chars=[z.Extract((x%4)*8+7,(x%4)*8,words[x//4]) for x in range(67)] if a.word_input else [z.BitVec('flag_%02d'%x,8) for x in range(67)]
 for j,x in enumerate(chars):s.mem[0x20000000+j]=x
 if a.traps:
  ts=json.loads(Path(a.traps).read_text())
  hv.traps={int(k,0) if isinstance(k,str) else k:tuple(int(x,0) if isinstance(x,str) else x for x in v) for k,v in ts.items()}
 stages=0;done=False;prevpc=0;t=time.time();last=[]
 def hook(u,pc,size,d):
  nonlocal stages,done,prevpc
  if len(last)>20:last.pop(0)
  last.append(pc)
  if size==1 and bytes(u.mem_read(pc,1))==b'\x90':
   chunk=bytes(u.mem_read(pc,256));n=0
   while n<len(chunk) and chunk[n]==0x90:n+=1
   u.reg_write(ux.UC_X86_REG_RIP,pc+n);return
  if pc in hv.traps and hv.traps[pc][0]==3 and u.reg_read(ux.UC_X86_REG_R10)==hv.traps[pc][2]:
   u.reg_write(ux.UC_X86_REG_R10,hv.traps[pc][1]);s.reg.pop('r10',None)
  if hv.handle(u,pc,size):return
  if pc==0x140698edb:
   print('RESULT',u.reg_read(ux.UC_X86_REG_EAX),'symbolic',s.getreg(X86_REG_EAX),flush=True);done=True;u.emu_stop();return
  if pc==0x140699420:
   rsp=u.reg_read(ux.UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(ux.UC_X86_REG_RSP,rsp+8);u.reg_write(ux.UC_X86_REG_RIP,ra);return
  if 0x140698a19<=pc<0x140698edb and bytes(u.mem_read(pc,1))==b'\xe8':
   stages+=1;print('STAGE',stages,'PC',hex(pc),'TIME',time.time()-t,'SYMBYTES',len(s.mem),'UNKNOWN',s.unknown,flush=True)
   if stages>a.stop_stage:u.emu_stop();return
   transform_stages=set(range(1,6))|set(range(8,12))|set(range(14,18))|set(range(20,24))|set(range(26,31))|set(range(33,37))|set(range(39,43))|set(range(45,49))|set(range(51,56))
   if a.transforms_only and stages not in transform_stages:
    if stages>55:u.emu_stop();return
    u.reg_write(ux.UC_X86_REG_RIP,pc+size);return
  s.step(pc,size)
 u.hook_add(unicorn.UC_HOOK_CODE,hook)
 def intr(u,n,d):
  if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(ux.UC_X86_REG_RIP))))
 u.hook_add(unicorn.UC_HOOK_INTR,intr)
 try:u.emu_start(0x140698a19,0,count=10000000)
 except Exception as e:print('ERROR',repr(e),'LAST',list(map(hex,last)),flush=True);raise
 print('FINISHED',time.time()-t,'INSTRUCTIONS',s.n,flush=True)
 if a.validate:
  subs=[(x,z.BitVecVal(int.from_bytes((concrete+b'\0')[j*4:j*4+4],'little'),32)) for j,x in enumerate(words)] if a.word_input else [(x,z.BitVecVal(concrete[j],8)) for j,x in enumerate(chars)];subs+=s.bindings;bad=[]
  for addr,v in s.mem.items():
   ev=z.simplify(z.substitute(bv(v,8),*subs));actual=u.mem_read(addr,1)[0]
   if not z.is_bv_value(ev) or ev.as_long()!=actual:bad.append((hex(addr),str(ev),actual))
  print('VALIDATION_BAD',len(bad),bad[:20],flush=True)
 out={}
 for off in range(0x2080):
  v=s.mem.get(sp+0xa0+off)
  if v is not None:out[off]=v
 solver=z.Solver();solver.add(s.defs)
 for x in chars:solver.add(z.UGE(x,32),z.ULE(x,126))
 for j,v in enumerate(b'ctfcup{'):solver.add(chars[j]==v)
 solver.add(chars[-1]==ord('}'))
 if done:
  result=s.getreg(X86_REG_EAX);solver.add(bv(result,32)==1)
  Path('check_constraints.smt2').write_text(solver.to_smt2())
  if a.solve:
   print('SOLVING',flush=True);r=solver.check();print(r,flush=True)
   if r==z.sat:print('FLAG',bytes(solver.model().eval(x).as_long() for x in chars).decode(),flush=True)
 if not a.no_workspace:
  summary=z.Solver();summary.add(s.defs)
  for off,v in out.items():summary.add(z.BitVec('workspace_%04x'%off,8)==v)
  Path('check_workspace.smt2').write_text(summary.to_smt2())
 state_solver=z.Solver();state_solver.add(s.defs)
 for off in range(0,72,4):state_solver.add(z.BitVec('state_%02d'%off,32)==s.readmem(sp+0x50+off,sp+0x50+off,4))
 Path(a.output).write_text(state_solver.to_smt2())
if __name__=='__main__':main()
