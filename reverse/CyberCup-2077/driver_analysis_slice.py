import pickle
from capstone import *
from capstone.x86 import *
t,patches=pickle.load(open('driver_analysis_trace.pkl','rb'))
md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
names=['rax','rcx','rdx','rbx','rsp','rbp','rsi','rdi','r8','r9','r10','r11','r12','r13','r14','r15','eflags']
def canon(s):
 for i,r in enumerate(names):
  if s==r:return i
  if i<8 and s in [r[1:],r.replace('r','e',1),r[1]+'l',r[1]+'h']:return i
  if i>=8 and s in [r+'d',r+'w',r+'b']:return i
 return s
wanted={1};mem=set();sliced=[];cache={}
for idx in range(len(t)-1,-1,-1):
 a,b,rs,mm=t[idx]
 if a not in cache:cache[a]=next(md.disasm(b,a))
 ins=cache[a];reads,writes=ins.regs_access();writes={canon(ins.reg_name(r)) for r in writes};reads={canon(ins.reg_name(r)) for r in reads}
 mw={p for typ,addr,sz,val in mm if typ==17 for p in range(addr,addr+sz)}
 mr={p for typ,addr,sz,val in mm if typ==16 for p in range(addr,addr+sz)}
 if not (writes&wanted or mw&mem):continue
 wanted-=writes;mem-=mw;mem|=mr
 reads.discard(16)
 if ins.mnemonic not in ('lea','push','pop','ret','call'):
  for o in ins.operands:
   if o.type==X86_OP_MEM:
    for r in (o.mem.base,o.mem.index):
     if r:reads.discard(canon(ins.reg_name(r)))
 # Controlstack use doesn't matter when value is not rsp
 reads.discard(4);reads.discard('rip');reads.discard('ss');reads.discard('riz')
 wanted|=reads
 sliced.append((idx,ins,rs,mm,wanted.copy(),mem.copy()))
sliced.reverse()
with open('driver_analysis_slice.log','w') as f:
 print('Residual',wanted,len(mem),'slice',len(sliced),file=f)
 for idx,ins,rs,mm,need,m in sliced:
  print(idx,hex(ins.address),ins.mnemonic,ins.op_str,';',' '.join(f'{names[i]}={v:x}' for i,v in enumerate(rs) if i in range(16)),mm,file=f)
print('Slice',len(sliced),'of',len(t),'residual',wanted,'mem',len(mem))
