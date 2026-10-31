from pathlib import Path
import json,struct
from capstone import *
from capstone.x86_const import *
b=Path('check_clean.bin').read_bytes();w=Path('cc2_native_workspace.bin').read_bytes();m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
traps=json.loads(Path('cc2_init_0x1406987c0_traps.json').read_text());out=[]
for k,(s,t) in enumerate(traps.items()):
 pc=int(s);offset=None
 for i in m.disasm(b[pc-0x140000000:pc-0x140000000+50],pc):
  if i.operands and i.operands[0].type==X86_OP_MEM and i.operands[0].mem.base==X86_REG_R8:
   offset=i.operands[0].mem.disp;break
 if offset is None:print('NO OFFSET',k);continue
 vals=struct.unpack_from('<6I',w,offset)
 target=vals[3]|(vals[5]<<32)
 print(k,hex(offset),[hex(x) for x in vals],'target',hex(target),flush=True)
 out.append({'block':k,'offset':offset,'target':target,'words':list(vals)})
Path('cc2_expected.json').write_text(json.dumps(out,indent=2))
