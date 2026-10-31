from pathlib import Path
import json,struct
from capstone import *
from capstone.x86_const import *
b=Path('check_clean.bin').read_bytes();B=0x140000000;m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
stages=json.loads(Path('check_stage_map.json').read_text());traps=json.loads(Path('cc2_init_0x1406987c0_traps.json').read_text());targets=[]
for k,(pc,trap) in enumerate(traps.items()):
 idx=next(i for i,d in enumerate(stages) if int(d['stage'],16)<=int(pc)<int(d['stage'],16)+20)
 entry=int(stages[idx+1]['stage'],16);todo=[entry];seen=set();consts=[]
 while todo:
  pc=todo.pop()
  while pc not in seen:
   seen.add(pc);i=next(m.disasm(b[pc-B:pc-B+15],pc,count=1));pc+=i.size
   if i.id==X86_INS_NOP:continue
   if len(i.operands)==2 and i.operands[0].type==X86_OP_MEM and i.operands[1].type==X86_OP_IMM and (i.operands[1].imm&0xffffffff)>0xffff:
    consts.append((hex(i.address),i.mnemonic,i.op_str,i.operands[1].imm&0xffffffff))
   if i.mnemonic=='ret':break
   if i.group(CS_GRP_JUMP):
    if i.operands[0].type!=X86_OP_IMM:break
    if i.mnemonic=='jmp':pc=i.operands[0].imm
    else:todo.append(i.operands[0].imm)
 print(k,hex(entry),consts,flush=True)
 val=struct.unpack_from('<Q',b,trap[1]-B)[0]
 if len(consts)==2:
  target=val^consts[0][-1]^(consts[1][-1]<<32)
  targets.append(target);print('TARGET',hex(target),flush=True)
Path('cc2_targets.json').write_text(json.dumps(targets))
