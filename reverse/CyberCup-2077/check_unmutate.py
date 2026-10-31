"""Cancel syntactically inverse register mutation inside pushfq/popfq regions."""
from pathlib import Path
from capstone import *
from capstone.x86 import *
import argparse,json
p=argparse.ArgumentParser();p.add_argument('image');p.add_argument('--output',default='check_clean.bin');a=p.parse_args()
b=bytearray(Path(a.image).read_bytes());m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True;B=0x140000000;patches=[];offset=0;allowed=set()
starts=[i.operands[0].imm for i in m.disasm(bytes(b[0x698a19:0x698edb]),B+0x698a19) if i.mnemonic=="call"]
for start in starts:
 pc=start
 while pc not in allowed:
  allowed.add(pc);ins=next(m.disasm(bytes(b[pc-B:pc-B+15]),pc,count=1),None)
  if ins is None or ins.mnemonic=="ret":break
  pc+=ins.size
  if ins.mnemonic=="jmp":
   if ins.operands[0].type!=X86_OP_IMM:break
   pc=ins.operands[0].imm
candidates=iter(sorted(pc-B for pc in allowed if b[pc-B]==0x9c))
while True:
 offset=next(candidates,-1)
 if offset<0:break
 start=offset;offset+=1
 ins=list(m.disasm(bytes(b[start:start+220]),B+start));end=next((i for i,x in enumerate(ins[1:],1) if x.mnemonic=='popfq'),None)
 if not end:continue
 ins=ins[:end+1]
 if any(x.mnemonic in ('push','call','jmp','pushfq','vmmcall','ret') for x in ins[1:-1]):continue
 seq=[];valid=True
 for j,x in enumerate(ins[1:-1],1):
  o=x.operands
  if len(o)>0 and o[0].type==X86_OP_REG:
   if len(o)==2 and o[1].type==X86_OP_IMM and x.mnemonic in ('xor','add','sub','rol','ror'):
    seq.append((x.mnemonic,o[0].reg,o[1].imm,j))
   elif len(o)==1 and x.mnemonic in ('neg','not'):
    seq.append((x.mnemonic,o[0].reg,None,j))
   else:seq.append(('barrier',None,None,j))
  else:seq.append(('barrier',None,None,j))
 stack=[];cancel=[]
 for x in seq:
  stack.append(x);changed=True
  while changed:
   changed=False
   if len(stack)>=3:
    aa,bb,cc=stack[-3:]
    if aa[1]==bb[1]==cc[1] and (aa[0],bb[0],cc[0],cc[2]) in [('neg','not','add',1),('not','neg','sub',1)]:
     cancel.extend(y[3] for y in stack[-3:]);del stack[-3:];changed=True;continue
   if len(stack)>=2:
    aa,bb=stack[-2:]
    inverse=(aa[0]==bb[0] and aa[0] in ('xor','neg','not') and aa[2]==bb[2]) or ((aa[0],bb[0]) in [('add','sub'),('sub','add'),('rol','ror'),('ror','rol')] and aa[2]==bb[2])
    if aa[1]==bb[1] and inverse:
     cancel.extend(y[3] for y in stack[-2:]);del stack[-2:];changed=True
 if cancel:
  for j in cancel:
   x=ins[j];b[x.address-B:x.address-B+x.size]=b'\x90'*x.size
  patches.append({'start':hex(B+start),'end':hex(ins[-1].address+ins[-1].size),'removed':len(cancel),'remaining':[f'{ins[x[3]].mnemonic} {ins[x[3]].op_str}' for x in stack]})
Path(a.output).write_bytes(b);Path(a.output+'.json').write_text(json.dumps(patches,indent=2));print('groups',len(patches),'removed',sum(x['removed'] for x in patches))
