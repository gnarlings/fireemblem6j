#!/usr/bin/env python3
# usage: ishack.py FILE — exit 0 if the file's last function definition uses a fakematch construct
import re, sys

s = open(sys.argv[1]).read()
m = list(re.finditer(r"^\w[^;\n]*\([^;]*\)\s*\n\{", s, re.M))
body = s[m[-1].start():] if m else s
sys.exit(0 if re.search(r"\bvolatile\b|while\s*\(0\)|\bregister\b|\basm\b|__asm", body) else 1)
