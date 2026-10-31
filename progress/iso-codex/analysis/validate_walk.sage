import collections,json
set_random_seed(42)
h={}
for d in [1,2,3,4]:
    h[d]=json.load(open('analysis/H%d.json'%d))
flag=b'ctfcup{0000000000000000000}'
counts=collections.Counter()
for trial in range(30):
    p=next_prime(getrandbits(128)); E=EllipticCurve(GF(p),j=int.from_bytes(flag,'little')); jstart=E.j_invariant(); stack=[jstart]
    if not E.isogenies_prime_degree(2):continue
    for _ in range(64):
        E=choice(E.isogenies_prime_degree(2)).codomain(); j=E.j_invariant()
        if len(stack)>1 and j==stack[-2]: stack.pop()
        else:stack.append(j)
    d=len(stack)-1;counts[d]+=1
    if d in h:
        a,b=E.a4(),E.a6();s=GF(p)(2)^(64+d)
        v=sum(GF(p)(int(co))*a^ex[1]*b^ex[2]*s^ex[3] for ex,co in h[d])
        assert v==0,(trial,d,v)
    elif d==0:
        a,b=E.a4(),E.a6()
        assert 4*a^3+27*b^2+31104*GF(p)(2)^64*a*b==0
    print(trial,d,dict(counts),flush=True)
