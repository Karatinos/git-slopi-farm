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
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);u.mem_write(0x20000000,a.flag.encode());u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RSI,0)
snap=pickle.load(gzip.open('unpack_initialized_state.pkl.gz'))
for addr,blob in snap['mem']:
 if addr==0x30000000:u.mem_write(addr,blob)
apis=snap['apis'] if a.init else {}
u.mem_map(0x70000000,0x100000);u.mem_write(0x70000000,b'\xc3'*0x100000)
hv=Hypervisor(pid=1234,trace=lambda *x:print('HV',x) if x[0]=='trap' else None);last=[]
def hook(u,pc,size,data):
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
 if pc==0x141541b37:print('FINALRET',hex(u.reg_read(UC_X86_REG_RSP)),bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP),64)).hex())
 if hv.handle(u,pc,size):return
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
t=time.time()
try:
 if a.init:
  put(sp-8,0x140698a19);u.reg_write(UC_X86_REG_RSP,sp-8)
 u.emu_start(0x14161345b if a.init else 0x140698a19,0,count=10000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-t,'RIP',hex(u.reg_read(UC_X86_REG_RIP)),'STATE',bytes(u.mem_read(sp+0x50,80)).hex());print('LAST',list(map(hex,last)))

pickle.dump(hv.traps,open('driver_analysis_traps.pkl','wb'))
print('TRAPS',hv.traps)
