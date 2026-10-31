"""Re-run the native checker after freshly registering its hidden reads.

Windows APIs and the challenge hypervisor are emulated. --full additionally
enters the public checker prologue; its Windows exception/timing probe is
stubbed, but no flag computation or flag comparison is bypassed.
"""
from pathlib import Path
import argparse,gzip,json,pickle,struct,time
import unicorn as uc
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor

P=argparse.ArgumentParser()
P.add_argument('--full',action='store_true')
P.add_argument('--image',default='check_clean.bin')
args=P.parse_args()
image=Path(args.image).read_bytes()
saved=pickle.load(gzip.open('unpack_initialized_state.pkl.gz'))
base=0x140000000

def run(flag):
    u=uc.Uc(uc.UC_ARCH_X86,uc.UC_MODE_64)
    u.mem_map(base,(len(image)+4095)&~4095);u.mem_write(base,image)
    for addr,size in [(0x10000000,0x1000000),(0x20000000,0x10000),
                      (0x30000000,0x10000000),(0x7ff00000,0x100000),
                      (0x70000000,0x100000)]:u.mem_map(addr,size)
    u.mem_write(0x70000000,b'\xc3'*0x100000)
    for addr,blob in saved['mem']:
        if addr in (0x30000000,0x7ff00000):u.mem_write(addr,blob)
    def put(addr,value):u.mem_write(addr,struct.pack('<Q',value))
    def ret(value=None):
        rsp=u.reg_read(UC_X86_REG_RSP)
        pc=struct.unpack('<Q',u.mem_read(rsp,8))[0]
        u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,pc)
        if value is not None:u.reg_write(UC_X86_REG_RAX,value)
    put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000)
    put(0x7ff00060,0x7ff01000);put(0x14134d552,0x30010000)
    u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000)
    sp=0x10fe0000
    u.reg_write(UC_X86_REG_RSP,sp-8)
    u.reg_write(UC_X86_REG_RBP,sp+0x100)
    u.reg_write(UC_X86_REG_RDI,0x20000000)
    u.mem_write(0x20000000,flag.encode())
    put(sp-8,0x700ffff0 if args.full else 0x140698a19)
    if args.full:
        u.reg_write(UC_X86_REG_RCX,0x20000000)
        u.reg_write(UC_X86_REG_RDX,len(flag))
    hv=Hypervisor(pid=1234)
    result={'input':flag,'mode':'full-prologue' if args.full else 'fresh-readiness'}
    ticks=100000000
    def hook(u,pc,size,_):
        nonlocal ticks
        if pc==0x140698edb:
            result['eax']=u.reg_read(UC_X86_REG_EAX)
            result['comparison_stage_reached']=True
            u.emu_stop();return
        if pc==0x700ffff0:
            result['outer_return']=u.reg_read(UC_X86_REG_RAX)
            u.emu_stop();return
        if args.full and pc==0x140698930:
            result['timing_probe_stubbed']=True;ret(1);return
        if pc==0x140699420:ret();return
        raw=bytes(u.mem_read(pc,min(3,size)))
        if raw[:2]==b'\x0f\x31' or raw==b'\x0f\x01\xf9':
            ticks+=100;u.reg_write(UC_X86_REG_EAX,ticks)
            u.reg_write(UC_X86_REG_EDX,0);u.reg_write(UC_X86_REG_RIP,pc+size);return
        if pc in hv.traps:
            kind,target,source=hv.traps[pc]
            if kind==3 and u.reg_read(UC_X86_REG_R10)==source:u.reg_write(UC_X86_REG_R10,target)
        if pc in saved['apis']:
            name=saved['apis'][pc]
            rcx=u.reg_read(UC_X86_REG_RCX);rdx=u.reg_read(UC_X86_REG_RDX)
            if name=='GetCurrentProcess':v=0xffffffffffffffff
            elif name in ('GetCurrentProcessId','GetCurrentThreadId'):v=1234
            elif name=='IsDebuggerPresent':v=0
            elif name=='CheckRemoteDebuggerPresent':u.mem_write(rdx,b'\0'*4);v=1
            elif name=='NtQueryInformationProcess':
                buf=u.reg_read(UC_X86_REG_R8);sz=u.reg_read(UC_X86_REG_R9)
                u.mem_write(buf,(1 if rdx==31 else 0).to_bytes(sz,'little'));v=0
            elif name=='VirtualQuery':
                u.mem_write(rdx,struct.pack('<QQIIQIIII',rcx&~0xfff,0,0,0,0x200000,0x10000,0,0,0));v=48
            elif name=='VirtualProtect':put(u.reg_read(UC_X86_REG_R9),0x40);v=1
            elif name=='GetSystemTimeAsFileTime':put(rcx,13245678900123456);v=1
            elif name=='QueryPerformanceCounter':put(rcx,ticks);v=1
            elif name=='QueryPerformanceFrequency':put(rcx,1000000);v=1
            elif name=='GetTickCount':v=123456
            elif name=='VirtualFree':v=1
            else:raise RuntimeError('Unmodeled API: '+name)
            ret(v);return
        hv.handle(u,pc,size)
    u.hook_add(uc.UC_HOOK_CODE,hook)
    def intr(u,n,_):
        if not hv.handle_exception(u,n):raise RuntimeError(('Unhandled interrupt',n,hex(u.reg_read(UC_X86_REG_RIP))))
    u.hook_add(uc.UC_HOOK_INTR,intr)
    def cpuid(u,_):
        leaf=u.reg_read(UC_X86_REG_EAX)
        values={0:(13,0x756e6547,0x6c65746e,0x49656e69),
                1:(0x306a9,0x10800,0xfffafbff,0xbfebfbff),
                0x80000000:(0x80000008,0,0,0),0x80000001:(0,0,0x121,0x2c100800),
                0x80000008:(0x3028,0,0,0)}.get(leaf,(0,0,0,0))
        for reg,v in zip((UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX),values):u.reg_write(reg,v)
        return True
    u.hook_add(uc.UC_HOOK_INSN,cpuid,None,1,0,UC_X86_INS_CPUID)
    start=time.time()
    try:u.emu_start(0x140698990 if args.full else 0x1406987c0,0,count=5000000)
    except Exception as e:result['error']=str(e)
    result.update(seconds=time.time()-start,pc=hex(u.reg_read(UC_X86_REG_RIP)),registered_reads=sum(v[0]==3 for v in hv.traps.values()))
    return result

flag=Path('cc3_candidate.txt').read_text().strip()
tests=[flag,flag[:7]+'A'+flag[8:],flag[:25]+'s'+flag[26:]]
results=[]
for value in tests:
    r=run(value);results.append(r);print(json.dumps(r),flush=True)
    if 'error' in r:break
output='cc3_verify_full.json' if args.full else 'cc3_verify_native.json'
Path(output).write_text(json.dumps(results,indent=2)+'\n')
if len(results)==3:
    assert [r.get('eax') for r in results]==[1,0,0],results
    assert all(r['registered_reads']==11 for r in results),results
