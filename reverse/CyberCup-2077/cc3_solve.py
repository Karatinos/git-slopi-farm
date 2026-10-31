"""Reproduce the compact-model solution from the saved native trace parameters."""
from pathlib import Path
import itertools,json,string,subprocess
from cc3_model import transform

params=json.loads(Path('cc3_params.json').read_text())
targets=json.loads(Path('cc2_expected.json').read_text())
alphabet=string.ascii_letters+string.digits+'_'

def matches(j,s):
    a,b=transform(params[j],s.encode())
    return a|(b<<32)==targets[j]['target']

with Path('cc3_mitm_params.txt').open('w') as out:
    for p,t in zip(params[:8],targets):
        print(p['kind'],p['a'],p['b'],t['target']&0xffffffff,t['target']>>32,
              *p['masks'],*p['p'],*p['q'],file=out)
subprocess.run(['clang++','-O3','-std=c++20','cc3_mitm.cpp','-o','cc3_mitm'],check=True)
result=subprocess.run(['./cc3_mitm','4','2','3','6','7'],text=True,capture_output=True,check=True)
Path('cc3_mitm.log').write_text(result.stderr)
Path('cc3_mitm_candidates.jsonl').write_text(result.stdout)
blocks={}
for line in result.stdout.splitlines():
    record=json.loads(line);j=record['block'];value=record['value']
    assert j not in blocks,('Multiple MITM solutions',j)
    assert matches(j,value)
    blocks[j]=value

short0=['ctfcup{'+c for c in alphabet if matches(0,'ctfcup{'+c)]
short8=[''.join(c)+'}' for c in itertools.product(alphabet,repeat=2) if matches(8,''.join(c)+'}')]
assert len(short0)==len(short8)==1
blocks[0]=short0[0];blocks[8]=short8[0]

# The independently recovered chunks read "d...n7_0f_7h1S_t4sk_w4s_sp0n...".
# These two phrase hypotheses are tested against their exact 64-bit targets.
for j,word in [(1,'3v3l0pm3'),(5,'s0r3d_by')]:
    variants=itertools.product(*[(c.lower(),c.upper()) if c.isalpha() else (c,) for c in word])
    candidates=[''.join(s) for s in variants if matches(j,''.join(s))]
    assert len(candidates)==1,(j,candidates)
    blocks[j]=candidates[0]

flag=''.join(blocks[j] for j in range(9))
assert len(flag)==67
assert all(matches(j,flag[8*j:8*j+8]) for j in range(9))
Path('cc3_candidate.txt').write_text(flag+'\n')
print(flag)
print('All nine exact block targets match; run cc3_verify_native.py for aggregate/native verification.')
