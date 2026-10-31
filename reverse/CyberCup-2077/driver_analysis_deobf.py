"""Remove inert hypervisor guards; replace simple ARM overrides with x86.
Works on mapped PE image snapshots with base 0x140000000. Writes separate file.
"""
from pathlib import Path
import struct,json,argparse
from capstone import *
from capstone.x86 import *
from driver_analysis_arm import injection
p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--output',default='driver_analysis_deobf.bin');a=p.parse_args()
BASE=0x140000000;b=bytearray(Path(a.input).read_bytes());orig=bytes(b);patches=[]
md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True

def replace(start,end,code,desc):
 if len(code)+5>end-start:raise ValueError('replacement too large')
 code+=b'\xe9'+struct.pack('<i',end-start-len(code)-5)
 b[start:end]=code+b'\x90'*(end-start-len(code));patches.append({'start':hex(BASE+start),'end':hex(BASE+end),'description':desc})

prologue=bytes.fromhex('9c505351524150415141524153')
epilogue=bytes.fromhex('415b415a415941585a595b589d')
start=0;counts={'guards':0,'overrides':0}
while True:
 start=orig.find(prologue,start)
 if start<0:break
 ins=list(md.disasm(orig[start:start+100],BASE+start));branch=next((x for x in ins if x.mnemonic=='jne'),None)
 if branch and branch.operands[0].type==X86_OP_IMM:
  end=branch.operands[0].imm-BASE
  if 0<=end<len(orig) and orig[end:end+len(epilogue)]==epilogue:
   target=end+len(epilogue);b[start:start+5]=b'\xe9'+struct.pack('<i',target-start-5)
   patches.append({'start':hex(BASE+start),'end':hex(BASE+target),'description':'skip inert register-preserving CPUID/capability guard'});counts['guards']+=1
 start+=len(prologue)

prologue=bytes.fromhex('9c5051524150415141524153')
epilogue=bytes.fromhex('415b415a415941585a59589d0f01d9')
start=0
while True:
 start=orig.find(prologue,start)
 if start<0:break
 ins=list(md.disasm(orig[start:start+200],BASE+start));vals={};call=None
 for x in ins:
  if x.mnemonic=='vmmcall':call=x.address-BASE;break
  if x.mnemonic in ('mov','movabs') and len(x.operands)==2 and x.operands[0].type==X86_OP_REG and x.operands[1].type==X86_OP_IMM:vals[x.reg_name(x.operands[0].reg)]=x.operands[1].imm
 if call and vals.get('edx') in (0x3201,0x3202,0x3203) and vals.get('r10d')==12 and orig[call+3:call+3+len(epilogue)]==epilogue:
  op=vals['edx'];value=vals.get('r8',vals.get('r8d'));desc=vals['r9d'];width=(desc>>8)&7;dst=desc&15;flags=(desc>>11)&1
  code=None;desc_text=''
  if op==0x3202 and width==3:
   code=(b'\x41' if dst>=8 else b'')+bytes([0xb8+(dst&7)])+struct.pack('<I',value&0xffffffff);desc_text=f'mov dwordGPR{dst}, {value&0xffffffff:#x}'
  elif op==0x3201 and width==3:
   rd=value&31;rn=(value>>5)&31;rm=(value>>16)&31;kind=value&0xffe0fc00
   assert rd==dst
   if rn==31 and kind==0xaa000000 and rm<16:
    rex=0x40|(4 if rm>=8 else 0)|(1 if dst>=8 else 0)
    code=(bytes([rex]) if rex!=0x40 else b'')+bytes([0x89,0xc0|((rm&7)<<3)|(dst&7)]);desc_text=f'mov dwordGPR{dst}, dwordGPR{rm}'
   elif rn==dst and rm<16 and (flags or dst!=4) and kind in (0x8a000000,0xaa000000,0xca000000):
    opcode={0x8a000000:0x21,0xaa000000:0x09,0xca000000:0x31}[kind]
    rex=0x40|(4 if rm>=8 else 0)|(1 if dst>=8 else 0)
    code=(bytes([rex]) if rex!=0x40 else b'')+bytes([opcode,0xc0|((rm&7)<<3)|(dst&7)])
    if not flags:code=b'\x9c'+code+b'\x9d'
    desc_text=f'logical{kind:#x} dwordGPR{dst}, dwordGPR{rm}'
  elif op==0x3203 and width==3 and (flags or dst!=4):
   kind=(desc>>12)&3
   if kind<3:
    subop={0:4,1:1,2:6}[kind]
    code=(b'\x41' if dst>=8 else b'')+bytes([0x81,0xc0|(subop<<3)|(dst&7)])+struct.pack('<I',value&0xffffffff)
    if not flags:code=b'\x9c'+code+b'\x9d'
    desc_text=f'logical immediate {kind} dwordGPR{dst}, {value&0xffffffff:#x}'
  if code is not None:
   replace(start,call+3+len(epilogue),code,desc_text);counts['overrides']+=1
 start+=len(prologue)
Path(a.output).write_bytes(b);Path(a.output+'.json').write_text(json.dumps(patches,indent=2));print(counts,'->',a.output)
