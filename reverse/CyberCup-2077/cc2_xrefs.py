from pathlib import Path
from capstone import *
from capstone.x86_const import *
b=Path('unpack_initialized.bin').read_bytes();B=0x140000000
m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True;m.skipdata=True
for start,end in [(0x1000,0x6e3e00),(0x124b000,0x1671000)]:
 for i in m.disasm(b[start:end],B+start):
  if not i.id:continue
  vals=[]
  for o in i.operands:
   if o.type==X86_OP_MEM and o.mem.base==X86_REG_RIP:vals.append((i.address+i.size+o.mem.disp)&((1<<64)-1))
   if o.type==X86_OP_IMM:vals.append(o.imm)
  for v in vals:
   if 0x141158700<=v<0x141158900 or v in [0x1405cf80,0x1405e3670]:print(hex(i.address),i.mnemonic,i.op_str,'TARGET',hex(v),flush=True)
