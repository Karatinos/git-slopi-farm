from pathlib import Path
import json,struct,sys,time
import unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
B=0x140000000;b=Path('check_clean.bin').read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
u.mem_map(B,(len(b)+4095)&~4095);u.mem_write(B,b);u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x10000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000)
flag=sys.argv[1] if len(sys.argv)>1 else 'ctfcup{'+'A'*59+'}';u.mem_write(0x20000000,flag.encode())
h=Hypervisor(pid=1234);h.traps={int(k):v for k,v in json.loads(Path('cc2_init_0x1406987c0_traps.json').read_text()).items()}
def hook(u,pc,size,data):
 if pc in h.traps:
  kind,target,source=h.traps[pc]
  if kind==3 and u.reg_read(UC_X86_REG_R10)==source:u.reg_write(UC_X86_REG_R10,target)
 if h.handle(u,pc,size):return
 if pc==0x140698edb:print('RESULT',u.reg_read(UC_X86_REG_EAX),flush=True);u.emu_stop();return
 if pc==0x140699420:
  rsp=u.reg_read(UC_X86_REG_RSP);u.reg_write(UC_X86_REG_RIP,struct.unpack('<Q',u.mem_read(rsp,8))[0]);u.reg_write(UC_X86_REG_RSP,rsp+8)
u.hook_add(unicorn.UC_HOOK_CODE,hook)
t=time.time();u.emu_start(0x140698a19,0,count=10000000);print('TIME',time.time()-t,'PC',hex(u.reg_read(UC_X86_REG_RIP)))
Path('cc2_native_workspace.bin').write_bytes(u.mem_read(sp+0xa0,0x20b0));Path('cc2_native_state.bin').write_bytes(u.mem_read(sp+0x50,72));print('STATE',u.mem_read(sp+0x50,72).hex())
