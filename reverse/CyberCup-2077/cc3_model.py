"""Compact block transforms, derived from actual LUT reads in the checker."""
from pathlib import Path
import json, struct

MASK = 0xffffffff
GROUPS = [(1,5),(8,11),(14,17),(20,23),(26,30),(33,36),(39,42),(45,48),(51,55)]

def rol(x, n):
    x &= MASK
    return ((x << n) | (x >> (32-n))) & MASK

def ror(x, n):
    return rol(x, 32-n)

def pack(values):
    return sum(v << (8*i) for i,v in enumerate(values))

def derive():
    ops=json.loads(Path('cc3_lut_trace.json').read_text())
    inputs=b'ctfcup{'+b'A'*59+b'}'
    params=[]
    for j,(lo,hi) in enumerate(GROUPS):
        t=[o for o in ops if lo<=o[0]<=hi]
        start=max(i for i,o in enumerate(t) if o[1]=='and')+1
        word=lambda at, column:pack([o[column] for o in t[at:at+4]])
        add=lambda at:(t[at][4]&65535)|((t[at+3][4]&65535)<<16)
        k=add(start)
        kind=j%4
        if kind in (0,1):
            a=word(start+4,2)
            b=(add(start+8)-(a^k))&MASK
        elif kind==2:
            a=word(start+8,2)
            b=(add(start+4)-k)&MASK
        else:
            a=(add(start+4)-k)&MASK
            b=word(start+12,3)
        p={'block':j,'kind':kind,'a':a,'b':b,'masks':[],'p':[],'q':[]}
        for i in range(3 if j==8 else 8):
            offset=36+40*i
            s=t[offset+8][4]
            p['masks'].append(s^inputs[8*j+i])
            p['p'].append((add(offset+12)-s)&255)
            p['q'].append(t[offset+24][3])
        if j==8:
            keys=[]
            offset=start
            for i in range(8):
                keys.append(add(offset))
                offset+=24+4*((5+i%7)%8!=0)+4*((11+i%5)%8!=0)
            assert offset==len(t)
            p['padding_keys']=keys[3:]
        params.append(p)
    Path('cc3_params.json').write_text(json.dumps(params,indent=2)+'\n')
    return params

def preprocess(p, data):
    ss=[c^m for c,m in zip(data,p['masks'])]
    qq=[(s^((s+offset)&255)^q)&255 for s,offset,q in zip(ss,p['p'],p['q'])]
    rr=[(c+q)&255 for c,q in zip(data,qq)]
    return ss,qq,rr

def transform(p, data):
    ss,qq,rr=preprocess(p,data)
    kind=p['kind']
    keys=[(((s+p['p'][i])&255) if (kind==2 and i%2==1) or (kind==3 and i%2==0) else s)+257+65*i for i,s in enumerate(ss)]
    keys+=p.get('padding_keys',[])
    a,b=p['a'],p['b']
    if kind in (0,1):
        for i,k in enumerate(keys[:6] if kind==1 else keys):
            a=rol((a^k)+b,(7+i) if kind==1 else (5+i%7))
            b=a^rol(b+(a^k),(11+i) if kind==1 else (11+i%5))
    elif kind==2:
        for i,k in enumerate(keys[:4]):a=rol(a^((b+k)&MASK),5+i)
        for i,k in enumerate(keys[4:],4):b=rol(b+k,13+i%7)^a
    else:
        for i,k in enumerate(keys[:4]):a=rol(a+k,9+i)^(b^k)
        for i,k in enumerate(keys[4:],4):b=(rol(b^k,11+i%5)+(a^k))&MASK
    if kind==1:a,b=b,a
    if kind:
        a^=pack(rr[4:8])
        b^=pack(qq[:4])
    return a,b

if __name__=='__main__':
    params=derive()
    tests=[(b'ctfcup{'+b'A'*59+b'}','cc3_trace_state.bin'),
           (Path('cc3_sample2_input.txt').read_bytes(),'cc3_sample2_state.bin')]
    for data,path in tests:
        actual=Path(path).read_bytes()
        for j,p in enumerate(params):
            predicted=struct.pack('<II',*transform(p,data[8*j:8*j+8]))
            expected=actual[j*8:j*8+8]
            print(path,j,predicted.hex(),expected.hex(),'OK' if predicted==expected else 'FAIL')
            assert predicted==expected
    print('All 18 block outputs match native execution.')
