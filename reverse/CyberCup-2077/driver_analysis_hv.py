"""Unicorn-friendly model of cybercup.sys user-facing hypervisor services.
Use hv=Hypervisor(); uc.hook_add(UC_HOOK_CODE,hv.hook_code).
Only the challenge's custom CPU behavior is emulated; normal Windows APIs
are the caller's responsibility. Timeouts/concurrency/hardware counters omitted.
"""
from unicorn.x86_const import *
from driver_analysis_arm import arm,injection,GPRS,MASK
from check_hypercall import Capabilities,CheckSessions,Tickets,rol
R={name:globals()['UC_X86_REG_'+name.upper()] for name in GPRS}
R.update(rip=UC_X86_REG_RIP,eflags=UC_X86_REG_EFLAGS)
MAGIC=0x43434248564c4142

def ror(x,n):return rol(x,64-n)
def mix32(x):
 x^=x>>16;x=x*0x7feb352d&0xffffffff;x^=x>>15;x=x*0x846ca68b&0xffffffff;return x^(x>>16)

class Hypervisor:
 def __init__(self,pid=1,key=(0,0),trace=None):
  self.pid=pid;self.cap=Capabilities(*key);self.arm_sessions={};self.next_arm=0
  self.overrides={};self.traps={};self.trace=trace;self.events=[]
  self.source=0x43453032;self.counter={};self.check=CheckSessions(*key);self.tickets=Tickets()
 def event(self,*args):
  self.events.append(args)
  if self.trace:self.trace(*args)
 def install(self,address,code,mask,flags=0):
  value=(list(code),mask,flags)
  if address in self.overrides and self.overrides[address]!=value:raise ValueError('conflicting ARM override')
  self.overrides[address]=value;self.event('install',address,value)
 def run_override(self,u,address,size=3):
  code,mask,flags=self.overrides[address];old=[u.reg_read(R[r]) for r in GPRS]
  status,result,nzcv=arm(code,old+[0]*16)
  if status:raise RuntimeError(('ARM error',address,status,code))
  for i,reg in enumerate(GPRS):
   width=(mask>>(i*3))&7
   if not width:continue
   bits=[0,8,16,32,64][width];m=(1<<bits)-1
   val=(result[i]&m) if width>=3 else ((old[i]&~m)|(result[i]&m))
   u.reg_write(R[reg],val)
   if flags:
    ef=u.reg_read(R['eflags'])&~0x8d5
    ef|=(int((val&255).bit_count()%2==0)<<2)|(int(val==0)<<6)|(((val>>(bits-1))&1)<<7)
    u.reg_write(R['eflags'],ef)
  u.reg_write(R['rip'],address+size);self.event('override',address,old,result[:16])
 def cpuid(self,u,address):
  eax=u.reg_read(R['rax'])&0xffffffff;ecx=u.reg_read(R['rcx'])&0xffffffff
  get=lambda r:u.reg_read(R[r]);out=None
  if eax==0x4ffffffd:
   out=(eax,mix32(ecx^0x9c3017a5)^self.source^0x73d45bc1,0x41434631,0)
   self.counter[7]=(ecx,out[1],self.counter.get(7,(0,0,0))[2]+1)
  elif eax==0x4ffffffe and ecx==0x43594355 and get('r10')==0x4856435049443131:
   val=self.cap.call(self.pid,0x3021,get('r8'),get('r9'),MASK)
   out=(val&0xffffffff,0x43594355,0,val>>32)
  elif eax==0x4fffffff:
   out=(eax,0x706d6953,0x7653656c,0x2020206d)
   if ecx==1:out=(eax,0,0,0x20000)
   elif ecx==2:out=(eax,0,0,0)
   elif ecx==3:out=(eax,1,1,0)
   elif ecx==4:out=(eax,self.source,0x4241434b,0x414c4953)
   elif ecx==5:out=(eax,self.counter.get('hc',0),0,0x484d5554)
   elif ecx in (6,7):out=(eax,*self.counter.get(ecx,(0,0,0)))
   elif ecx==8:out=(eax,0,0,0x41444754)
  if out is None:return False
  for reg,val in zip(('rax','rbx','rcx','rdx'),out):u.reg_write(R[reg],val&0xffffffff)
  u.reg_write(R['rip'],address+2);self.event('cpuid',address,eax,ecx,out);return True
 def call(self,op,a=0,b=0,c=0,rax=0,rbx=0,next_rip=0):
  """Arguments map RDX op,R8 a,R9 b,R10 c,RAX rax,RBX rbx. Returns RAX,RDX."""
  self.counter['hc']=self.counter.get('hc',0)+1
  if op in (0x3201,0x3202,0x3203):
   if not 1<=c<=64:return MASK,1
   code,mask,flags=injection(op,a,b);self.install(next_rip+c,code,mask,flags);return 0,0
  if op in (0x3301,0x3302):
   kind=rax if op==0x3301 else 3;base=a if op==0x3301 else b
   e1,e2=(b,c) if op==0x3301 else (c,rax)
   target=ror(((e1^e2)-base*0x9e3779b97f4a7c15)&MASK,17)
   if kind not in (1,2,3) or not 0x10000<=target<=0x7fffffffffff:return MASK,1
   self.traps[a]=(kind,target,0 if kind!=3 else b);self.event('trap',a,kind,target,b);return 0,0
  if op==0x3200:
   status,r,_=arm([a],[rax,rbx]+[0]*30)
   return (r[0],0) if status==0 else (rax,status+1)
  if op==0x31ff:return 0x20000,0
  if op==0x3100:
   self.next_arm+=1;token=self.cap.hash(self.next_arm,self.pid,0x41524d564d303031)
   if token in (0,MASK):token^=0x42
   self.arm_sessions[token]={'code':[],'regs':[0]*32,'done':False};return token,0
  if 0x3101<=op<=0x3106:
   s=self.arm_sessions.get(b)
   if not s:return MASK,1
   if op==0x3101 and not s['done'] and c==0 and a<=0xffffffff and len(s['code'])<64:s['code'].append(a);return len(s['code']),0
   if op==0x3102 and not s['done'] and a<31:s['regs'][a]=c;return 0,0
   if op==0x3103 and not s['done'] and not a and not c:
    status,r,_=arm(s['code'],s['regs'])
    if status:return (1<<63)|status,0
    s['regs']=r;s['done']=True;return 0,0
   if op==0x3104 and not c:
    if a==31:del self.arm_sessions[b];return 0,0
    if a<31 and s['done']:return s['regs'][a],0
   if op==0x3105 and not a and not c:
    regs=s['regs'].copy();regs[0]=rax;status,r,_=arm(s['code'],regs);s['done']=True
    return (r[0],0) if status==0 else (rax,status+1)
   if op==0x3106 and s['code']:
    self.install(a,s['code'],c,0);s['done']=True;return 0,0
   return MASK,1
  if 0x3050<=op<=0x305f and self.check:return self.check.call(self.pid,op,a,b),1
  if 0x3000<=op<=0x30ff:return self.cap.call(self.pid,op,a,b,0),1
  if self.tickets:return self.tickets.call(self.pid,op,a,b),1
  raise NotImplementedError(('unknown hypercall',hex(op),a,b,c,rax,next_rip))
 def handle(self,u,address,size=None):
  """Call from UC_HOOK_CODE; returns True if handled and RIP advanced."""
  raw=bytes(u.mem_read(address,3));get=lambda r:u.reg_read(R[r])
  if address in self.traps and self.traps[address][0] in (1,2):
   _,target,_=self.traps[address];u.reg_write(R['rip'],target);self.event('transfer',address,target);return True
  if raw[:2]==b'\x0f\xa2':return self.cpuid(u,address)
  if raw==b'\x0f\x01\xd9':
   if address in self.overrides:self.run_override(u,address);return True
   if get('rcx')!=MAGIC:raise RuntimeError(('unrecognized VMMCALL',address,get('rcx')))
   args=(get('rdx'),get('r8'),get('r9'),get('r10'),get('rax'),get('rbx'),address+3)
   val,status=self.call(*args);u.reg_write(R['rax'],val&MASK);u.reg_write(R['rdx'],status&MASK);u.reg_write(R['rip'],address+3)
   self.event('hypercall',address,args,(val,status));return True
  if raw[:2]==b'\x0f\x0b' and get('r10')==0x4856545241503131 and get('rdx')==0x3011:
   val=self.cap.call(self.pid,0x3011,get('r8'),get('r9'),address)
   if val==MASK:raise RuntimeError('invalid capability UD2')
   u.reg_write(R['rax'],val);u.reg_write(R['rip'],address+1);return True
  if raw[:1]==b'\xcc' and get('r10')==0x4856425245414b31 and get('rdx')==0x3041:
   val=self.cap.call(self.pid,0x3041,get('r8'),get('r9'),address)
   if val==MASK:raise RuntimeError('invalid capability INT3')
   u.reg_write(R['rax'],val);u.reg_write(R['rip'],address+1);return True
  return False
 def hook_code(self,u,address,size,user_data=None):self.handle(u,address,size)
 def resolve_fault(self,u,address,access):
  """For parent emulator exception handler. access='fetch' or 'read'."""
  pc=u.reg_read(R['rip'])
  if access=='fetch' and address in self.traps and self.traps[address][0]==1:
   u.reg_write(R['rip'],self.traps[address][1]);return True
  if access=='read' and pc in self.traps:
   kind,target,source=self.traps[pc]
   if kind==3 and address==source:u.reg_write(R['r10'],target);return True
  return False

 def handle_exception(self,u,vector,address=None):
  """Handle Unicorn UC_HOOK_INTR #UD6/#BP3; address is faulting RIP."""
  if address is None:address=u.reg_read(R['rip'])-(1 if vector==3 else 0)
  get=lambda r:u.reg_read(R[r]);op=0x3011 if vector==6 else 0x3041
  magic=0x4856545241503131 if vector==6 else 0x4856425245414b31
  if vector not in (3,6) or get('r10')!=magic or get('rdx')!=op:return False
  val=self.cap.call(self.pid,op,get('r8'),get('r9'),address)
  if val==MASK:return False
  u.reg_write(R['rax'],val);u.reg_write(R['rip'],address+1);return True
