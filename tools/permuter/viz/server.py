#!/usr/bin/env python3
# usage: server.py [PORT] [RUN ...] — live best-score chart for climbers in tools/permuter/work (default: every run there)
import glob, json, os, re, subprocess, sys
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


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        page = os.path.join(HERE, "index.html")
        if self.path.startswith("/data"):
            body = json.dumps({"page": os.path.getmtime(page), "runs": [run_data(r) for r in runs()]}).encode()
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
ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
