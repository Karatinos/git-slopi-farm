"""Semantics recovered from cybercup.sys RVA 0x1260 / 0x29c0."""
MASK=(1<<64)-1
GPRS=['rax','rcx','rdx','rbx','rsp','rbp','rsi','rdi','r8','r9','r10','r11','r12','r13','r14','r15']
def signed(x,n):
 x&=(1<<n)-1
 return x-(1<<n) if x>>(n-1) else x

def arm(code, regs=None):
 """Return (status, registers, NZCV), mirroring driver. Status0 is success."""
 r=list(regs or [0]*32);r += [0]*(32-len(r));n=z=c=v=0;pc=0;steps=0
 get=lambda i:0 if i==31 else r[i]
 if not 1<=len(code)<=64:return 1,r,(n,z,c,v)
 while pc<len(code):
  if steps==256:return 2,r,(n,z,c,v)
  steps+=1;ins=code[pc];rd=ins&31;rn=(ins>>5)&31;rm=(ins>>16)&31;npc=pc+1
  if (((ins&0xff800000)+0x2d800000)&0xdfffffff)==0:
   shift=((ins>>21)&3)*16;value=((ins>>5)&65535)<<shift
   if ins&(1<<29): value=(get(rd)&~(65535<<shift))|value
   if rd!=31:r[rd]=value
  elif (((ins&0xffe0fc00)+0x76000000)&0x9fffffff)==0 and (ins&0xffe0fc00)!=0xea000000:
   a,b=get(rn),get(rm);value=(a^b) if ins&(1<<30) else ((a|b) if ins&(1<<29) else a&b)
   if rd!=31:r[rd]=value
  elif (ins&0xffe0fc1f)==0xeb00001f or (ins&0xffc0001f)==0xf100001f:
   a=get(rn);b=((ins>>10)&0xfff) if (ins&0xffc0001f)==0xf100001f else get(rm)
   d=(a-b)&MASK;n=d>>63;z=int(d==0);c=int(a>=b);v=((a>>63)^(b>>63))&((a>>63)^n)
  elif (ins&0xfc000000)==0x14000000:npc=pc+signed(ins,26)
  elif (ins&0xff000010)==0x54000000:
   cond=ins&15
   if cond>=14:return 1,r,(n,z,c,v)
   yes=[z,not z,c,not c,n,not n,v,not v,c and not z,not c or z,n==v,n!=v,not z and n==v,z or n!=v][cond]
   if yes:npc=pc+signed(ins>>5,19)
  else:return 1,r,(n,z,c,v)
  if npc<0 or npc>len(code):return 3,r,(n,z,c,v)
  pc=npc
 r[31]=(steps<<32)|pc
 return 0,r,(n,z,c,v)

def injection(op,value,descriptor):
 """Generate an override exactly as 0x3201/2/3 do; return code, outputmask, flags."""
 dst=descriptor&15;width=(descriptor>>8)&7;flags=(descriptor>>11)&1;logical=(descriptor>>12)&3
 assert 1<=width<=4 and descriptor&~0x3f0f==0
 if op==0x3201:
  assert value<=0xffffffff and logical==0
  code=[value]
 else:
  assert op in [0x3202,0x3203]
  assert (op==0x3202 and flags==0 and logical==0) or (op==0x3203 and flags==1 and logical<3)
  reg=dst if op==0x3202 else 16
  code=[(0xd2800000 if i==0 else 0xf2800000)|(i<<21)|(((value>>(16*i))&65535)<<5)|reg for i in range(4)]
  if op==0x3203:code += [[0x8a000000,0xaa000000,0xca000000][logical]|(16<<16)|(dst<<5)|dst]
 return code,width<<(3*dst),flags
