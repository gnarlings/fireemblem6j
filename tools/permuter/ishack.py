#!/usr/bin/env python3
# usage: ishack.py FILE — exit 0 if the last function definition uses a fakematch construct or the file has a permuter-made helper
import re, sys

s = open(sys.argv[1]).read()
m = list(re.finditer(r"^\w[^;\n]*\([^;]*\)\s*\n\{", s, re.M))
body = s[m[-1].start():] if m else s
hack = re.search(r"\bvolatile\b|while\s*\(0\)|\bregister\b|\basm\b|__asm", body) or re.search(r"\binline_fn\d*\b", s)
sys.exit(0 if hack else 1)
