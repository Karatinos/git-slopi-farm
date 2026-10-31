from pathlib import Path
import subprocess, threading, queue, re, time, json
base=Path(__file__).resolve().parent
n=int((base/'n2_current.txt').read_text())
lo=2*6079433314242371108270239373533376748
hi=2**128
out=base/'factor_hunt.log'
q=queue.Queue()
workers=4
bounds=[1000000,1000000,3000000,3000000]
factors=[]
def read_pipe(proc, idx, generation):
    for line in proc.stdout:
        q.put((idx,generation,line.strip()))
    q.put((idx,generation,None))
start=time.time();gen=0
with out.open('a',buffering=1) as log:
    def emit(s):
        line=f'[{time.time()-start:.1f}s] {s}'
        print(line,flush=True);log.write(line+'\n')
    while True:
        gen+=1
        subprocess.run(['docker','exec','-i','iso-math','sh','-c','cat > /tmp/iso_hunt.txt'],input=str(n)+'\n',text=True,check=True)
        emit(f'Generation {gen}: cofactor has {len(str(n))} digits')
        procs=[]
        for idx in range(workers):
            p=subprocess.Popen(['docker','exec','iso-math','ecm','-c','1000','-one','-inp','/tmp/iso_hunt.txt',str(bounds[idx])],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
            procs.append(p)
            threading.Thread(target=read_pipe,args=(p,idx,gen),daemon=True).start()
        got=None;completed=0;curves=0
        while completed<workers:
            idx,g,line=q.get()
            if g!=gen:continue
            if line is None:
                completed+=1
                continue
            log.write(f'worker {idx}: {line}\n')
            if line.startswith('Using B1='):
                curves+=1
                if curves%10==0:emit(f'{curves} curves started in generation {gen}')
            match=re.search(r'Factor found.*: (\d+)',line)
            if match:
                got=int(match.group(1));emit(f'FACTOR {got} ({got.bit_length()} bits)')
                break
        subprocess.run(['docker','exec','iso-math','pkill','ecm'],capture_output=True)
        for proc in procs:
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.kill()
        if not got:
            emit('No new factor in this batch');break
        assert n%got==0
        factors.append(str(got))
        (base/'hunt_factors.json').write_text(json.dumps(factors,indent=2))
        if lo<got<hi:
            (base/'candidate_p.txt').write_text(str(got)+'\n')
            emit('Target-sized factor found; saved candidate_p.txt')
            break
        n//=got
        (base/'n2_current.txt').write_text(str(n)+'\n')
