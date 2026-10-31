from pathlib import Path
import struct,numpy as np
from capstone import *
from capstone.x86_const import *
b=Path('unpack_initialized.bin').read_bytes();B=0x140000000;m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
for align in range(4):
 n=(len(b)-align)//4;ar=np.frombuffer(b,dtype='<i4',count=n,offset=align).astype(np.int64)
 offs=np.arange(n,dtype=np.int64)*4+align;targets=ar+offs+4+B
 ids=np.flatnonzero((targets>=0x141158700)&(targets<0x141158900))
 for j in ids:
  off=int(offs[j]);target=int(targets[j]);found=False
  for start in range(max(0,off-8),off):
   i=next(m.disasm(b[start:off+5],B+start),None)
   if i and i.address+i.size==B+off+4 and any(o.type==X86_OP_MEM and o.mem.base==X86_REG_RIP for o in i.operands):print(hex(i.address),i.mnemonic,i.op_str,'TARGET',hex(target),flush=True);found=True
  if not found:print('POSSIBLE',hex(B+off),hex(target),b[off-5:off+5].hex(),flush=True)
for target in [0x141158710,0x141158818,0x14005cf80]:
 for sz in [4,8]:
  p=0;raw=(target if sz==8 else target-B).to_bytes(sz,'little')
  while True:
   p=b.find(raw,p)
   if p<0:break
   print('DIRECT',sz,hex(target),hex(B+p),flush=True);p+=1
