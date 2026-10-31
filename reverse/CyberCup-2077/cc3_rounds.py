from pathlib import Path
import z3 as z
cs=z.parse_smt2_file('unpack_reduced.smt2')
for c in cs:
 if z.is_eq(c) and str(c.arg(0)).startswith('lut_') and 130<=int(str(c.arg(0))[4:])<=200:
  print(c.arg(0),'=',c.arg(1),flush=True)
