from pathlib import Path
import numpy as np,json,struct
b=Path('unpack_memory.bin').read_bytes();base=0x140000000
x=np.arange(256,dtype=np.uint32)[:,None];y=np.arange(256,dtype=np.uint32)[None,:]
ops={'add':x+y,'sub':x-y,'rsub':y-x,'xor':x^y,'and':x&y,'or':x|y,'mul':x*y,'eq':x==y,'lt':x<y,'gt':x>y,'carry':(x+y)>>8,'borrow':x<y,'shr':x>>np.minimum(y,31),'rshr':y>>np.minimum(x,31),'shl':x<<np.minimum(y,31),'rshl':y<<np.minimum(x,31),'rol':(x<<(y%8))|(x>>((8-y)%8)),'ror':(x>>(y%8))|(x<<((8-y)%8))}
ops.update({f'funnel_left_{n}':(x<<n)|(y>>(8-n)) for n in range(1,8)})
ops={k:(v&255).astype('uint8') for k,v in ops.items()};arr=np.frombuffer(b[:len(b)//8*8],dtype='<u8');candidates=np.flatnonzero((arr[1:]-arr[:-1])==256);out=[];end=0
for i in candidates:
 off=int(i)*8
 if off<end:continue
 ptr=int(arr[i]);r=ptr-base
 if r<0 or r+65536>len(b) or not np.array_equal(arr[i:i+256],ptr+np.arange(256,dtype=np.uint64)*256):continue
 data=np.frombuffer(b[r:r+65536],dtype=np.uint8).reshape(256,256)
 matches=[n for n,v in ops.items() if np.array_equal(data,v)]
 out.append(dict(global_address=hex(base+off-8),rows=hex(base+off),data=hex(ptr),operation=matches or 'unknown'))
 end=off+2048
print(json.dumps(out,indent=2));Path('lut_catalog.json').write_text(json.dumps(out,indent=2))
