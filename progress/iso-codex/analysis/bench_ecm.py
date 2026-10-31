from pathlib import Path
import subprocess,os,time
root=Path(__file__).resolve().parent
for tag,opts in [('param0',['-param','0']),('param1',['-param','1']),('param2',['-param','2']),('torsion16',['-torsion','Z2xZ8'])]:
 t=time.time()
 p=subprocess.run(['/opt/homebrew/bin/ecm','-v','-inp',str(root/'n2_current.txt')]+opts+['100000'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,env=dict(os.environ,OMP_NUM_THREADS='1'),timeout=180)
 (root/f'bench_ecm_{tag}.log').write_text(p.stdout)
 print(tag,'wall',round(time.time()-t,2),'return',p.returncode,flush=True)
 lines=p.stdout.splitlines()
 for i,l in enumerate(lines):
  if l.startswith('Step '):print(l,flush=True)
  if l.startswith('Expected number') or l.startswith('Expected time'):print('\n'.join(lines[i:i+3]),flush=True)
