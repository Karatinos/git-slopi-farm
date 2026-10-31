"""Run the isolated input transformation, omitting UI and timing checks."""
from pathlib import Path
import argparse,struct,time,pickle,gzip
import unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
P=argparse.ArgumentParser();P.add_argument('image');P.add_argument('flag',nargs='?',default='ctfcup{'+'A'*59+'}');P.add_argument('--trace',action='store_true');P.add_argument('--init',action='store_true');a=P.parse_args()
b=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);base=0x140000000
u.mem_map(base,(len(b)+4095)&~4095);u.mem_write(base,b)
u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x10000000);u.mem_map(0x7ff00000,0x100000)
def put(p,x):u.mem_write(p,struct.pack('<Q',x))
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000);put(0x7ff00008,0x11000000);put(0x7ff00010,0x10000000);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);u.mem_write(0x20000000,a.flag.encode());u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RSI,0)
snap=pickle.load(gzip.open('unpack_initialized_state.pkl.gz'))
for addr,blob in snap['mem']:
 if addr==0x30000000:u.mem_write(addr,blob)
apis=snap['apis'] if a.init else {}
u.mem_map(0x70000000,0x100000);u.mem_write(0x70000000,b'\xc3'*0x100000)
hv=Hypervisor(pid=1234,trace=lambda *x:print('HV',x) if x[0]=='trap' else None);last=[]; history=[]
tsc=100000000
def hook(u,pc,size,data):
 global tsc
 raw=bytes(u.mem_read(pc,min(size,3)))
 if raw[:2]==b'\x0f\x31' or raw[:3]==b'\x0f\x01\xf9':
  tsc+=100;u.reg_write(UC_X86_REG_EAX,tsc);u.reg_write(UC_X86_REG_EDX,0);u.reg_write(UC_X86_REG_RIP,pc+size);print('RDTSC',hex(pc),tsc);return
 if pc in apis:
  name=apis[pc];print('API',name,'RCX',hex(u.reg_read(UC_X86_REG_RCX)),'RDX',hex(u.reg_read(UC_X86_REG_RDX)))
  if name=='GetCurrentProcess':v=0xffffffffffffffff
  elif name in ['GetCurrentProcessId','GetCurrentThreadId']:v=1234
  elif name=='IsDebuggerPresent':v=0
  elif name=='CheckRemoteDebuggerPresent':u.mem_write(u.reg_read(UC_X86_REG_RDX),b'\0'*4);v=1
  elif name=='NtQueryInformationProcess':
   cl=u.reg_read(UC_X86_REG_EDX);buf=u.reg_read(UC_X86_REG_R8);sz=u.reg_read(UC_X86_REG_R9);print('QUERY',cl,hex(buf),sz);u.mem_write(buf,(1 if cl==31 else 0).to_bytes(sz,'little'));v=0
  elif name=='VirtualProtect':
   put(u.reg_read(UC_X86_REG_R9),0x40);v=1
  elif name=='GetSystemTimeAsFileTime':put(u.reg_read(UC_X86_REG_RCX),13245678900123456);v=1
  elif name=='QueryPerformanceCounter':put(u.reg_read(UC_X86_REG_RCX),123456789);v=1
  elif name=='GetTickCount':v=123456
  else:raise RuntimeError(('API',name))
  rsp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RAX,v);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ret);return
 if pc==0x141541b37:print('FINALRET',hex(u.reg_read(UC_X86_REG_RSP)),bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP),64)).hex())
 if hv.handle(u,pc,size):return
 history.append([pc]+[u.reg_read(r) for r in [UC_X86_REG_RAX,UC_X86_REG_RBX,UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_RSP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_RBP,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15,UC_X86_REG_EFLAGS]])
 if pc==0x140698edb:
  print('RESULT',hex(u.reg_read(UC_X86_REG_EAX)));u.emu_stop();return
 if pc==0x140699420: # MSVC security-cookie verification outside the transform.
  rsp=u.reg_read(UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ra);return
 if len(last)>20:last.pop(0)
 last.append(pc)
 if a.trace and 0x140698a19<=pc<0x140698edb:print('MAIN',hex(pc))
u.hook_add(unicorn.UC_HOOK_CODE,hook)
def intr(u,n,data):
 if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(UC_X86_REG_RIP))))
u.hook_add(unicorn.UC_HOOK_INTR,intr)
def invalid(u,access,p,n,v,data):
 print('UNMAPPED',access,hex(p),n,hex(u.reg_read(UC_X86_REG_RIP)))
 for n in ['RAX','RCX','RDX','RBX','RSI','RDI','RBP','RSP','R8','R9','R10','R11','R12','R13','R14','R15']:print(n,hex(u.reg_read(globals()['UC_X86_REG_'+n])))
 return False
u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
def cpuid(u,d):
 leaf=u.reg_read(UC_X86_REG_EAX);sub=u.reg_read(UC_X86_REG_ECX);vals=[0,0,0,0]
 if leaf==0x4ffffffd:
  x=sub^0x9c3017a5;x^=x>>16;x=x*0x7feb352d&0xffffffff;x^=x>>15;x=x*0x846ca68b&0xffffffff;x^=x>>16
  vals=[leaf,x^0x43453032^0x73d45bc1,0x41434631,0]
 elif leaf==0x4fffffff:
  vals=[leaf,0x706d6953,0x7653656c,0x2020206d]
  if sub==1:vals=[leaf,0,0,0x20000]
  elif sub==2:vals=[leaf,0,0,0]
  elif sub==3:vals=[leaf,1,1,0]
  elif sub==4:vals=[leaf,0x43453032,0x4241434b,0x414c4953]
 elif leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
 elif leaf==1:vals=[0x306a9,0x00010800,0x7ffafbff,0xbfebfbff]
 elif leaf==0x80000000:vals=[0x80000008,0,0,0]
 elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
 elif leaf==0x80000008:vals=[0x3028,0,0,0]
 elif leaf in [0x80000002,0x80000003,0x80000004]:vals=list(struct.unpack('<4I',b'Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz          '.ljust(48,b' ')[(leaf-0x80000002)*16:(leaf-0x80000001)*16]))
 print('CPUID',hex(leaf),hex(sub),flush=True)
 for reg,val in zip([UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX],vals):u.reg_write(reg,val)
 return True
u.hook_add(unicorn.UC_HOOK_INSN,cpuid,None,1,0,UC_X86_INS_CPUID)
def watch(u,ac,addr,size,val,data):
 if val&0xffffffff==0xdeadc0de:
  print('DEADWRITE',hex(addr),size,hex(val),'PC',hex(u.reg_read(UC_X86_REG_RIP)))
  print('PREHISTORY',history[-20:])
u.hook_add(unicorn.UC_HOOK_MEM_WRITE,watch)
t=time.time()
try:
 if a.init:
  put(sp-8,0x140698a19);u.reg_write(UC_X86_REG_RSP,sp-8)
 u.emu_start(0x1406987c0 if a.init else 0x140698a19,0,count=10000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-t,'RIP',hex(u.reg_read(UC_X86_REG_RIP)),'STATE',bytes(u.mem_read(sp+0x50,80)).hex());print('LAST',list(map(hex,last)))

import json
Path('cc2_ready_clear_trace.json').write_text(json.dumps(history))
Path('cc2_clear_traps.json').write_text(json.dumps(hv.traps))
print('TRAPS',hv.traps)
