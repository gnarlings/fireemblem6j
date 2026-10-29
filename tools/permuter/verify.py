#!/usr/bin/env python3
"""Splice a permuter candidate into the real source and run `make compare`.

usage: verify.py SRC FUNC CANDIDATE [--keep]
  Replaces FUNC's `#if NONMATCHING ... #endif // NONMATCHING` block in SRC with the candidate's last
  function definition, builds, and restores SRC unless --keep is given and the ROM matched.
  Extra make arguments come from $MAKE_ARGS (e.g. MAKE_ARGS=".SHELLFLAGS='-O xpg_echo -c'").
"""
import os, re, subprocess, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def last_function(text):
    m = list(re.finditer(r"^\w[^;\n]*\([^;]*\)\s*\n\{", text, re.M))
    if not m:
        sys.exit("candidate has no function definition")
    s = text[m[-1].start():]
    depth = 0
    for i, c in enumerate(s):
        depth += {"{": 1, "}": -1}.get(c, 0)
        if c == "}" and depth == 0:
            return s[: i + 1]
    sys.exit("unbalanced candidate")


def main():
    src, func, cand = sys.argv[1:4]
    keep = "--keep" in sys.argv
    path = os.path.join(REPO, src)
    orig = open(path).read()
    m = re.search(r"#if NONMATCHING\s*\n\s*(?:\w+\s+)*" + re.escape(func) + r"\(.*?#endif // NONMATCHING\n", orig, re.S)
    if not m:
        sys.exit(f"no NONMATCHING block for {func} in {src}")
    with open(path, "w") as f:
        f.write(orig[: m.start()] + last_function(open(cand).read()) + "\n" + orig[m.end():])
    rom = os.path.join(REPO, "fe6.gba")
    if os.path.exists(rom):
        os.remove(rom)
    r = subprocess.run(f"make -j{os.cpu_count()} compare {os.environ.get('MAKE_ARGS', '')}", shell=True, cwd=REPO, capture_output=True, text=True)
    ok = "fe6.gba: OK" in r.stdout + r.stderr
    print("MATCH" if ok else "NO MATCH")
    if not ok:
        print("\n".join((r.stdout + r.stderr).splitlines()[-15:]))
    if not (ok and keep):
        with open(path, "w") as f:
            f.write(orig)
        print(f"restored {src}")


main()
