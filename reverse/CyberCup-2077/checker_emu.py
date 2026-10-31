"""Run the isolated input transformation, omitting UI and timing checks."""
from pathlib import Path
import argparse,struct,time,pickle,gzip
import unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
P=argparse.ArgumentParser();P.add_argument('image');P.add_argument('flag',nargs='?',default='ctfcup{'+'A'*59+'}');P.add_argument('--trace',action='store_true');P.add_argument('--init',action='store_true');P.add_argument('--full',action='store_true');a=P.parse_args()
b=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);base=0x140000000
u.mem_map(base,(len(b)+4095)&~4095);u.mem_write(base,b)
u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x20000);u.mem_map(0x7ff00000,0x100000)
def put(p,x):u.mem_write(p,struct.pack('<Q',x))
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);u.mem_write(0x20000000,a.flag.encode());u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RSI,0)
saved=pickle.load(gzip.open('unpack_initialized_state.pkl.gz')) if a.init else None
apis=saved['apis'] if saved else {}
if saved:
 for ma,mb in saved['mem']:
  if ma==0x30000000: u.mem_write(ma,mb)
u.mem_map(0x70000000,0x100000);u.mem_write(0x70000000,b'\xc3'*0x100000)
hv=Hypervisor(pid=1234);last=[]
def hook(u,pc,size,data):
 if pc==0x140698930:
  rsp=u.reg_read(UC_X86_REG_RSP);u.reg_write(UC_X86_REG_RIP,struct.unpack('<Q',u.mem_read(rsp,8))[0]);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RAX,1);return
 if pc==0x141541b37:print('VMRETURN',hex(u.reg_read(UC_X86_REG_RAX)),hex(u.reg_read(UC_X86_REG_RSP)),u.mem_read(u.reg_read(UC_X86_REG_RSP),32).hex())
 if pc in hv.traps and hv.traps[pc][0]==3:
  _,target,source=hv.traps[pc];u.reg_write(UC_X86_REG_R10,struct.unpack('<Q',u.mem_read(target,8))[0]);u.reg_write(UC_X86_REG_RIP,pc+3);return
 if pc in apis:
  name=apis[pc];print('API',name)
  if name=='GetCurrentProcess':v=0xffffffffffffffff
  elif name in ['GetCurrentProcessId','GetCurrentThreadId']:v=1234
  elif name=='IsDebuggerPresent':v=0
  elif name=='CheckRemoteDebuggerPresent':u.mem_write(u.reg_read(UC_X86_REG_RDX),b'\0'*4);v=1
  elif name=='NtQueryInformationProcess':
   cl=u.reg_read(UC_X86_REG_EDX);buf=u.reg_read(UC_X86_REG_R8);sz=u.reg_read(UC_X86_REG_R9);print('QUERY',cl,hex(buf),sz);u.mem_write(buf,(1 if cl==31 else 0).to_bytes(sz,'little'));v=0
  elif name=='VirtualProtect':
   put(u.reg_read(UC_X86_REG_R9),0x40);v=1
  else:raise RuntimeError(('API',name))
  rsp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RAX,v);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ret);return
 if hv.handle(u,pc,size):return
 if pc==0x140698edb:
  print('RESULT',hex(u.reg_read(UC_X86_REG_EAX)));u.emu_stop();return
 if pc==0x140699420: # MSVC security-cookie verification outside the transform.
  rsp=u.reg_read(UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ra);return
 if len(last)>20:last.pop(0)
 last.append(pc)
 if a.trace and 0x140698a19<=pc<0x140698edb:print('MAIN',hex(pc))
def cpuid_normal(u,data):
 leaf=u.reg_read(UC_X86_REG_EAX);vals=[0,0,0,0]
 if leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
 elif leaf==1:vals=[0x306a9,0x00010800,0x7ffafbff,0xbfebfbff]
 elif leaf==0x80000000:vals=[0x80000008,0,0,0]
 elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
 elif leaf==0x80000008:vals=[0x3028,0,0,0]
 for r,v in zip([UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX],vals):u.reg_write(r,v)
 return True
u.hook_add(unicorn.UC_HOOK_INSN,cpuid_normal,None,1,0,UC_X86_INS_CPUID)
u.hook_add(unicorn.UC_HOOK_CODE,hook)
def intr(u,n,data):
 if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(UC_X86_REG_RIP))))
u.hook_add(unicorn.UC_HOOK_INTR,intr)
def invalid(u,access,p,n,v,data):print('UNMAPPED',access,hex(p),n,hex(u.reg_read(UC_X86_REG_RIP)));return False
u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
t=time.time()
try:
 if a.init:
  put(sp-8,0x140698a19);u.reg_write(UC_X86_REG_RSP,sp-8)
 if a.full:
  u.reg_write(UC_X86_REG_RCX,0x20000000);u.reg_write(UC_X86_REG_RDX,len(a.flag));u.reg_write(UC_X86_REG_RAX,1)
 u.emu_start(0x14166fe79 if a.full else (0x1406987c0 if a.init else 0x140698a19),0,count=10000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-t,'RIP',hex(u.reg_read(UC_X86_REG_RIP)),'STATE',bytes(u.mem_read(sp+0x50,80)).hex());print('LAST',list(map(hex,last)));import json;Path('checker_traps.json').write_text(json.dumps(hv.traps));Path('checker_events.json').write_text(json.dumps(hv.events))
