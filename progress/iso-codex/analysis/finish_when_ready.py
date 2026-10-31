"""Validate new field-prime candidates locally and save a uniquely recovered flag."""
from pathlib import Path
import json,re,subprocess,time,os
ROOT=Path(__file__).resolve().parent.parent
A=6079433314242371108270239373533376748
B=-1779744368654530162000920720207404089
seen=set()
log=ROOT/'analysis/recovery_monitor.log'
def say(s):
 print(s,flush=True)
 with log.open('a') as f:f.write(s+'\n')
(ROOT/'analysis/recovery_monitor.pid').write_text(str(os.getpid())+'\n')
say('Local recovery monitor active; waiting for a target-sized prime factor.')
while True:
 candidates=[]
 pfile=ROOT/'analysis/candidate_p.txt'
 if pfile.exists():
  try:candidates.append(int(pfile.read_text()))
  except ValueError:pass
 hits=ROOT/'analysis/dictionary_hits.txt'
 if hits.exists():
  for line in hits.read_text().splitlines():
   m=re.search(r'(\d+)\s*$',line)
   if m:candidates.append(int(m.group(1)))
 for p in candidates:
  if p in seen or not 2*A<p<2**128+1024:continue
  seen.add(p);say('Checking candidate prime '+str(p))
  proc=subprocess.run(['docker','exec','iso-sage','sage','analysis/recover_from_p.sage',str(p)],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=1200)
  (ROOT/f'analysis/recovery_{p}.log').write_text(proc.stdout)
  say(proc.stdout)
  if proc.returncode:continue
  recovered=ROOT/'analysis/recovered.json'
  if not recovered.exists():continue
  rows=[r for r in json.loads(recovered.read_text()) if int(r['p'])==p]
  flags={s for r in rows for s in r['flags'] if re.fullmatch(r'ctfcup\{[A-Za-z0-9_!]+\}',s) and len(s)==27}
  if len(flags)!=1:
   say('No unique flag in the usual CTF character set; manual review required.')
   continue
  flag=flags.pop();row=next(r for r in rows if flag in r['flags'])
  # recover_from_p.sage asserts an explicit 64-step reconstruction for every saved candidate.
  result={'flag':flag,**row,'verification':'explicit 64 normalized degree-two isogenies reproduce both centered coefficients'}
  (ROOT/'analysis/verified_result.json').write_text(json.dumps(result,indent=2)+'\n')
  flagfile=ROOT/'VERIFIED_FLAG.txt'
  if not flagfile.exists():
   with flagfile.open('x') as f:f.write(flag+'\n')
  doc=f'''# Iso\n\nFlag: `{flag}`\n\n## Recovering the field\n\nThe generator hides the prime p and maps the little-endian flag integer to the j-invariant of an elliptic curve over GF(p). Sage's generic starting model is a=-3j(j-1728), b=-2j(j-1728)^2. For a model scaled by u, the coefficients satisfy\n\n```text\n4a^3 + 27b^2 + 31104 u^2 ab = 0 mod p.\n```\n\nA normalized degree-two isogeny with kernel root r maps (a,b) to (-4a-15r^2,22b+14ar), where r^3+ar+b=0. Following it with its normalized dual scales the coefficients to (16a,64b). Thus most immediate backtracks in the 64-step walk can be removed. For reduced length d, walking back d steps from the output reaches the initial model scaled with u^2=2^(64+d).\n\nThe script `analysis/walk_relations.py` takes polynomial norms over the possible kernel roots and removes the factors arising from backtracking. Evaluating the resulting relation at the published coefficients produces an integer divisible by the hidden prime. Factoring the candidate integer, then checking actual isogeny paths, recovered\n\n```text\np = {p}\nd = {row['d']}\nj = {row['j']}\n```\n\nThe factorization checkpoints and detailed derivation are retained in `PROGRESS.md` and `analysis/`.\n\n## Recovering the flag\n\nThe flag has 27 bytes. Fixing `ctfcup{{` and the final `}}` leaves 19 unknown bytes. The congruence int.from_bytes(flag,'little') = j mod p becomes one modular linear equation in these bytes. `analysis/lift_flag.sage` applies LLL and bounded closest-vector enumeration, then filters printable candidates. The unique candidate in the usual letter/digit/underscore/exclamation flag alphabet is the flag above.\n\n## Verification and reproduction\n\n`analysis/verify_walk.sage` converts the recovered reverse path into forward dual isogenies, corrects their scaling, and inserts enough dual backtracking pairs to make exactly 64 steps. For this flag it reproduces both published centered coefficients:\n\n```text\na4 = {A}\na6 = {B}\n```\n\nFrom the challenge directory, with SageMath and fpylll available:\n\n```sh\nsage analysis/recover_from_p.sage {p}\n```\n\nThis verifies the generator mathematically. No submission endpoint was supplied, so no platform acceptance is claimed.\n'''
  writeup=ROOT/'writeup.md'
  if not writeup.exists():
   with writeup.open('x') as f:f.write(doc)
  with (ROOT/'PROGRESS.md').open('a') as f:f.write('\n## Verified recovery\n\nFlag: `'+flag+'`. The explicit 64-step reconstruction passed. See `writeup.md` and `analysis/verified_result.json`.\n')
  say('VERIFIED FLAG: '+flag)
  raise SystemExit(0)
 time.sleep(2)
