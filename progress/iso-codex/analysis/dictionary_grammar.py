from flint import fmpz
from pathlib import Path
import itertools,json,time
N=fmpz(int(Path('analysis/n2_current.txt').read_text()))
coeffs=[fmpz(int(v))%N for v in json.load(open('analysis/candidate_A2.json'))]
lo=2*6079433314242371108270239373533376748
S=fmpz(2)**132
batch=[];product=fmpz(1);count=0;start=time.time()
def check(body):
 global count,product,batch
 flag=b'ctfcup{'+body.encode()+b'}';assert len(flag)==27
 j=fmpz(int.from_bytes(flag,'little'));c=(-3*j*(j-1728)*S)%N
 v=fmpz(0)
 for co in reversed(coeffs):v=(v*c+co)%N
 product=product*v%N;batch.append((flag,v));count+=1
 if len(batch)==256:flush()
def flush():
 global batch,product
 g=product.gcd(N)
 if g>1:
  for flag,v in batch:
   h=v.gcd(N)
   if h>1:
    print('HIT',flag,str(h),flush=True)
    with open('analysis/dictionary_hits.txt','a') as f:f.write(f'{flag!r} {h}\n')
 batch=[];product=fmpz(1)
concepts='isogeny isogenies isomorphism isomorphisms isomorphy iso math maths SageMath sage Sage elliptic_curves elliptic_curve curves curve random_walk random_walks walk walks volcano volcanoes volcanos volcano_walking dual duality dual_isogeny dual_isogenies backtracking backtracks cycles cycle graph graphs lattices lattice LLL resultant resultants polynomial polynomials gcd norm norms prime primes modulus field fields finite_field finite_fields group groups factor factors factoring factorization security crypto cryptography secrecy degree small_degree low_degree endomorphism'.split()
adjs='easy hard fun cool good bad evil nice sweet tasty amazing awesome crazy insane simple weird funny tricky sneaky smart silly happy pretty sexy cute hot boring spooky scary weak safe secure dead alive broken insecure useless useful noisy leaky hidden public secret random short small large long slow fast enough magic magical difficult key linear valid great old new false true dual cyclic integer rational modular impressive beautiful powerful strong important overrated smooth shaky lost everywhere cool_stuff too_easy too_hard not_easy not_hard not_safe not_secure not_dead a_lie a_joke a_trap not_random not_really the_key the_best the_way my_friend a_good_idea a_bad_idea'.split()
verbs='find recover compute calculate break crack solve reverse invert guess know hide reveal leak factor love like hate learn understand study use trust follow enjoy praise watch discover remember forget'.split()
phrases=set()
def add(s):
 if 16<=len(s)<=19:
  phrases.add(s+'!'*(19-len(s)))
  if len(s)==18:phrases.add(s+'_')
for c in concepts:
 for a in adjs:
  for fmt in ['{c}_is_{a}','{c}_are_{a}','{c}_is_not_{a}','{c}_are_not_{a}','{c}_is_so_{a}','{c}_are_so_{a}','{c}_is_very_{a}','{c}_are_very_{a}','the_{c}_is_{a}','the_{c}_are_{a}','{a}_{c}','{c}_sounds_{a}']:
   add(fmt.format(c=c,a=a))
 for v in verbs:
  for fmt in ['{v}_the_{c}','{v}_your_{c}','{v}_my_{c}','{v}_some_{c}','{v}_a_{c}','{v}_an_{c}','just_{v}_{c}','can_you_{v}_{c}','please_{v}_{c}','we_{v}_{c}','i_{v}_{c}','I_{v}_{c}','lets_{v}_{c}']:
   add(fmt.format(c=c,v=v))
 for fmt in ['there_is_no_{c}','there_are_no_{c}','no_{c}_no_problem','look_ma_no_{c}','nothing_but_{c}','what_a_nice_{c}','what_a_cool_{c}','this_is_{c}','this_is_a_{c}','this_is_not_{c}','that_is_not_{c}','my_first_{c}','your_first_{c}','my_beloved_{c}','all_you_need_is_{c}','{c}_is_all_you_need','{c}_goes_brrrr','{c}_go_brrrr','{c}_for_the_win','{c}_ftw','{c}_everywhere','{c}_wins_again','{c}_strikes_back']:
  add(fmt.format(c=c))
for c in ['walk','walking','walks','step','stepping','run','running','jump','jumping','hike','hiking']:
 for prep in ['on','in','over','around','through','along','into','down','up']:
  for place in ['volcano','volcanoes','volcanos','curves','circles','cycle','graph','isogenies','curve','field','Fp','the_volcano','the_curve','the_graph','a_volcano','a_curve','a_circle']:
   add(c+'_'+prep+'_'+place)
for s in '''always_go_back_home return_to_your_home that_was_not_random dont_forget_the_p dont_forget_the_prime nothing_but_duality deal_with_the_dual two_degree_isogeny low_degree_isogeny a_walk_to_remember dual_isogenies_rule compute_isomorphism find_an_isomorphism no_randomness_here what_goes_around_comes_around back_to_where_we_were back_to_the_start back_to_the_origin back_to_the_beginning back_to_the_future isogeny_is_a_homomorphism not_all_isogenies_are_equal normalize_your_curve normalization_is_key'''.split():add(s)
leet={'a':['a','4'],'e':['e','3'],'i':['i','1'],'l':['l','1'],'o':['o','0'],'s':['s','5'],'t':['t','7'],'g':['g','9'],'b':['b','8']}
print('Phrases',len(phrases),flush=True)
for pi,phrase in enumerate(sorted(phrases)):
 keys=sorted(set(phrase)&leet.keys())
 for combo in itertools.product(*(leet[k] for k in keys)):
  body=phrase.translate(str.maketrans(dict(zip(keys,combo))))
  check(body)
 if pi%1000==0:print('progress',pi,'candidates',count,'seconds',round(time.time()-start,1),flush=True)
flush();print('DONE',count,round(time.time()-start,1),flush=True)
Path('analysis/grammar_phrases.json').write_text(json.dumps(sorted(phrases)))
