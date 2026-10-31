import pefile, struct, random
from unicorn import *
from unicorn.x86_const import *
from driver_analysis_arm import *
p=pefile.PE('cybercup.sys');base=p.OPTIONAL_HEADER.ImageBase
u=Uc(UC_ARCH_X86,UC_MODE_64);u.mem_map(base,0x70000);u.mem_write(base,p.get_memory_mapped_image());u.mem_map(0x400000,0x10000)
def run(code, regs):
 data=struct.pack('<32Q',*regs)+bytes(8)
 u.mem_write(0x400000,struct.pack('<'+'I'*len(code),*code));u.mem_write(0x401000,data)
 u.reg_write(UC_X86_REG_RSP,0x40f000);u.mem_write(0x40f000,struct.pack('<Q',0x402000))
 u.reg_write(UC_X86_REG_RCX,0x400000);u.reg_write(UC_X86_REG_RDX,len(code));u.reg_write(UC_X86_REG_R8,0x401000)
 u.emu_start(base+0x1260,0x402000,count=100000)
 out=bytes(u.mem_read(0x401000,264));return u.reg_read(UC_X86_REG_RAX),list(struct.unpack('<32Q',out[:256])),tuple(out[256:260])
rng=random.Random(123)
for i in range(200):
 r=[rng.getrandbits(64) for j in range(32)];code=[]
 for j in range(8):
  typ=rng.randrange(5);d,n,m=[rng.randrange(32) for k in range(3)]
  if typ==0:ins=rng.choice([0xd2800000,0xf2800000])|d|(rng.randrange(65536)<<5)|(rng.randrange(4)<<21)
  elif typ==1:ins=rng.choice([0x8a000000,0xaa000000,0xca000000])|d|(n<<5)|(m<<16)
  elif typ==2:ins=0xeb00001f|(n<<5)|(m<<16)
  elif typ==3:ins=0xf100001f|(n<<5)|(rng.randrange(4096)<<10)
  else:ins=0x54000000|(1<<5)|rng.randrange(14)
  code.append(ins)
 a=arm(code,r);b=run(code,r)
 assert a==b,(i,a,b,list(map(hex,code)))
print('200 mixed ARM programs agree exactly with original driver function emulated in Unicorn')
