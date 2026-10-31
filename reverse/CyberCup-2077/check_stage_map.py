from pathlib import Path
from capstone import *
from capstone.x86 import *
import json
b=Path('checker_deobf.bin').read_bytes();B=0x140000000;m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
stages=[i.operands[0].imm for i in m.disasm(b[0x698a19:0x698edb],B+0x698a19) if i.mnemonic=='call'];out=[]
for st in stages:
 seen=set();pc=st;reads=set();states=set();calls=[]
 while pc not in seen:
  seen.add(pc);i=next(m.disasm(b[pc-B:pc-B+15],pc,count=1),None)
  if i is None:break
  pc+=i.size
  for o in i.operands:
   if o.type==X86_OP_MEM and o.mem.base==X86_REG_RCX:reads.add(o.mem.disp)
   if o.type==X86_OP_MEM and o.mem.base==X86_REG_RDX:states.add(o.mem.disp)
  if i.mnemonic=='ret':break
  if i.mnemonic=='call':calls.append(i.op_str)
  if i.mnemonic=='jmp':
   if i.operands[0].type!=X86_OP_IMM:break
   pc=i.operands[0].imm
 out.append({'stage':hex(st),'ins':len(seen),'input':sorted(reads),'state':sorted(states),'calls':calls})
 print(out[-1],flush=True)
Path('check_stage_map.json').write_text(json.dumps(out,indent=2))
