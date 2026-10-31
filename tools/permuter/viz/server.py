#!/usr/bin/env python3
# usage: server.py [PORT] [RUN ...] — live best-score chart for climbers in tools/permuter/work (default: every run there)
import difflib, glob, json, os, re, subprocess, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(os.path.dirname(HERE), "work")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
RUNS = sys.argv[2:]


def tail(path, n=4000):
    with open(path, "rb") as f:
        f.seek(max(0, os.path.getsize(path) - n))
        return f.read().decode(errors="replace")


def base_score(log):
    if os.path.exists(log):
        m = re.search(r"base score = (\d+)", open(log, errors="replace").read(4000))
        return m and int(m.group(1))


def run_data(run):
    d = os.path.join(WORK, run)
    events = []
    for b in glob.glob(f"{d}/gen-*/base.c") + [f"{d}/base.c"]:
        s = base_score(os.path.join(os.path.dirname(b), "run.log"))
        if s is not None:
            events.append((os.path.getmtime(b), s))
    for o in glob.glob(f"{d}/output-*") + glob.glob(f"{d}/gen-*/output-*"):
        m = re.match(r"output-(\d+)-", os.path.basename(o))
        if m:
            events.append((os.path.getmtime(o), int(m.group(1))))
    events.sort()
    points, best = [], None
    for t, s in events:
        if best is None or s < best:
            best = s
            points.append({"t": t, "score": s})
    log = f"{d}/run.log"
    its = re.findall(r"iteration (\d+)", tail(log)) if os.path.exists(log) else []
    alive = subprocess.run(["pgrep", "-f", f"permuter.py {d} "], capture_output=True).returncode == 0
    return {"run": run, "points": points, "iterations": int(its[-1]) if its else None, "alive": alive}


def runs():
    if RUNS:
        return RUNS
    return sorted(n for n in os.listdir(WORK) if os.path.isdir(os.path.join(WORK, n))) if os.path.isdir(WORK) else []


SMELLS = {
    "permuter temporary": r"\bnew_var\d*\b",
    "self-assignment": r"\b(\w+) = \1(?: & \1)?;",
    "no-op arithmetic": r"\^ 0\b|\+ 0\b|\* 1\b|& 0xFF\b|\(0, ",
    "constant condition": r"\bif \((?:0|1)\)",
    "empty statement": r"^;$",
    "inline helper": r"\binline_fn\d*\b",
}
variant_cache = {}


def statements(path):
    """The last function's statements, one per line, without layout differences."""
    s = re.sub(r"PERM_IGNORE\( (.*) \)", r"\1", open(path, errors="replace").read())
    m = list(re.finditer(r"^\w[^;\n]*\([^;]*\)\s*\n\{", s, re.M))
    out = []
    for l in s[m[-1].start():].splitlines()[2:]:
        l = l.strip().removeprefix("} ")
        if l.startswith("int ") and "," in l:
            out += [f"int {v.strip().rstrip(';')};" for v in l[4:].split(",")]
        elif l not in ("", "{", "}"):
            out.append(l)
    return out


def variant(o, base):
    if o not in variant_cache:
        key = lambda l: re.sub(r"[\s()]", "", l)
        new = statements(f"{o}/source.c")
        diff = []
        ops = difflib.SequenceMatcher(None, [key(l) for l in base], [key(l) for l in new], autojunk=False).get_opcodes()
        for op, a0, a1, b0, b1 in ops:
            if op != "equal":
                diff += [["-", l] for l in base[a0:a1]] + [["+", l] for l in new[b0:b1]]
        added = [l for sign, l in diff if sign == "+"]
        smells = [n for n, p in SMELLS.items() if any(re.search(p, l) for l in added)]
        text = [re.sub(r"[\s()]", "", l) for l in added]
        if any("++" in l for l in text) and any("--" in l for l in text):
            smells.append("cancelling steps")
        variant_cache[o] = {"name": os.path.basename(o), "t": os.path.getmtime(o), "diff": diff, "smells": smells}
    return variant_cache[o]


def matches():
    """Every run's score-0 variants, cleanest first: fewest smells, then the smallest change from the base."""
    found = []
    for run in runs():
        d = os.path.join(WORK, run)
        if not os.path.exists(f"{d}/base.c"):
            continue
        outs = glob.glob(f"{d}/output-0-*") + glob.glob(f"{d}/gen-*/output-0-*")
        if outs:
            base = statements(f"{d}/base.c")
            found += [{**variant(o, base), "run": run} for o in outs if os.path.exists(f"{o}/source.c")]
    found.sort(key=lambda v: (len(v["smells"]), len(v["diff"]), v["t"]))
    return {"total": len(found), "variants": found[:40]}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        page = os.path.join(HERE, "index.html")
        if self.path.startswith("/data"):
            body = json.dumps({"page": os.path.getmtime(page), "runs": [run_data(r) for r in runs()]}).encode()
            ctype = "application/json"
        elif self.path.startswith("/matches"):
            body = json.dumps(matches()).encode()
            ctype = "application/json"
        elif self.path in ("/", "/index.html"):
            body = open(page, "rb").read()
            ctype = "text/html; charset=utf-8"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


print(f"http://127.0.0.1:{PORT}/", flush=True)
ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
