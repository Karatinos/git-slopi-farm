from unicorn import Uc,UC_ARCH_X86,UC_MODE_64,UC_HOOK_CODE
from driver_analysis_hv import *
u=Uc(UC_ARCH_X86,UC_MODE_64);u.mem_map(0x100000,0x2000)
h=Hypervisor();u.hook_add(UC_HOOK_CODE,h.hook_code)
# Install a dword XOR for R10; low32 zero-extends, flags reflect32bits.
value=0x12345678
_,status=h.call(0x3203,value,0x2b0a,16,next_rip=0x100000)
assert status==0
u.reg_write(R['r10'],0xffffffff88888888);u.reg_write(R['eflags'],0x202)
u.mem_write(0x100010,b'\x0f\x01\xd9\x90')
u.emu_start(0x100010,0x100013)
assert u.reg_read(R['r10'])==(0x88888888^value)
assert u.reg_read(R['eflags']) & 0x80
# ARM temporary context API.
tok,_=h.call(0x3100)
for ins in injection(0x3202,0x123456789abcdef0,0x400)[0]:h.call(0x3101,ins,tok)
assert h.call(0x3103,0,tok)==(0,0)
assert h.call(0x3104,0,tok)==(0x123456789abcdef0,0)
# Trap registration and redirection.
source=0x100100;target=0x100200
encoded=(rol(target,17)+source*0x9e3779b97f4a7c15)&MASK
assert h.call(0x3301,source,encoded,0,1)==(0,0)
u.mem_write(source,b'\x0f\x0b\x90');u.mem_write(target,b'\x90')
u.emu_start(source,target+1)
assert u.reg_read(R['rip'])==target+1
# Custom CPUIDsource exact formula.
u.reg_write(R['rax'],0x4ffffffd);u.reg_write(R['rcx'],123)
u.mem_write(0x100300,b'\x0f\xa2');u.emu_start(0x100300,0x100302)
assert u.reg_read(R['rbx'])==mix32(123^0x9c3017a5)^0x43453032^0x73d45bc1
print('Hypercall registration, ARM override, flags, context session, trap transfer, CPUID tested')
