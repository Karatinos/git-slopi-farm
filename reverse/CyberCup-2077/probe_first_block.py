from pathlib import Path
import struct,string,time,unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
b=Path('check_clean.bin').read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);u.mem_map(0x140000000,(len(b)+4095)&~4095);u.mem_write(0x140000000,b);u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x10000)
hv=Hypervisor(pid=1234);u.hook_add(unicorn.UC_HOOK_CODE,hv.hook_code)
sp=0x10fe0000;out={};start=time.time()
for c in string.ascii_letters+string.digits+'_':
 u.mem_write(0x20000000,b'ctfcup{'+c.encode()+b'A'*58+b'}');u.mem_write(sp,bytes(0x3000));u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000)
 try:u.emu_start(0x140698a19,0x140698a96,count=1000000)
 except Exception as e:print('ERR',hex(u.reg_read(UC_X86_REG_RIP)),e);break
 val=struct.unpack('<Q',u.mem_read(sp+0x50,8))[0];out[c]=val
 print(c,hex(val),flush=True)
import json
Path('probe_first_block.json').write_text(json.dumps(out))
print('TIME',time.time()-start)
