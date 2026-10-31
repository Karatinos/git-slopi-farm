from pathlib import Path
from capstone import *
from capstone.x86 import *
import struct,json,collections
B=0x140000000;b=Path('unpack_memory.bin').read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
seen=set(); todo=[0x14126f3ea,0x1413f20a8];globals=collections.Counter()
while todo:
 pc=todo.pop()
 while pc not in seen:
  seen.add(pc);ins=next(md.disasm(b[pc-B:pc-B+15],pc,count=1),None)
  if not ins:break
  pc+=ins.size
  for o in ins.operands:
   if o.type==X86_OP_MEM and o.mem.base==X86_REG_RIP:globals[pc+o.mem.disp]+=1
  if ins.mnemonic=='ret':break
  if ins.mnemonic=='jmp':
   if ins.operands[0].type==X86_OP_IMM:pc=ins.operands[0].imm
   else:break
  elif ins.group(CS_GRP_JUMP):
   if ins.operands[0].type==X86_OP_IMM:todo.append(ins.operands[0].imm)

def q(a):return struct.unpack_from('<Q',b,a-B)[0]
for a,n in globals.most_common():
 p=q(a)
 if not 0<=p-B<len(b):print(hex(a),n,'BAD',hex(p));continue
 ps=[q(p+x*8) for x in range(256)]
 if all(0<=v-B<len(b)-255 for v in ps):
  ts=[b[v-B:v-B+256] for v in ps]
  ops={'xor':lambda x,y:x^y,'or':lambda x,y:x|y,'and':lambda x,y:x&y,'add':lambda x,y:(x+y)&255,'sub':lambda x,y:(x-y)&255,'carryadd':lambda x,y:int(x+y>255),'borrowsub':lambda x,y:int(x<y),'mul':lambda x,y:x*y&255,'eq':lambda x,y:int(x==y),'neq':lambda x,y:int(x!=y),'shl':lambda x,y:(x<<y)&255,'shr':lambda x,y:x>>y}
  match=[name for name,f in ops.items() if all(ts[x][y]==f(x,y) for x in range(256) for y in range(256))]
  print(hex(a),n,hex(p),'binary',match,'rowsample',[(x,list(ts[x][:8])) for x in range(3)])
 else:
  t=b[p-B:p-B+256];print(hex(a),n,hex(p),'unary',list(t[:32]),'unique',len(set(t)))
