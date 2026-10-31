from pathlib import Path
import struct
M=(1<<32)-1
def H(a,b):
 x=a^b^0x9e3779b9;x=((x<<13)|(x>>19))&M;x=x*0x85ebca6b&M;x^=x>>15;x=x*0xc2b2ae35&M;return x^(x>>16)
raw=Path('unpack_resolved.bin').read_bytes();natural=Path('unpack_memory.bin').read_bytes();out=bytearray(raw)
records=[struct.unpack_from('<III',raw,0x1671008+12*i) for i in range(0xedfa)]
rva,previous_cipher,kind=records[0];plain0=struct.unpack_from('<I',natural,rva)[0];mask=previous_cipher^plain0;print('FIRST',hex(rva),hex(previous_cipher),hex(plain0),hex(mask))
struct.pack_into('<I',out,rva,plain0)
matched=0;diff=[]
for i,(rva,cipher,kind) in enumerate(records[1:],1):
 key=[0xa29a6108,0x7580794a][i&1];state=H(mask,previous_cipher^key^0xaf201288);mask=H(state^key,i);plain=cipher^mask
 # All metadata records patch four-byte fields.
 if kind:plain=struct.unpack_from('<I',natural,rva)[0]
 struct.pack_into('<I',out,rva,plain)
 old=struct.unpack_from('<I',raw,rva)[0];nat=struct.unpack_from('<I',natural,rva)[0]
 if old!=nat:
  if plain==nat:matched+=1
  else:diff.append((i,hex(rva),hex(nat),hex(plain)))
 previous_cipher=cipher
print('Matched',matched,'naturalmodifiedrecords; mismatches',len(diff),diff[:6])
assert not diff
Path('unpack_final.bin').write_bytes(out)
