from pathlib import Path
s=Path('cc2_concrete.py').read_text()
s=s.replace("t=time.time();", """tables=json.loads(Path('lut_catalog.json').read_text());ops=[];stage=0
original_hook=hook
def newhook(u,pc,size,data):
 global stage
 if 0x140698a19<=pc<0x140698edb and bytes(u.mem_read(pc,1))==b'\\xe8':stage+=1
 original_hook(u,pc,size,data)
def read(u,ac,addr,size,value,data):
 if size==1:
  for d in tables:
   start=int(d['data'],16)
   if start<=addr<start+65536:
    x,y=divmod(addr-start,256);ops.append([stage,d['operation'][0],x,y,u.mem_read(addr,1)[0],hex(u.reg_read(UC_X86_REG_RIP))]);return
 elif size==4 and 0x1410d8600<=addr<0x141158600:
  ops.append([stage,'add',0,0,(addr-0x1410d8600)//4,hex(u.reg_read(UC_X86_REG_RIP))])
u.hook_add(unicorn.UC_HOOK_CODE,newhook)
u.hook_add(unicorn.UC_HOOK_MEM_READ,read)
t=time.time();""")
s=s.replace("u.hook_add(unicorn.UC_HOOK_CODE,hook)", "# Hook added below")
s=s.replace("'cc2_native_workspace.bin'", "'cc3_trace_workspace.bin'").replace("'cc2_native_state.bin'", "'cc3_trace_state.bin'")
s += "\nPath('cc3_lut_trace.json').write_text(json.dumps(ops))\n"
exec(compile(s,'cc2_concrete.py','exec'))
