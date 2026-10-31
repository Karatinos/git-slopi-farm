import pefile,unicorn,struct
from unicorn.x86_const import *
from check_hypercall import *
p=pefile.PE('cybercup.sys');base=p.OPTIONAL_HEADER.ImageBase
u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);u.mem_map(base,0x70000);u.mem_write(base,p.get_memory_mapped_image());u.mem_map(0x100000,0x10000);u.mem_map(0xff78000000000,0x1000)
u.mem_write(base+0x80c8,struct.pack('<I',1));u.mem_write(base+0x92d0,struct.pack('<Q',0x101000));u.mem_write(0x101000,struct.pack('<QQ',0x123456,0x765432))
m=Capabilities(0x123456,0x765432)
def call(op,arg=0,token=0,extra=0):
 a=[123,op,arg,token,extra];sp=0x108000
 for r,v in zip([UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9],a):u.reg_write(r,v)
 u.reg_write(UC_X86_REG_RSP,sp);u.mem_write(sp,struct.pack('<Q',base+0x6000));u.mem_write(sp+40,struct.pack('<Q',a[4]))
 u.emu_start(base+0x315c,base+0x6000,count=1000000)
 actual=u.reg_read(UC_X86_REG_RAX);expected=m.call(*a)
 print(hex(op),hex(actual),hex(expected));assert actual==expected
 return actual
call(0x30ff);call(0x30fe);t=call(0x3000,0x99887)
t=call(0x3001,0x100000023,t);call(0x3030,0x1234,t)
call(0x3010,0x100000,t);t=call(0x3011,0x200000023,t,0x100000)
t=call(0x3021,0x300000023,t,MASK)
call(0x3040,0x101000,t);t=call(0x3041,0x400000023,t,0x101000)
call(0x3002,0,t)
print('Capabilities API matches driver open, query, predictor, four step channels, close')
