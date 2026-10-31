from pathlib import Path
import struct
b=Path(__file__).with_name('unpack_memory.bin').read_bytes();d={struct.unpack_from('<I',b,0x1671008+12*i)[0]:(i,struct.unpack_from('<III',b,0x1671008+12*i)[1]) for i in range(60922)}
M=0xffffffff
pairs=[(0x1615620,0x4fffffff),(0x1615629,0x4fffffff),(0x1615635,0x706d6953),(0x160fefa,0x3301)]
def ux(x,n):
 for k in range(n,32,n): x^=(x>>k) if k==n else 0
 # use successive doubling
 return x

def undo_xor(x,n):
 y=x
 for j in range(n,32,n): y^=x>>j
 return y

def invmix(x,kind):
 if kind==0: a,c,s1,s2,s3=0x7feb352d,0x846ca68b,16,15,16
 else:a,c,s1,s2,s3=0x85ebca6b,0xc2b2ae35,16,13,16
 x=undo_xor(x,s3);x=x*pow(c,-1,1<<32)&M;x=undo_xor(x,s2);x=x*pow(a,-1,1<<32)&M;return undo_xor(x,s1)
for kind in range(2):
 for combine in ['xor','sub','add']:
  for src in ['rva','idx','idx12','obs']:
   ks=[]
   for r,p in pairs:
    i,c=d[r];o=struct.unpack_from('<I',b,r)[0];z=c^p if combine=='xor' else ((c-p)&M if combine=='sub' else (p-c)&M);v=invmix(z,kind);q={'rva':r,'idx':i,'idx12':i*12,'obs':o}[src];ks.append(v^q)
   print(kind,combine,src,[hex(x) for x in ks])
