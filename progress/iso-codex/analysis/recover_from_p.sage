import sys,json
from pathlib import Path
exec(preparse(Path('analysis/lift_flag.sage').read_text().split("if __name__")[0]))
exec(preparse(Path('analysis/verify_walk.sage').read_text().split("if __name__")[0]))
A=6079433314242371108270239373533376748
B=-1779744368654530162000920720207404089
p=ZZ(sys.argv[1]) if len(sys.argv)>1 else ZZ(Path('analysis/candidate_p.txt').read_text())
print('p =',p,'bits =',p.nbits(),'prime =',p.is_prime(),flush=True)
assert p.is_prime() and p>2*max(abs(A),abs(B)) and p<=2^128+1024
K=GF(p);E=EllipticCurve(K,[A,B]);saves=[]
layer=[(E,[])];seen_js=set()
for d in range(7):
    print('depth',d,'curves',len(layer),flush=True)
    if d%2==0:
        for F,path in layer:
            j=F.j_invariant()
            if F.a4()!=-3*j*(j-1728)*K(2)^(128+2*d):continue
            if F.a6()!=-2*j*(j-1728)^2*K(2)^(192+3*d):continue
            if ZZ(j) in seen_js:continue
            seen_js.add(ZZ(j))
            print('MATCH: depth',d,'j',j,flush=True)
            flags=lift_flag(ZZ(j),p)
            print('Printable candidates:',len(flags),flush=True)
            for flag in flags:
                check,roots=explicit_walk(flag,p,path)
                assert check.a4().lift_centered()==A and check.a6().lift_centered()==B
                print('Verified with explicit 64-step walk:',flag,flush=True)
            saves.append({'p':str(p),'d':d,'j':str(j),'path':[str(r) for r in path], 'flags':[f.decode() for f in flags]})
            Path('analysis/recovered.json').write_text(json.dumps(saves,indent=2))
    next_layer=[]
    for F,path in layer:
        for phi in F.isogenies_prime_degree(2):
            r=-phi.kernel_polynomial()[0]
            # A dual step has kernel x-coordinate -2*r_previous after transport.
            if path and r==-2*K(path[-1]):continue
            next_layer.append((phi.codomain(),path+[ZZ(r)]))
    layer=next_layer
print('Total matching initial invariants:',len(seen_js),flush=True)
