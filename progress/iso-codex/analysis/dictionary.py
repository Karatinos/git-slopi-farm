from flint import fmpz
from pathlib import Path
import itertools,json,time,sys
d=int(sys.argv[1]) if len(sys.argv)>1 else 2
N=fmpz(int(Path(f'analysis/cofactor{d}.txt').read_text()))
coeffs=[fmpz(int(v))%N for v in json.load(open(f'analysis/candidate_A{d}.json'))]
lo=2*6079433314242371108270239373533376748

def check(body):
 flag=b'ctfcup{'+body.encode()+b'}'
 assert len(flag)==27
 j=fmpz(int.from_bytes(flag,'little'))
 c=(-3*j*(j-1728)*2**(128+2*d))%N
 v=fmpz(0)
 for co in reversed(coeffs):v=(v*c+co)%N
 g=v.gcd(N)
 if g>=lo:
  print('CANDIDATE',flag,g,flush=True)
  with open('analysis/dictionary_hits.txt','a') as f:f.write(f'{flag!r} {g}\n')

phrases=set('''isogeny_is_not_hard
isogenies_are_magic
isogenies_are_scary
isogenies_are_great
isogenies_are_tough
isogenies_are_weird
isogenies_are_funny
isogeny_random_walk
random_isogeny_walk
elliptic_curve_walk
isomorphism_is_easy
isomorphism_is_hard
isogenies_are_tasty
isogenies_are_crazy
isogenies_are_fancy
isogenies_are_sweet
isogenies_are_nasty
isogenies_are_smart
isogenies_are_sexy
isogenies_are_funky
isogenies_are_lucky
isogenies_are_tricky
'''.split())
words='easy hard nice good cool fast slow safe weak sick cute sexy evil free real dead dumb best fine fun bad odd new old mad sad raw big hot red way day bit key art'.split()
for w in words:
 phrases.add('isogeny_is_not_'+w)
 phrases.add('isomorphism_is_'+w)
for a,b,c in itertools.product(['isogeny','isogenies','curves','elliptic','random','hidden','modulus','prime','field','walking','walk','rational','iso'],['is','are','of','and','the','with','over','in','on'],['easy','hard','magic','scary','great','tough','weird','funny','crazy','fancy','sweet','smart','lucky','numbers','curves','fields','primes','a_prime','not_hard','not_easy','not_dead','not_safe','not_good','a_curve','the_key','a_field']):
 phrases.add(a+'_'+b+'_'+c)
phrases.update('''no_prime_no_problem
no_field_no_problem
a_walk_in_the_curve
praise_the_SageMath
praise_the_iso_walk
we_love_isogenies
math_is_beautiful
isogenies_are_fun
I_love_isogenies
i_love_isogenies
nice_isogeny_walk
nice_job_well_done
we_broke_isogenies
you_broke_isogenies
recover_the_modulus
recover_the_prime
find_the_modulus
isogeny_in_the_wild
isogenies_over_Fp
isogeny_volcano
isogeny_volcanoes
isogeny_and_lattice
isogeny_is_cool
isogenies_are_cool
isogeny_is_easy
isogeny_is_hard
'''.split())
phrases={p+'!'*(19-len(p)) for p in phrases if 16<=len(p)<=19}
leet={'a':['a','4'],'e':['e','3'],'i':['i','1'],'l':['l','1'],'o':['o','0'],'s':['s','5'],'t':['t','7'],'g':['g','9'],'b':['b','8']}
seen=set();t=time.time()
for phrase in phrases:
 if len(phrase)!=19:continue
 letters=sorted(set(phrase)&leet.keys())
 for combo in itertools.product(*(leet[k] for k in letters)):
  table=str.maketrans(dict(zip(letters,combo)));body=phrase.translate(table)
  if body in seen:continue
  seen.add(body);check(body)
print('tested',len(seen),'time',time.time()-t,flush=True)
