from pathlib import Path
from capstone import *
from capstone.x86 import *
import struct,json,collections
B=0x140000000;b=Path('checker_deobf.bin').read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
stages=[i.operands[0].imm for i in md.disasm(b[0x698a19:0x698edb],B+0x698a19) if i.mnemonic=='call']
todo=list(stages);seen=set();gs=collections.Counter()
while todo:
 pc=todo.pop()
 while pc not in seen:
  seen.add(pc);i=next(md.disasm(b[pc-B:pc-B+15],pc,count=1),None)
  if i is None:break
  pc+=i.size
  for o in i.operands:
   if o.type==X86_OP_MEM and o.mem.base==X86_REG_RIP:gs[pc+o.mem.disp]+=1
  if i.mnemonic=='ret':break
  if i.mnemonic=='jmp':
   if i.operands[0].type!=X86_OP_IMM:break
   pc=i.operands[0].imm
  elif i.group(CS_GRP_JUMP):
   if i.operands[0].type==X86_OP_IMM:todo.append(i.operands[0].imm)
ops={}
for name,f in [('xor',lambda x,y:x^y),('or',lambda x,y:x|y),('and',lambda x,y:x&y)]:ops[name]=f
for k in range(1,8):ops['shl'+str(k)]=lambda x,y,k=k:((x<<k)|(y>>(8-k)))&255
for k in range(1,8):ops['shr'+str(k)]=lambda x,y,k=k:((x>>k)|(y<<(8-k)))&255
result={}
for a,n in gs.most_common():
 p=struct.unpack_from('<Q',b,a-B)[0]
 if not 0<=p-B<len(b)-2048:continue
 ps=struct.unpack_from('<256Q',b,p-B)
 if not all(0<=v-B<len(b)-255 for v in ps):
  t=b[p-B:p-B+256]
  kind='eq0' if t==b'\1'+b'\0'*255 else 'not' if t==bytes([x^255 for x in range(256)]) else 'unary'+t.hex()
  result[a]={'pointer':p,'kind':kind,'n':n};print(hex(a),n,'unary',kind[:80]);continue
 stride=ps[1]-ps[0];regular=all(ps[x]==ps[0]+x*stride for x in range(256))
 ts=[b[v-B:v-B+256] for v in ps]
 match=[name for name,f in ops.items() if all(ts[x][y]==f(x,y) for x in range(256) for y in range(256))]
 if stride==4 and regular:
  words=struct.unpack_from('<511I',b,ps[0]-B)
  if words==tuple(range(511)):match=['add32']
 print(hex(a),n,hex(p),'stride',stride,'regular',regular,'kind',match)
 result[a]={'pointer':p,'matrix':ps[0],'stride':stride,'regular':regular,'kind':match,'n':n}
Path('check_tables.json').write_text(json.dumps(result,indent=2))
print('STAGES',len(stages),'INS',len(seen))
