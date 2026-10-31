from pathlib import Path
from capstone import *
from capstone.x86 import *
import sys
base=0x140000000
b=Path(sys.argv[1]).read_bytes()
md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
start=int(sys.argv[2],16);todo=[start];seen=set();n=0
while todo:
 pc=todo.pop(0)
 print(f'\nBLOCK {pc:x}')
 while pc not in seen and n<15000:
  if not 0<=pc-base<len(b):print('OUT OF RANGE');break
  ins=next(md.disasm(b[pc-base:pc-base+15],pc,count=1),None)
  if ins is None:print('BAD');break
  seen.add(pc);n+=1
  if ins.mnemonic!='nop':print(f'{pc:x}: {ins.mnemonic} {ins.op_str}')
  pc+=ins.size
  if ins.mnemonic=='ret':break
  if ins.group(CS_GRP_JUMP):
   if len(ins.operands)>0 and ins.operands[0].type==X86_OP_IMM:
    target=ins.operands[0].imm
    if ins.mnemonic=='jmp':pc=target
    elif target not in seen and target not in todo:todo.append(target)
   else:break
print('INSTRUCTIONS',n,'BLOCKS',len(seen))
