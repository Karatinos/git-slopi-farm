import pefile,struct
from unicorn import *
from unicorn.x86_const import *
from driver_analysis_hv import mix32
p=pefile.PE('cybercup.sys');base=p.OPTIONAL_HEADER.ImageBase
u=Uc(UC_ARCH_X86,UC_MODE_64);u.mem_map(base,0x70000);u.mem_write(base,p.get_memory_mapped_image());u.mem_map(0x400000,0x800000)
def w(a,x,n=8):u.mem_write(a,x.to_bytes(n,'little'))
vm=0x500000;ctx=0x510000;regs=0x511000;shared=0x600000
w(vm+0x64cb,3,1);w(vm+0x5fe8,shared);w(shared+0x407000,0x414c49534241434b);w(base+0x80c8,1,4);w(base+0x70b4,0x43453032,4);w(ctx,regs)
for leaf,sub in [(0x4ffffffd,0xacf2077),(0x4ffffffd,0xacf2078),(0x4fffffff,4)]:
 w(regs+0x78,leaf);w(regs+0x70,sub);w(0x40f000,0x402000)
 u.reg_write(UC_X86_REG_RSP,0x40f000);u.reg_write(UC_X86_REG_RCX,vm);u.reg_write(UC_X86_REG_RDX,ctx)
 u.emu_start(base+0x1db4,0x402000,count=100000)
 result=[int.from_bytes(u.mem_read(regs+x,8),'little') for x in (0x78,0x60,0x70,0x68)]
 print(hex(leaf),hex(sub),'->',*[hex(x) for x in result])
 expect=[leaf,mix32(sub^0x9c3017a5)^0x43453032^0x73d45bc1,0x41434631,0] if leaf==0x4ffffffd else [leaf,0x43453032,0x4241434b,0x414c4953]
 assert result==expect,(result,expect)
