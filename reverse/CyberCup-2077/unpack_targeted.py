import pefile,unicorn,capstone,struct,sys,time,collections,pickle,gzip,lzma,os
from unicorn.x86_const import *
P=pefile.PE('cybercup.exe'); U=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
base=P.OPTIONAL_HEADER.ImageBase;size=(P.OPTIONAL_HEADER.SizeOfImage+0xfff)&~0xfff
U.mem_map(base,size); U.mem_write(base,P.get_memory_mapped_image())
U.mem_map(0x10000000,0x1000000);U.reg_write(UC_X86_REG_RSP,0x10ff0000)
U.mem_map(0x70000000,0x1000000);U.mem_write(0x70000000,b'\xc3'*0x1000000)
U.mem_map(0x7ff00000,0x100000);U.reg_write(UC_X86_REG_GS_BASE,0x7ff00000)

def put(a,v):U.mem_write(a,struct.pack('<Q',v))
def get(a):return struct.unpack('<Q',U.mem_read(a,8))[0]
put(0x7ff00060,0x7ff01000);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000);U.mem_write(0x7ff01118,struct.pack('<III',10,0,19041))
put(0x7ff00008,0x11000000);put(0x7ff00010,0x10000000)
U.mem_map(0x30000000,0x10000000); heap=0x30010000
apis={};reverse={}; jumped=False;last_vp=None
def apiptr(s):
 if s not in reverse:
  ptr=0x70000000+len(apis)*0x10;apis[ptr]=s;reverse[s]=ptr
 return reverse[s]
for dll in P.DIRECTORY_ENTRY_IMPORT:
 for i in dll.imports:
  s=(i.name or str(i.ordinal).encode()).decode();put(i.address,apiptr(s))
def cstr(a,wide=False):
 if not a:return ''
 d=bytes(U.mem_read(a,512));return d.decode('utf-16le',errors='ignore').split('\0')[0] if wide else d.split(b'\0')[0].decode(errors='replace')
def api(u,a,s,d):
 global heap,jumped,last_vp
 n=apis.get(a,'unknown');rcx,rdx,r8,r9=[u.reg_read(r) for r in [UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9]]
 if a==0x14246778f:
  data=bytes(U.mem_read(rdx,256));name=[]
  for i,v in enumerate(data):
   shift=i%32;k=((0x17a206fd<<shift)|(0x17a206fd>>(32-shift)))&0xffffffff
   b=v^((k+i)&255) if r8&255 else v
   if b==0:break
   name.append(b)
  n=bytes(name).decode(errors='replace');print('RESOLVE',n,hex(rdx),hex(r8),flush=True)
  rsp=u.reg_read(UC_X86_REG_RSP);u.reg_write(UC_X86_REG_RAX,0 if n=='wine_get_version' else apiptr(n));u.reg_write(UC_X86_REG_RIP,get(rsp));u.reg_write(UC_X86_REG_RSP,rsp+8);return
 if n!='VirtualProtect':print('API',n,*map(hex,[rcx,rdx,r8,r9]),flush=True)

 val=1
 if n in ['LocalFree','HeapFree','VirtualFree']:val=0
 elif n=='GetProcessHeap':val=0x30000000
 elif n in ['LocalAlloc','HeapAlloc','VirtualAlloc']:
  size=rdx if n!='HeapAlloc' else r8;val=heap;heap+=(size+0xfff)&~0xfff
 elif n in ['LoadLibraryA','GetModuleHandleA','GetModuleHandleW']:
  print('DLL',cstr(rcx,n.endswith('W')),flush=True);val=0x60000000
 elif n=='GetProcAddress':
  name=cstr(rdx);print('PROC',name,flush=True);val=apiptr(name)
 elif n=='VirtualProtect':
  if not jumped and last_vp==rcx:
   current=u.reg_read(UC_X86_REG_R14)
   if 100<current<60627:
    rsp=u.reg_read(UC_X86_REG_RSP);data=bytearray(u.mem_read(rsp,0x10ff0000-rsp));old=struct.pack('<Q',current);new=struct.pack('<Q',60627);hits=[]
    for off in range(0,len(data)-8,8):
     if data[off:off+8]==old:data[off:off+8]=new;hits.append(hex(rsp+off))
    u.mem_write(rsp,bytes(data));u.reg_write(UC_X86_REG_R14,60627);jumped=True;print('JUMP',current,'->60627',hits,flush=True)
  last_vp=rcx
  if r9:U.mem_write(r9,struct.pack('<I',0x40))
 elif n=='GetModuleFileNameW':
  st='C:\\cybercup.exe\0'.encode('utf-16le');U.mem_write(rdx,st);val=len(st)//2-1
 elif n=='GetProcessAffinityMask':put(rdx,1);put(r8,1)
 elif n in ['GetCurrentProcessId','GetCurrentThreadId']:val=1234
 elif n=='GetCurrentProcess':val=0xffffffffffffffff
 elif n in ['IsDebuggerPresent','CheckRemoteDebuggerPresent']:val=0
 elif n=='ExitProcess':u.emu_stop();return
 elif n in ['memcpy','memmove']:
  U.mem_write(rcx,bytes(U.mem_read(rdx,r8)));val=rcx
 elif n=='memset':U.mem_write(rcx,bytes([rdx&255])*r8);val=rcx
 else:
  print('UNKNOWN API',n,flush=True);u.emu_stop();return
 rsp=u.reg_read(UC_X86_REG_RSP);u.reg_write(UC_X86_REG_RAX,val);u.reg_write(UC_X86_REG_RIP,get(rsp));u.reg_write(UC_X86_REG_RSP,rsp+8)
U.hook_add(unicorn.UC_HOOK_CODE,api,begin=0x70000000,end=0x70ffffff)
U.hook_add(unicorn.UC_HOOK_CODE,api,begin=0x14246778f,end=0x14246778f)
last=collections.deque(maxlen=20)
decomp_seen=False
def checkpoint(path):
 with gzip.open(path+'.tmp','wb',compresslevel=1) as f:pickle.dump(dict(ctx=U.context_save(),mem=[(base,bytes(U.mem_read(base,size))),(0x10000000,bytes(U.mem_read(0x10000000,0x1000000))),(0x30000000,bytes(U.mem_read(0x30000000,heap-0x30000000))),(0x7ff00000,bytes(U.mem_read(0x7ff00000,0x100000)))],apis=apis,reverse=reverse,heap=heap),f)
 os.replace(path+'.tmp',path)
def block(u,a,s,d):
 global decomp_seen
 last.append(a)
 if not decomp_seen and 0x142466000<=a<0x142467700:
  decomp_seen=True;print('DECOMP ENTRY',hex(a),flush=True)
  for n in ['RAX','RBX','RCX','RDX','RSI','RDI','RBP','RSP','R8','R9','R10','R11','R12','R13','R14','R15']:print(n,hex(u.reg_read(globals()['UC_X86_REG_'+n])),flush=True)
  checkpoint('unpack_decomp_state.pkl.gz');u.emu_stop()

block_handle=U.hook_add(unicorn.UC_HOOK_BLOCK,block)
def invalid(u,access,a,s,v,d):print('INVALID',access,hex(a),s,hex(v),flush=True);return False
U.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
def fastcrc(u,a,s,d):
 n=u.reg_read(UC_X86_REG_RDI); ptr=u.reg_read(UC_X86_REG_R9);tab=u.reg_read(UC_X86_REG_R11); c=u.reg_read(UC_X86_REG_ECX)
 print('CRC',hex(ptr),hex(n),flush=True)
 table=struct.unpack('<256I',u.mem_read(tab,1024))
 for b in u.mem_read(ptr,n):c=((c>>8)^table[(b^c)&255]^0x20791431)&0xffffffff
 u.reg_write(UC_X86_REG_R9,ptr+n);u.reg_write(UC_X86_REG_RDI,0);u.reg_write(UC_X86_REG_ECX,c);u.reg_write(UC_X86_REG_RIP,0x142595958)
U.hook_add(unicorn.UC_HOOK_CODE,fastcrc,begin=0x1424c0fdd,end=0x1424c0fdd)
def fastlzma(u,a,s,d):
 rsp=u.reg_read(UC_X86_REG_RSP); props=u.reg_read(UC_X86_REG_RCX);src=u.reg_read(UC_X86_REG_RDX);consumedptr=u.reg_read(UC_X86_REG_R9)
 lc,lp,pb=struct.unpack('<III',u.mem_read(props,12));dest=get(rsp+0x28);lenptr=get(rsp+0x38)
 data=bytes(u.mem_read(src,base+size-src));de=lzma.LZMADecompressor(format=lzma.FORMAT_RAW,filters=[dict(id=lzma.FILTER_LZMA1,dict_size=1<<26,lc=lc,lp=lp,pb=pb)])
 out=de.decompress(data);assert de.eof;used=len(data)-len(de.unused_data)
 print('LZMA',hex(src),'->',hex(dest),'used',hex(used),'out',hex(len(out)),flush=True)
 u.mem_write(dest,out);put(consumedptr,used);put(lenptr,len(out));u.reg_write(UC_X86_REG_RAX,0);u.reg_write(UC_X86_REG_RIP,get(rsp));u.reg_write(UC_X86_REG_RSP,rsp+8)
U.hook_add(unicorn.UC_HOOK_CODE,fastlzma,begin=0x1424661cb,end=0x1424661cb)
U.reg_write(UC_X86_REG_RCX,base);U.reg_write(UC_X86_REG_RDX,1);U.reg_write(UC_X86_REG_R8,0)
def cpuid(u,d):
 leaf=u.reg_read(UC_X86_REG_EAX);sub=u.reg_read(UC_X86_REG_ECX);vals=[0,0,0,0]
 if leaf==0x4ffffffd:
  x=sub^0x9c3017a5;x^=x>>16;x=x*0x7feb352d&0xffffffff;x^=x>>15;x=x*0x846ca68b&0xffffffff;x^=x>>16
  vals=[leaf,x^0x43453032^0x73d45bc1,0x41434631,0]
 elif leaf==0x4fffffff:
  vals=[leaf,0x706d6953,0x7653656c,0x2020206d]
  if sub==1:vals=[leaf,0,0,0x20000]
  elif sub==2:vals=[leaf,0,0,0]
  elif sub==3:vals=[leaf,1,1,0]
  elif sub==4:vals=[leaf,0x43453032,0x4241434b,0x414c4953]
 elif leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
 elif leaf==1:vals=[0x306a9,0x00010800,0x7ffafbff,0xbfebfbff]
 elif leaf==0x80000000:vals=[0x80000008,0,0,0]
 elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
 elif leaf==0x80000008:vals=[0x3028,0,0,0]
 elif leaf in [0x80000002,0x80000003,0x80000004]:vals=list(struct.unpack('<4I',b'Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz          '.ljust(48,b' ')[(leaf-0x80000002)*16:(leaf-0x80000001)*16]))
 print('CPUID',hex(leaf),hex(sub),flush=True)
 for reg,val in zip([UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX],vals):u.reg_write(reg,val)
 return True
U.hook_add(unicorn.UC_HOOK_INSN,cpuid,None,1,0,UC_X86_INS_CPUID)
tsc=100000000
def rdtsc(u,a,s,d):
 global tsc
 tsc+=100;u.reg_write(UC_X86_REG_EAX,tsc&0xffffffff);u.reg_write(UC_X86_REG_EDX,tsc>>32);u.reg_write(UC_X86_REG_RIP,a+2)
for va in [0x142468951,0x142468969]:U.hook_add(unicorn.UC_HOOK_CODE,rdtsc,begin=va,end=va)
entry=0x142419ae5
if len(sys.argv)>1:
 with gzip.open(sys.argv[1],'rb') as f:saved=pickle.load(f)
 for a,b in saved['mem']:U.mem_write(a,b)
 U.context_restore(saved['ctx']);apis=saved['apis'];reverse=saved['reverse'];heap=saved['heap'];entry=U.reg_read(UC_X86_REG_RIP);decomp_seen=True;U.hook_del(block_handle)
patch_count=0
def patchwatch(u,access,a,sz,val,d):
 global patch_count
 patch_count+=1
 if patch_count<=5:print('PATCHREGS',[(n,hex(u.reg_read(globals()['UC_X86_REG_'+n]))) for n in ['RAX','RBX','RCX','RDX','RSI','RDI','RBP','RSP','R8','R9','R10','R11','R12','R13','R14','R15']],flush=True)
 if patch_count<=40 or patch_count%10000==0:print('PATCH',patch_count,hex(a),sz,bytes(u.mem_read(a,sz)).hex(),hex(val),flush=True)
U.hook_add(unicorn.UC_HOOK_MEM_WRITE,patchwatch,begin=0x140001000,end=0x141670fff)
start=time.time()
try:U.emu_start(entry,0,count=100000000,timeout=60000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-start,'RIP',hex(U.reg_read(UC_X86_REG_RIP)), 'BLOCKS',list(map(hex,last)),flush=True)
for r in ['RAX','RBX','RCX','RDX','RSI','RDI','RBP','RSP','R8','R9','R10','R11','R12','R13','R14','R15']:
 print(r,hex(U.reg_read(globals()['UC_X86_REG_'+r])))
open('unpack_targeted.bin','wb').write(U.mem_read(base,size))
checkpoint('unpack_targeted_state.pkl.gz')
