from pathlib import Path
import sys,time,itertools
sys.argv=[sys.argv[0],'2']
exec(compile(Path('analysis/dictionary.py').read_text(),'dictionary.py','exec'))
N=fmpz(int(Path('analysis/n2_current.txt').read_text()))
coeffs=[fmpz(int(v))%N for v in json.load(open('analysis/candidate_A2.json'))]
extra='''walking_on_volcanos walking_on_volcanoes walk_on_the_volcano a_walk_on_a_volcano walking_on_a_curve walking_in_a_curve walking_on_a_graph walking_in_a_graph isogeny_walk_is_easy isogeny_walk_is_hard isogenies_are_evil isogenies_are_real isogenies_are_easy isogenies_are_hard isogeny_is_just_math isogenies_are_broken isogenies_are_unsafe isogenies_are_simple isogenies_are_secure isogenies_are_secret isogenies_are_tricky isogenies_are_sneaky isogenies_are_spooky isogenies_are_strong isogenies_are_pretty isogenies_are_smooth isogenies_are_random isogenies_are_linear isogenies_are_boring isogeny_is_not_safe isogeny_is_not_easy isogeny_is_not_scary isogeny_is_not_magic isogeny_is_not_trick isogeny_is_not_dead isogeny_is_not_aes elliptic_curves_rock elliptic_curves_win we_like_isogenies we_love_isogenies I_like_isogenies I_love_isogenies life_is_an_isogeny what_a_nice_isogeny what_a_nice_volcano what_a_random_walk this_is_an_isogeny this_is_a_volcano this_is_not_crypto this_is_not_random this_is_not_secure this_is_too_simple this_is_not_so_hard this_is_not_so_easy the_prime_is_leaked the_prime_is_hidden the_prime_is_secret the_prime_is_public prime_is_not_secret field_is_not_secret prime_is_very_small prime_is_too_small prime_is_the_secret modulus_is_not_safe find_a_small_factor find_the_modulus find_the_hidden_p find_the_secret_p recover_the_prime recover_the_secret recover_the_flag factor_the_modulus factor_the_integer just_factor_it factorization_time factoring_is_easy factoring_is_hard sage_is_very_smart sage_is_very_leaky sage_math_is_magic SageMath_is_magic let_us_walk_back can_you_walk_back lets_walk_it_back lets_walk_backwards can_you_walk_it_back reverse_the_walk retrace_your_steps back_and_forth_walk walk_back_and_forth isomorphic_curves isogenous_curves isogeny_is_a_thing nice_job_with_curves that_was_too_easy that_was_not_hard that_was_not_easy instinct_and_skill skill_over_instinct trust_your_instinct trust_the_instinct skills_pay_the_bills one_shot_one_kill focus_and_fire_away iso_is_not_so_easy iso_is_not_so_hard isogeny_meets_lll isogenies_and_lll isogeny_and_lattice isogeny_of_degree_2 isogeny_of_degree_4 only_two_isogenies only_four_isogenies just_two_isogenies just_one_isogeny only_one_isogeny 64_steps_backwards sixty_four_isogenies random_isogenies random_walks_are_fun random_walk_is_easy random_walk_is_hard random_walk_is_short not_so_random_walk not_a_random_walk random_walks_on_ice random_walks_on_EC random_walk_on_EC viva_la_isogenia praise_the_isogeny praise_the_volcano praise_the_lattice praise_the_LLL praise_the_LLL_algo'''.split()
for phrase in extra:
 if 14<=len(phrase)<=19:
  phrases.add(phrase+'!'*(19-len(phrase)))
  phrases.add(phrase+'_'*(19-len(phrase)))
count=0;t=time.time()
print('Expanded phrases',len(phrases),flush=True)
for pi,phrase in enumerate(sorted(phrases)):
 if len(phrase)!=19:continue
 opts=[leet.get(c,[c]) for c in phrase]
 for combination in itertools.product(*opts):
  body=''.join(combination)
  if body in seen:continue
  check(body);count+=1
 if pi%100==0:print('progress',pi,len(phrases),'candidates',count,'seconds',round(time.time()-t,1),flush=True)
print('Expanded done:',count,'seconds',time.time()-t,flush=True)
