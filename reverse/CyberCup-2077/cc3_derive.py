from pathlib import Path
import z3 as z,json,random
cs=list(z.parse_smt2_file('unpack_reduced.smt2'));keys=[1,16,32,55,71,86,103,122]
vals=[]
for sample in [bytes(8),bytes(range(8)),b'ctfcup{A',b'ctfcup{d',bytes([255]*8)]:
 subs=[(z.BitVec(f'input_word_{j:02}',32),z.BitVecVal(int.from_bytes(sample[j*4:j*4+4],'little'),32)) for j in range(2)];out={}
 for c in cs:
  if not z.is_eq(c):continue
  lhs,rhs=c.children()
  if not (z.is_const(lhs) and lhs.decl().kind()==z.Z3_OP_UNINTERPRETED):lhs,rhs=rhs,lhs
  if str(lhs).startswith('lut_') and int(str(lhs)[4:])>=136:break
  v=z.simplify(z.substitute(rhs,*subs));assert z.is_bv_value(v),(lhs,v)
  subs.append((lhs,v));out[str(lhs)]=v.as_long()
 kv=[out[f'lut_{j:05}'] for j in keys];masks=[a^b for a,b in zip(sample,kv)];print(sample,kv,'masks',masks,flush=True);vals.append(masks)
assert all(x==vals[0] for x in vals)
M=0xffffffff
rol=lambda x,n:((x<<n)|(x>>(32-n)))&M
masks=vals[0]
def transform(s):
 a=0x8d60e266;b=0xa23f2146
 for i,c in enumerate(s):
  k=(c^masks[i])+257+65*i
  a=rol(((a^k)+b)&M,5+i%7)
  b=a^rol((b+(a^k))&M,11+i%5)
 return a,b
for s in [b'ctfcup{A',b'ctfcup{d']:print(s,[hex(x) for x in transform(s)])
Path('cc3_first_model.json').write_text(json.dumps({'masks':masks,'a':0x8d60e266,'b':0xa23f2146}))
