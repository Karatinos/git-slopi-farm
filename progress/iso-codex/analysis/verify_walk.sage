from pathlib import Path

def explicit_walk(flag,p,path):
    K=GF(p);R=PolynomialRing(K,'X');X=R.gen()
    d=len(path)
    assert d%2==0 and d<=64
    E=EllipticCurve(K,j=int.from_bytes(flag,'little'))
    scale=K(2)^(-((64+d)//2))
    roots=[]
    for root in reversed(path):
        r=-2*K(root)*scale^2
        phi=E.isogeny(X-r)
        E=phi.codomain();roots.append(ZZ(r));scale*=2
    for _ in range((64-d)//2):
        phi=E.isogenies_prime_degree(2)[0]
        r=-phi.kernel_polynomial()[0]
        E=phi.codomain();roots.append(ZZ(r))
        E=E.isogeny(X+2*r).codomain();roots.append(ZZ(-2*r))
    assert len(roots)==64
    return E,roots

if __name__=='__main__':
    # Synthetic example only; this does not contain the challenge flag.
    flag=b'ctfcup{1s0g3ny_1s_n0t_h4rd}'
    p=next_prime(0xda9b6fc1d332b35719a45eab6fcbb7dd)
    while True:
        K=GF(p);R=PolynomialRing(K,'X');X=R.gen()
        E0=EllipticCurve(K,j=int.from_bytes(flag,'little'))
        first=E0.isogenies_prime_degree(2)
        if first:
            phi=first[0];r=-phi.kernel_polynomial()[0];E1=phi.codomain()
            second=[f for f in E1.isogenies_prime_degree(2) if -f.kernel_polynomial()[0]!=-2*r]
            if second:break
        p=next_prime(p+1)
    target=second[0].codomain()
    for _ in range(31):
        phi=target.isogenies_prime_degree(2)[0];r=-phi.kernel_polynomial()[0]
        target=phi.codomain().isogeny(X+2*r).codomain()
    j=E0.j_invariant();matches=[]
    for f in target.isogenies_prime_degree(2):
        for g in f.codomain().isogenies_prime_degree(2):
            F=g.codomain()
            if F.a4()==-3*j*(j-1728)*K(2)^132 and F.a6()==-2*j*(j-1728)^2*K(2)^198:
                matches.append([ZZ(-f.kernel_polynomial()[0]),ZZ(-g.kernel_polynomial()[0])])
    assert matches
    for path in matches:
        actual,roots=explicit_walk(flag,p,path)
        assert actual==target
    print('Synthetic end-to-end verification passed: recovered dual path reproduces exactly 64 forward steps.',flush=True)
