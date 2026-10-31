from pathlib import Path
s=Path('check_split_states.py').read_text().replace("f'check_block{block}.smt2'", "f'cc2_block{block}.smt2'")
exec(compile(s,'check_split_states.py','exec'))
