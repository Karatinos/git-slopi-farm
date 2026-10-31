"""Evaluate environment-masked constant thunks in a fully unpacked image.
Writes thunk_values.json and optionally patches an image; environment is explicit.
"""
from pathlib import Path
import argparse,json,struct,random
from capstone import *
from unicorn import *
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor,R,GPRS
p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--output',default='driver_analysis_thunks.bin');p.add_argument('--pid',type=int,default=1234);a=p.parse_args()
BASE=0x140000000;data=Path(a.input).read_bytes();out=bytearray(data)
u=Uc(UC_ARCH_X86,UC_MODE_64);u.mem_map(BASE,(len(data)+4095)&~4095);u.mem_write(BASE,data)
u.mem_map(0x10000000,0x100000);u.mem_map(0x7ff00000,0x100000);u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000)
u.mem_map(0x30000000,0x10000)
def put(addr,val):u.mem_write(addr,struct.pack('<Q',val))
put(0x7ff00060,0x7ff01000);put(0x7ff01010,BASE);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000);put(0x7ff00040,a.pid)
h=Hypervisor(pid=a.pid)
def oncode(uc,addr,size,ud):
 if bytes(uc.mem_read(addr,2))==b'\x0f\xa2':
  if h.cpuid(uc,addr):return
  leaf=uc.reg_read(R['rax'])&0xffffffff;vals=[0,0,0,0]
  if leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
  elif leaf==1:vals=[0x306a9,0x00010800,0x7ffafbff,0xbfebfbff]
  elif leaf==0x80000000:vals=[0x80000008,0,0,0]
  elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
  elif leaf==0x80000008:vals=[0x3028,0,0,0]
  for name,v in zip(('rax','rbx','rcx','rdx'),vals):uc.reg_write(R[name],v)
  uc.reg_write(R['rip'],addr+2)
 else:h.handle(uc,addr,size)
u.hook_add(UC_HOOK_CODE,oncode)
prologue=bytes.fromhex('9c505351524150415141524153');epilogue=bytes.fromhex('415b415a415941585a595b589d')
md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
results=[];start=0
while True:
 start=data.find(prologue,start)
 if start<0:break
 end=data.find(epilogue,start+len(prologue),start+4096)
 if end<0:start+=len(prologue);continue
 instructions=list(md.disasm(data[start:end],BASE+start))
 saved_write=[i for i in instructions if i.mnemonic=='mov' and i.op_str.startswith('qword ptr [rsp + ') and i.op_str.endswith(', r11')]
 if not saved_write:start+=len(prologue);continue
 end+=len(epilogue);outcomes=[];err=None
 for seed in (17,81):
  rng=random.Random(seed);before={name:rng.getrandbits(64) for name in GPRS};before['rsp']=0x100ff000
  for name,v in before.items():u.reg_write(R[name],v)
  u.reg_write(R['eflags'],0x202)
  try:u.emu_start(BASE+start,BASE+end,count=50000)
  except UcError as e:err=f'{e} at {u.reg_read(R["rip"]):#x}';break
  assert u.reg_read(R['rip'])==BASE+end
  changed={name:u.reg_read(R[name]) for name in GPRS if u.reg_read(R[name])!=before[name]}
  outcomes.append(changed)
 record={'start':hex(BASE+start),'end':hex(BASE+end),'writes':[i.op_str for i in saved_write]}
 if err:record['error']=err
 elif outcomes[0]!=outcomes[1]:record['error']='depends on incoming registers';record['outcomes']=outcomes
 else:
  record['constant_outputs']={k:hex(v) for k,v in outcomes[0].items()};code=b''
  for name,value in outcomes[0].items():
   idx=GPRS.index(name)
   if idx<8:code+=bytes([0x48,0xb8+idx])+struct.pack('<Q',value)
   else:code+=bytes([0x49,0xb8+idx-8])+struct.pack('<Q',value)
  code+=b'\xe9'+struct.pack('<i',end-start-len(code)-5)
  assert len(code)<=end-start;out[start:end]=code+b'\x90'*(end-start-len(code))
 results.append(record);start+=len(prologue)
Path(a.output).write_bytes(out);Path(a.output+'.json').write_text(json.dumps({'environment':{'pid':a.pid,'gs_base':'0x7ff00000','peb':'0x7ff01000','imagebase':hex(BASE),'ldr':'0x7ff02000','heap':'0x30000000','shared_userdata_fields':0},'thunks':results},indent=2))
print(json.dumps(results,indent=2));print('Patched',sum('constant_outputs'in x for x in results),'/',len(results),'->',a.output)
