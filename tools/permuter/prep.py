#!/usr/bin/env python3
"""Build a decomp-permuter work dir (base.c, target.o, compile.sh, settings.toml) for one function.

usage: prep.py SRC FUNC SEED OUTDIR
  SRC    C file that holds FUNC, e.g. src/unitlistscreen.c (built without NONMATCHING, so FUNC is naked asm)
  FUNC   function name
  SEED   file whose last function definition is the C candidate to start from
  OUTDIR work dir to create
"""
import os, re, subprocess, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CPP = ["arm-none-eabi-cpp", "-I", "include", "-I", "asm/include", "-I", "tools/agbcc/include", "-I", ".", "-nostdinc", "-undef"]
COMPILE_SH = """#!/bin/bash
cd {repo}
iconv -f UTF-8 -t CP932 "$1" | tools/agbcc/bin/old_agbcc -mthumb-interwork -fhex-asm -O2 -o "$3.s" && arm-none-eabi-as -mcpu=arm7tdmi "$3.s" -o "$3"
r=$?; rm -f "$3.s"; exit $r
"""


def blocks(s):
    """Yield (header_start, body_start, body_end) for every top-level brace block."""
    depth, start = 0, None
    for i, c in enumerate(s):
        if c == "{":
            if depth == 0:
                start = i
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                h = max(s.rfind(";", 0, start), s.rfind("}", 0, start)) + 1
                yield h, start, i + 1


def fn_name(header):
    if not re.search(r"\)\s*$", header) or re.search(r"=\s*$", header):
        return None
    m = re.search(r"(\w+)\s*\((?:[^()]|\([^()]*\))*\)\s*$", header)
    return m and m.group(1)


def rewrite(s, keep, replace=None):
    """Turn every function except `keep` into a prototype; optionally swap `keep`'s text."""
    out, last = [], 0
    for h, b, e in blocks(s):
        name = fn_name(s[h:b])
        if not name or re.search(r"\binline\b", s[h:b]):
            continue
        if name == keep:
            if replace is not None:
                out.append(s[last:h] + "\n" + replace + "\n")
                last = e
            continue
        out.append(s[last:b].rstrip() + ";\n")
        last = e
    out.append(s[last:])
    return "".join(out)


def strip_attributes(s):
    out, i = [], 0
    while (j := s.find("__attribute__", i)) >= 0:
        out.append(s[i:j])
        k, d = s.index("(", j), 0
        while True:
            d += {"(": 1, ")": -1}.get(s[k], 0)
            k += 1
            if d == 0:
                break
        i = k
    out.append(s[i:])
    return "".join(out)


def truncate_after(s, func):
    for h, b, e in blocks(s):
        if fn_name(s[h:b]) == func:
            return s[:e] + "\n"
    sys.exit(f"{func} not found")


def last_function(text):
    found = [(h, e) for h, b, e in blocks(text) if fn_name(text[h:b])]
    if not found:
        sys.exit("seed has no function definition")
    h, e = found[-1]
    return text[h:e].strip()


def main():
    src, func, seed, out = sys.argv[1:5]
    os.makedirs(out, exist_ok=True)
    pp = subprocess.run(CPP + [src], cwd=REPO, capture_output=True, text=True, check=True).stdout

    with open(os.path.join(out, "compile.sh"), "w") as f:
        f.write(COMPILE_SH.format(repo=REPO))
    os.chmod(os.path.join(out, "compile.sh"), 0o755)
    with open(os.path.join(out, "settings.toml"), "w") as f:
        f.write(f'func_name = "{func}"\ncompiler_type = "base"\n')

    target_c = os.path.join(out, "target.c")
    with open(target_c, "w") as f:
        f.write(rewrite(pp, func))
    subprocess.run([os.path.join(out, "compile.sh"), os.path.abspath(target_c), "-o", os.path.abspath(os.path.join(out, "target.o"))], check=True)
    os.remove(target_c)

    seed_text = re.sub(r"//[^\n]*|/\*.*?\*/", "", open(seed).read(), flags=re.S)
    base = rewrite(pp, func, replace=last_function(seed_text))
    base = re.sub(r"^#.*$", "", strip_attributes(base), flags=re.M)
    base = truncate_after(rewrite(base, func), func)
    with open(os.path.join(out, "base.c"), "w") as f:
        f.write(base)
    print(f"{out}: ready")


main()
