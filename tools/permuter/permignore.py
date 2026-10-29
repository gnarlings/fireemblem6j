#!/usr/bin/env python3
# usage: permignore.py FILE — wrap lines holding ({ }) in PERM_IGNORE in place, which the permuter's parser needs
import re, sys


def wrap(text):
    out = []
    for l in text.split("\n"):
        if "({" in l and "PERM_IGNORE(" not in l:
            l = f"{l[:len(l) - len(l.lstrip())]}PERM_IGNORE( {l.strip()} )"
        out.append(l)
    return "\n".join(out)


def unwrap(text):
    return re.sub(r"^(\s*)PERM_IGNORE\( (.*) \)\s*$", r"\1\2", text, flags=re.M)


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    open(sys.argv[1], "w").write(wrap(s))
