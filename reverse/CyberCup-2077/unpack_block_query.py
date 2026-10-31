from pathlib import Path
import unicorn,struct,random,time
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
B=0x140000000;data=Path('checker_final.bin').read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);u.mem_map(B,(len(data)+4095)&~4095);u.mem_write(B,data)
for a,s in [(0x10000000,0x1000000),(0x20000000,0x1000000),(0x30000000,0x20000),(0x7ff00000,0x100000)]:u.mem_map(a,s)
def put(a,v):u.mem_write(a,struct.pack('<Q',v))
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff01010,B);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);initial=u.context_save();hv=Hypervisor(pid=1234)
def hook(u,pc,size,d):
 if pc==0x140698a96:u.emu_stop();return
 hv.handle(u,pc,size)
u.hook_add(unicorn.UC_HOOK_CODE,hook)
def intr(u,n,d):
 if not hv.handle_exception(u,n):raise RuntimeError((n,hex(u.reg_read(UC_X86_REG_RIP))))
u.hook_add(unicorn.UC_HOOK_INTR,intr)
def query(x):
 u.context_restore(initial);u.mem_write(0x10fd0000,b'\0'*0x20000);u.mem_write(0x20000000,x.to_bytes(8,'little')+b'A'*58+b'}');u.emu_start(0x140698a19,0,count=1000000);return int.from_bytes(u.mem_read(sp+0x50,8),'little')
if __name__=='__main__':
 t=time.time();print('known', hex(query(int.from_bytes(b'ctfcup{A','little'))), flush=True)
 f0=query(0);print('zero',hex(f0),flush=True)
 for _ in range(5):
  a=random.getrandbits(64);b=random.getrandbits(64);fa=query(a);fb=query(b);fab=query(a^b);print('linear?',fab==fa^fb^f0,'pair',hex(a),hex(fa),flush=True)
 print('time',time.time()-t)
