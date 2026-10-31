from fpylll import IntegerMatrix, LLL, GSO, Enumeration, EvaluatorStrategy
import itertools

def lift_flag(j,p):
    n=19
    fixed=int.from_bytes(b'ctfcup{'+bytes(n)+b'}','little')
    t=ZZ((ZZ(j)-fixed)*inverse_mod(256^7,p)%p)
    B=matrix(ZZ,n,n)
    B[0,0]=p
    for i in range(1,n):
        B[i,i]=1;B[i,0]=-power_mod(256,i,p)
    B=B.LLL()
    particular=vector(ZZ,[t]+[0]*(n-1))
    target=vector(ZZ,[79]*n)-particular
    # Exact nearest-plane reduction avoids precision loss for the 128-bit target.
    gs,_=B.gram_schmidt()
    residual=vector(QQ,target);near=vector(ZZ,[0]*n)
    for i in reversed(range(n)):
        k=ZZ(round(residual.dot_product(gs[i])/gs[i].dot_product(gs[i])))
        near+=k*B[i];residual-=k*B[i]
    mat=IntegerMatrix.from_matrix([list(row) for row in B])
    M=GSO.Mat(mat);M.update_gso()
    enum=Enumeration(M,nr_solutions=100000,strategy=EvaluatorStrategy.BEST_N_SOLUTIONS)
    results=enum.enumerate(0,n,float(47^2*n+1),0,target=M.from_canonical(tuple(residual)))
    found=[]
    for dist,coeff in results:
        v=vector(ZZ,[round(c) for c in coeff])*B
        x=particular+near+v
        if all(32<=c<=126 for c in x):
            flag=b'ctfcup{'+bytes(x)+b'}'
            assert int.from_bytes(flag,'little')%p==j
            found.append(flag)
    return found

if __name__=='__main__':
    p=next_prime(0xda9b6fc1d332b35719a45eab6fcbb7dd)
    flag=b'ctfcup{1s0g3ny_1s_n0t_h4rd}'
    j=int.from_bytes(flag,'little')%p
    result=lift_flag(j,p)
    print('Lift self-check:',len(result),'printable candidates; dummy flag present:',flag in result,flush=True)
    assert flag in result
