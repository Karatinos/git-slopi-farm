from pathlib import Path
import sys,pickle
sys.argv=['driver_analysis_trace.py','unpack_last_state.pkl.gz']
source=Path('unpack_emu.py').read_text().split('start=time.time()')[0]
exec(compile(source,'unpack_emu.py','exec'))
trace=[];patches=[];active=False
regs=[UC_X86_REG_RAX,UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_RBX,UC_X86_REG_RSP,UC_X86_REG_RBP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15,UC_X86_REG_EFLAGS]
def record(u,a,sz,d):
 if active:trace.append([a,bytes(u.mem_read(a,sz)),[u.reg_read(r) for r in regs],[]])
def memory(u,access,a,sz,val,d):
 global active
 if active and trace:
  trace[-1][3].append((access,a,sz,val if access==unicorn.UC_MEM_WRITE else int.from_bytes(u.mem_read(a,sz),'little')))
 if access==unicorn.UC_MEM_WRITE and 0x140001000<=a<0x141671000:
  patches.append((a,sz,val,[u.reg_read(r) for r in regs]))
  if active:u.emu_stop()
  else:active=True
U.hook_add(unicorn.UC_HOOK_CODE,record)
U.hook_add(unicorn.UC_HOOK_MEM_READ|unicorn.UC_HOOK_MEM_WRITE,memory)
U.emu_start(entry,0,count=2000000)
pickle.dump((trace,patches),open('driver_analysis_trace.pkl','wb'))
print('TRACE',len(trace),'patches',[(hex(a),sz,hex(v)) for a,sz,v,r in patches])
