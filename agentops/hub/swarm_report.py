#!/usr/bin/env python3
"""swarm-report: the client for the swarm hub. Standard library only. Full contract: docs/REPORTING.md.

Python (on every server: `import swarm_report as sr`; elsewhere copy this one file):

    import swarm_report as sr

    # once per experiment type (idempotent; usually from experiments/<id>/experiment.yaml)
    sr.register("boids-noise", title="Boids: order vs noise", params={"n": {"type": "int"}, "eta": {"type": "float"}},
                metrics=["order", "collisions"], primary_metric="order")

    # coordinator: queue a sweep
    sr.enqueue("boids-noise", [{"n": 200, "eta": e / 10} for e in range(11)])

    # worker: take queued runs until none are left; a crash marks that run failed and moves on
    def simulate(run):
        p = run.params                              # {"n": 200, "eta": 0.3}
        for step in range(100):
            run.progress(step + 1, 100, order=0.5, collisions=3)   # throttled to 1 call / 2 s
        run.artifact("order_vs_t.png")              # upload a file; rendered on the dashboard
        run.done(order=0.91, message="transition near eta=0.42")
    sr.work("boids-noise", simulate)

    # or by hand: start on enter, done on clean exit, failed on exception
    while (run := sr.next_run("boids-noise")):
        with run:
            ...

    # ad-hoc run without the queue
    with sr.start("boids-noise", params={"n": 50, "eta": 0.3}) as run: ...

CLI (installed as `swarm-report` on every server):

    swarm-report register experiments/boids-noise/experiment.yaml   (or .json)
    swarm-report enqueue -e boids-noise -p n=200 --grid eta=0,0.1,0.2 --grid seed=1,2,3
    swarm-report next -e boids-noise                 # prints the assigned run as JSON (exit 3 if queue empty)
    swarm-report start|progress|log|done|fail -r <run> [-e exp] [-M name=value] [--step N --total T] [-m msg]
    swarm-report artifact -r <run> path/to/file [--name plots/a.png]
    swarm-report runs -e boids-noise [--status planned]
    swarm-report heartbeat                           # host stats; a timer runs this every minute
    swarm-report flush                               # replay anything spooled while the hub was down

Config, first found wins: environment, ~/.config/swarm/report.env, /etc/swarm/report.env.
    SWARM_HUB_URL, SWARM_HUB_TOKEN, SWARM_SOURCE (<person>/<tool>-<n>, e.g. alice/claude-1),
    SWARM_ROLE (coordinator | worker), SWARM_HOST.

Progress reports never raise: a hub outage prints a warning and the experiment keeps going.
Queue and artifact calls raise HubError, because silently losing those is worse.
"""
from __future__ import annotations

import argparse
import fcntl
import itertools
import json
import mimetypes
import os
import shutil
import socket
import subprocess
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

HEARTBEAT_EVERY = 60  # seconds between per-run keepalives (hub LEASE is 20 min)
CONFIG_FILES = [Path.home() / ".config/swarm/report.env", Path("/etc/swarm/report.env")]


class HubError(RuntimeError):
    pass


def _config() -> dict:
    cfg = {}
    for f in reversed(CONFIG_FILES):
        try:
            for line in f.read_text().splitlines():
                if "=" in line and not line.lstrip().startswith("#"):
                    k, v = line.split("=", 1)
                    cfg[k.strip()] = v.strip().strip("'\"")
        except OSError:
            pass
    for k in ("SWARM_HUB_URL", "SWARM_HUB_TOKEN", "SWARM_SOURCE", "SWARM_ROLE", "SWARM_HOST"):
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    return cfg


def _source(cfg):
    return cfg.get("SWARM_SOURCE") or os.environ.get("USER") or "unknown"


def _host(cfg):
    return cfg.get("SWARM_HOST") or socket.gethostname()


def _call(method: str, path: str, body=None, *, raw: bytes | None = None, ctype="application/json",
          timeout: float = 30, source: str | None = None):
    cfg = _config()
    base, token = cfg.get("SWARM_HUB_URL", "").rstrip("/"), cfg.get("SWARM_HUB_TOKEN", "")
    if not base or not token:
        raise HubError("SWARM_HUB_URL / SWARM_HUB_TOKEN not set (see /etc/swarm/report.env)")
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(base + path, data=data, method=method, headers={
        "Authorization": f"Bearer {token}", "Content-Type": ctype, "X-Swarm-Source": source or _source(cfg)})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        raise HubError(f"{method} {path}: {e.code} {e.read().decode()[:300]}") from None
    except (urllib.error.URLError, OSError) as e:
        raise HubError(f"{method} {path}: hub unreachable ({e})") from None


# ---------------------------------------------------------------- spool: nothing is lost while the hub is down
#
# When the hub cannot be reached, events and artifact uploads are written to a local spool
# (~/.cache/swarm/spool, or $SWARM_SPOOL) and replayed in order on the next successful call, by
# `swarm-report flush`, and by every server's minute timer (`flush --all`, as root). While anything is
# spooled, new reports queue behind it, so the hub always receives them in the order they happened.

def _spool_dir() -> Path:
    return Path(os.environ.get("SWARM_SPOOL") or Path.home() / ".cache/swarm/spool")


def _retryable(e: Exception) -> bool:
    m = re.search(r": (\d{3}) ", str(e))
    return "unreachable" in str(e) or (m is not None and m.group(1) in ("429", "500", "502", "503", "504"))


def _spool_put(item: dict, data_file: Path | None = None) -> None:
    d = _spool_dir()
    d.mkdir(parents=True, exist_ok=True)
    stem = f"{time.time_ns():020d}-{os.getpid()}-{uuid.uuid4().hex[:6]}"
    if data_file is not None:
        blob = d / f"{stem}.blob"
        tmp = blob.with_suffix(".blob.tmp")
        shutil.copyfile(data_file, tmp)
        os.replace(tmp, blob)
        item["blob"] = blob.name
    meta = d / f"{stem}.json"
    tmp = meta.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(item, f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, meta)


def _pending(d: Path | None = None) -> list:
    d = d or _spool_dir()
    try:
        return sorted(p for p in d.glob("*.json"))
    except OSError:
        return []


def flush(dirs: list | None = None, quiet: bool = False) -> tuple:
    """Replay spooled events and uploads in order. Stops at the first failure (order matters).
    Returns (sent, left). Items the hub rejects as invalid (4xx) move to spool/dead/ and are skipped."""
    sent = left = 0
    for d in dirs or [_spool_dir()]:
        items = _pending(d)
        if not items:
            continue
        lockf = open(d / ".lock", "a+")
        try:
            fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            left += len(items)          # another process is flushing this spool
            continue
        try:
            items = _pending(d)
            for i, meta in enumerate(items):
                try:
                    item = json.loads(meta.read_text())
                except (OSError, ValueError):
                    meta.unlink(missing_ok=True)
                    continue
                try:
                    if item["type"] == "event":
                        _call("POST", "/api/v1/report", item["event"], timeout=15, source=item["event"].get("source"))
                    else:
                        blob = d / item["blob"]
                        q = urllib.parse.urlencode({"run": item["run"], "name": item["name"],
                                                    **({"attempt": item["attempt"]} if item.get("attempt") else {})})
                        _call("PUT", f"/api/v1/artifacts?{q}", raw=blob.read_bytes(), ctype=item["ctype"],
                              timeout=600, source=item.get("source"))
                except HubError as e:
                    if _retryable(e):
                        left += len(items) - i
                        break
                    dead = d / "dead"
                    dead.mkdir(exist_ok=True)
                    meta.rename(dead / meta.name)
                    if item.get("blob"):
                        (d / item["blob"]).rename(dead / item["blob"])
                    print(f"swarm-report: hub rejected a spooled item, kept in {dead}: {e}", file=sys.stderr)
                    continue
                if item.get("blob"):
                    (d / item["blob"]).unlink(missing_ok=True)
                meta.unlink(missing_ok=True)
                sent += 1
        finally:
            fcntl.flock(lockf, fcntl.LOCK_UN)
            lockf.close()
    if sent and not quiet:
        print(f"swarm-report: replayed {sent} spooled item(s){f', {left} still waiting' if left else ''}", file=sys.stderr)
    return sent, left


# ---------------------------------------------------------------- events (never raise, never lost)

def report(kind: str, experiment: str | None = None, run: str | None = None, *, message: str | None = None,
           step: float | None = None, total: float | None = None, progress: float | None = None,
           metrics: dict | None = None, url: str | None = None, status: str | None = None,
           data: dict | None = None, params: dict | None = None, source: str | None = None,
           role: str | None = None, strict: bool = False, attempt: int | None = None) -> bool:
    cfg = _config()
    if params:
        data = {**(data or {}), "params": params}
    ev = {"kind": kind, "experiment": experiment, "run": run, "message": message, "step": step, "total": total,
          "progress": progress, "metrics": metrics, "url": url, "status": status, "data": data,
          "source": source or _source(cfg),
          "role": role or cfg.get("SWARM_ROLE") or ("server" if kind == "heartbeat" and not experiment else "worker"),
          "host": _host(cfg), "ts": time.time(), "attempt": attempt}
    body = {k: v for k, v in ev.items() if v is not None}
    if kind == "heartbeat":                     # keepalives are never spooled: only "now" matters
        try:
            _call("POST", "/api/v1/report", body, timeout=10)
            return True
        except HubError as e:
            if strict:
                raise
            print(f"swarm-report: warning: {e}", file=sys.stderr)
            return False
    if _pending() and flush(quiet=True)[1]:     # older items still waiting: queue behind them
        _spool_put({"type": "event", "event": body})
        return False
    try:
        _call("POST", "/api/v1/report", body, timeout=10)
        return True
    except HubError as e:
        if strict:
            raise
        if _retryable(e):
            _spool_put({"type": "event", "event": body})
            print(f"swarm-report: hub unavailable, {kind} spooled locally and will be replayed ({e})", file=sys.stderr)
        else:
            print(f"swarm-report: warning: {e}", file=sys.stderr)
        return False


# ---------------------------------------------------------------- experiments + queue

def register(experiment: str, *, title: str | None = None, description: str | None = None,
             params: dict | None = None, metrics: list | None = None, primary_metric: str | None = None,
             owner: str | None = None, url: str | None = None) -> dict:
    """Create or update an experiment type. params: {name: {"type": ..., "default": ..., "description": ...}}."""
    body = {"id": experiment, "title": title, "description": description, "params": params, "metrics": metrics,
            "primary_metric": primary_metric, "owner": owner, "url": url}
    return _call("POST", "/api/v1/experiments", {k: v for k, v in body.items() if v is not None})


def enqueue(experiment: str, params_list: list, *, priority: int = 0, tags: list | None = None,
            run_ids: list | None = None) -> list:
    """Queue planned runs. Returns their run ids. Workers take them with next_run()."""
    items = [{"experiment": experiment, "params": p, "priority": priority, "tags": tags or [],
              **({"run": run_ids[i]} if run_ids else {}), "source": _source(_config())}
             for i, p in enumerate(params_list)]
    return _call("POST", "/api/v1/runs", items)["runs"]


PAUSED = False   # set by next_run(): the hub is paused for this experiment (or everything)


def pause(experiment: str | None = None, reason: str | None = None) -> dict:
    """Emergency stop for new work: the hub hands out no new runs (all experiments, or one).
    Runs in progress finish; idle sr.work workers wait. Undo with resume()."""
    return _call("POST", "/api/v1/pause", {"experiment": experiment, "reason": reason})


def resume(experiment: str | None = None) -> dict:
    return _call("POST", "/api/v1/resume", {"experiment": experiment})


def next_run(experiment: str | None = None) -> "Run | None":
    """Take the next queued run. Safe to retry: the request id makes a repeated request (lost response)
    return the same run instead of assigning a second one."""
    cfg = _config()
    req = {"experiment": experiment, "source": _source(cfg), "host": _host(cfg), "request_id": uuid.uuid4().hex}
    global PAUSED
    for attempt in range(4):
        try:
            resp = _call("POST", "/api/v1/runs/next", req)
            r, PAUSED = resp["run"], bool(resp.get("paused"))
            break
        except HubError as e:
            if attempt == 3 or not _retryable(e):
                raise
            time.sleep(2 * (attempt + 1))
    return Run(r["run"], r["experiment"], r.get("params") or {}, r.get("attempts")) if r else None


_CLIENT_FILE = Path(__file__).resolve()
_CLIENT_MTIME = _CLIENT_FILE.stat().st_mtime if _CLIENT_FILE.exists() else 0.0


def refresh_if_updated() -> None:
    """Between runs: if this server's client was updated after this process loaded it, flush the spool
    and re-launch the process with the same arguments, so long-lived workers pick up client fixes
    without anyone restarting them and without interrupting a run. SWARM_NO_AUTO_REFRESH=1 disables it."""
    if os.environ.get("SWARM_NO_AUTO_REFRESH"):
        return
    try:
        if _CLIENT_FILE.stat().st_mtime <= _CLIENT_MTIME:
            return
    except OSError:
        return
    script = sys.argv[0] if sys.argv else ""
    if not script or script in ("-c", "-m") or not Path(script).exists():
        print("swarm-report: the client was updated; restart this worker between runs to pick it up", file=sys.stderr)
        return
    if _pending():
        flush(quiet=True)
    print(f"swarm-report: client updated; re-launching {script} between runs", file=sys.stderr, flush=True)
    os.execv(sys.executable, [sys.executable] + sys.argv)


def work(experiment: str, fn, *, max_runs: int | None = None, stop_when_empty: bool = True, poll: float = 30) -> int:
    """Worker loop: take queued runs for `experiment` and call fn(run) for each.

    fn gets a Run (run.params, run.progress(...), run.artifact(...)). A run is marked done when fn
    returns and failed when it raises; the loop keeps going either way. Returns how many runs it took.
    With stop_when_empty=False it waits `poll` seconds for new work instead of returning."""
    n = 0
    while max_runs is None or n < max_runs:
        if max_runs is None:            # a bounded worker would restart its count: it finishes and exits instead
            refresh_if_updated()
        if _pending():
            flush(quiet=True)
        try:
            run = next_run(experiment)
        except HubError as e:
            print(f"swarm-report: {e}; retrying in {poll}s", file=sys.stderr)
            time.sleep(poll)
            continue
        if run is None:
            if PAUSED:                  # paused by a human: wait, never exit (so resume restarts the work)
                print(f"swarm-report: hub is paused for {experiment or 'all experiments'}; waiting", file=sys.stderr)
                time.sleep(poll)
                continue
            if stop_when_empty:
                return n
            time.sleep(poll)
            continue
        n += 1
        try:
            with run:
                fn(run)
        except Exception as e:  # noqa: BLE001 - already reported as failed by Run.__exit__
            print(f"swarm-report: {run.id} failed: {type(e).__name__}: {e}", file=sys.stderr)
    return n


def start(experiment: str, run: str | None = None, params: dict | None = None, message: str | None = None) -> "Run":
    """An ad-hoc run (not from the queue). Reports `start` immediately."""
    # random suffix: two runs started in the same second by one process must not share an id
    run = run or f"{experiment}/{time.strftime('%m%d-%H%M%S')}-{os.urandom(3).hex()}"
    r = Run(run, experiment, params or {})
    r._start(message)
    return r


def runs(experiment: str | None = None, status: str | None = None, limit: int = 200) -> list:
    q = urllib.parse.urlencode({k: v for k, v in {"experiment": experiment, "status": status, "limit": limit}.items() if v})
    return _call("GET", f"/api/v1/runs?{q}")


def get_run(run: str) -> dict:
    return _call("GET", f"/api/v1/runs/{urllib.parse.quote(run, safe='/')}")


def upload(run: str, path: str | Path, name: str | None = None, attempt: int | None = None) -> dict:
    p = Path(path)
    name = name or p.name
    ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
    q = urllib.parse.urlencode({"run": run, "name": name, **({"attempt": attempt} if attempt else {})})
    item = {"type": "upload", "run": run, "name": name, "ctype": ctype, "source": _source(_config()), "attempt": attempt}
    if _pending() and flush(quiet=True)[1]:     # e.g. this run's `start` is still spooled: keep the order
        _spool_put(item, p)
        return {"run": run, "name": name, "spooled": True}
    data = p.read_bytes()
    # Uploads are idempotent (same run+name overwrites): retry briefly, then spool the file so a hub
    # outage never fails a run that already did its work. Invalid requests (4xx) still raise.
    for attempt in range(3):
        try:
            return _call("PUT", f"/api/v1/artifacts?{q}", raw=data, ctype=ctype, timeout=600)
        except HubError as e:
            if not _retryable(e):
                raise
            if attempt == 2:
                _spool_put(item, p)
                print(f"swarm-report: hub unavailable, {name} spooled locally and will be uploaded ({e})", file=sys.stderr)
                return {"run": run, "name": name, "spooled": True}
            time.sleep(3 * (attempt + 1))


def download(url: str, dest: str | Path) -> Path:
    """Fetch an artifact (`/a/<run>/<name>`, as listed by get_run) to a local file."""
    cfg = _config()
    base, token = cfg.get("SWARM_HUB_URL", "").rstrip("/"), cfg.get("SWARM_HUB_TOKEN", "")
    if not base or not token:
        raise HubError("SWARM_HUB_URL / SWARM_HUB_TOKEN not set (see /etc/swarm/report.env)")
    req = urllib.request.Request(base + url if url.startswith("/") else url, headers={"Authorization": f"Bearer {token}"})
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
            shutil.copyfileobj(r, f)
    except urllib.error.HTTPError as e:
        raise HubError(f"GET {url}: {e.code}") from None
    return dest


class Run:
    """One run. Use as a context manager: start on enter, done on clean exit, fail on exception."""

    def __init__(self, run: str, experiment: str, params: dict, attempt: int | None = None):
        self.id, self.experiment, self.params = run, experiment, params
        self.attempt = attempt          # which assignment of this run we are; reports carry it (fencing)
        self._started = False
        self._finished = False
        self._last = 0.0
        self._alive = threading.Event()

    def __repr__(self):
        return f"Run({self.id!r}, params={self.params!r})"

    def _start(self, message=None):
        if not self._started:
            report("start", self.experiment, self.id, params=self.params, message=message, attempt=self.attempt)
            self._started = True
            threading.Thread(target=self._keepalive, daemon=True, name=f"swarm-heartbeat-{self.id}").start()

    def _keepalive(self):
        """Every minute while the run is open: tells the hub this worker is alive, so a long silent
        step is never mistaken for a dead worker and re-queued (hub LEASE is 20 minutes)."""
        while not self._alive.wait(HEARTBEAT_EVERY):
            report("heartbeat", self.experiment, self.id, attempt=self.attempt)

    def __enter__(self):
        self._start()
        return self

    def __exit__(self, et, ev, tb):
        if not self._finished:
            if et is None:
                self.done()
            else:
                self.fail(f"{et.__name__}: {ev}")
        return False

    def progress(self, step=None, total=None, message=None, force=False, **metrics):
        now = time.time()
        if not force and now - self._last < 2 and (total is None or step != total):
            return False
        self._last = now
        return report("progress", self.experiment, self.id, step=step, total=total, message=message,
                      metrics=metrics or None, attempt=self.attempt)

    def metric(self, **metrics):
        return report("metric", self.experiment, self.id, metrics=metrics, attempt=self.attempt)

    def log(self, message):
        return report("log", self.experiment, self.id, message=message, attempt=self.attempt)

    def artifact(self, path, name=None):
        return upload(self.id, path, name, attempt=self.attempt)

    def done(self, message=None, **metrics):
        self._finished = True
        self._alive.set()
        return report("done", self.experiment, self.id, message=message, metrics=metrics or None, attempt=self.attempt)

    def fail(self, message=None, **metrics):
        self._finished = True
        self._alive.set()
        return report("fail", self.experiment, self.id, message=message, metrics=metrics or None, attempt=self.attempt)


# ---------------------------------------------------------------- host heartbeat

def host_stats() -> dict:
    d = {}
    try:
        d["load"] = [round(x, 2) for x in os.getloadavg()]
        d["cpus"] = os.cpu_count()
    except OSError:
        pass
    try:
        mem = dict(line.split(":", 1) for line in Path("/proc/meminfo").read_text().splitlines())
        tot = int(mem["MemTotal"].split()[0]) / 1048576
        avail = int(mem["MemAvailable"].split()[0]) / 1048576
        d["mem_gb"], d["mem_used_gb"] = round(tot, 1), round(tot - avail, 1)
    except (OSError, KeyError, ValueError):
        pass
    spools = [p for p in {*Path("/home").glob("*/.cache/swarm/spool"), Path("/root/.cache/swarm/spool"), _spool_dir()}
              if p.is_dir()]
    items = [f for d in spools for f in _pending(d)]
    d["spool_items"] = len(items)
    if items:
        try:
            d["spool_oldest_s"] = int(time.time() - min(f.stat().st_mtime for f in items))
        except OSError:
            pass
    du = shutil.disk_usage("/")
    d["disk_gb"], d["disk_used_gb"] = round(du.total / 1e9), round(du.used / 1e9)
    for cmd, key in ((["who"], "users"), (["docker", "ps", "-q"], "containers"),
                     (["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total",
                       "--format=csv,noheader,nounits"], "gpus")):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        except (OSError, subprocess.SubprocessError):
            continue
        if r.returncode:
            continue
        if key == "users":
            d[key] = sorted({w.split()[0] for w in r.stdout.splitlines() if w.strip()})
        elif key == "containers":
            d[key] = len(r.stdout.split())
        else:
            d[key] = [[float(x) for x in line.split(",")] for line in r.stdout.strip().splitlines()]
    return d


# ---------------------------------------------------------------- CLI

def _val(s: str):
    for f in (int, float):
        try:
            return f(s)
        except ValueError:
            pass
    return {"true": True, "false": False}.get(s.lower(), s)


def _kv(items, what):
    out = {}
    for it in items:
        k, sep, v = it.partition("=")
        if not sep:
            raise SystemExit(f"{what} {it!r}: use name=value")
        out[k] = v
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="swarm-report", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, need_run=False):
        p.add_argument("-e", "--experiment")
        p.add_argument("-r", "--run", required=need_run)
        p.add_argument("-m", "--message")
        p.add_argument("-M", "--metric", action="append", default=[], help="name=value (number), repeatable")
        p.add_argument("--step", type=float)
        p.add_argument("--total", type=float)
        p.add_argument("--progress", type=float)
        p.add_argument("-p", "--param", action="append", default=[], help="name=value, repeatable (start)")
        p.add_argument("--url")
        p.add_argument("--status")
        p.add_argument("--role", choices=["coordinator", "worker", "server", "human"])
        p.add_argument("--strict", action="store_true")

    for k in ("plan", "start", "progress", "metric", "log", "done", "fail"):
        common(sub.add_parser(k))
    pz = sub.add_parser("pause", help="EMERGENCY STOP: no new runs (all experiments, or -e one); running runs finish")
    pz.add_argument("-e", "--experiment")
    pz.add_argument("-m", "--message", help="why (shown on the dashboard)")
    rz = sub.add_parser("resume", help="undo pause (all, or -e one)")
    rz.add_argument("-e", "--experiment")
    fl = sub.add_parser("flush", help="replay spooled reports and uploads now")
    fl.add_argument("--all", action="store_true", help="every user's spool on this server (root timer)")
    hb = sub.add_parser("heartbeat")
    hb.add_argument("--strict", action="store_true")
    hb.add_argument("--server", action="store_true", help="sent by the server's own timer: counts for /healthz/fleet")
    rg = sub.add_parser("register")
    rg.add_argument("file", help="experiment.yaml or .json with id, title, description, params, metrics, primary_metric")
    eq = sub.add_parser("enqueue")
    eq.add_argument("-e", "--experiment", required=True)
    eq.add_argument("-p", "--param", action="append", default=[], help="fixed name=value")
    eq.add_argument("--grid", action="append", default=[], help="name=v1,v2,... ; the cross product is queued")
    eq.add_argument("--repeat", type=int, default=1, help="queue each combination N times (seeds)")
    eq.add_argument("--priority", type=int, default=0)
    nx = sub.add_parser("next")
    nx.add_argument("-e", "--experiment")
    af = sub.add_parser("artifact")
    af.add_argument("-r", "--run", required=True)
    af.add_argument("path")
    af.add_argument("--name")
    ls = sub.add_parser("runs")
    ls.add_argument("-e", "--experiment")
    ls.add_argument("--status")
    sh = sub.add_parser("show")
    sh.add_argument("run")
    a = ap.parse_args(argv)

    try:
        if a.cmd == "pause":
            print(json.dumps(pause(a.experiment, a.message)))
            return 0
        if a.cmd == "resume":
            print(json.dumps(resume(a.experiment)))
            return 0
        if a.cmd == "flush":
            dirs = [_spool_dir()]
            if a.all:
                dirs = sorted({*Path("/home").glob("*/.cache/swarm/spool"), Path("/root/.cache/swarm/spool"), *dirs})
            sent, left = flush([d for d in dirs if d.is_dir()], quiet=True)
            print(f"flushed {sent}, waiting {left}")
            return 0 if not left else 1
        if a.cmd == "heartbeat":
            ok = report("heartbeat", data={**host_stats(), **({"_server": True} if a.server else {})}, strict=a.strict)
            return 0 if ok or not a.strict else 1
        if a.cmd == "register":
            text = Path(a.file).read_text()
            if a.file.endswith((".yaml", ".yml")):
                try:
                    import yaml  # type: ignore
                except ImportError:
                    raise SystemExit("PyYAML needed for .yaml (pip install pyyaml) or use .json")
                spec = yaml.safe_load(text)
            else:
                spec = json.loads(text)
            spec = {**spec, "experiment": spec.get("id")}
            print(json.dumps(register(spec.pop("experiment"), **{k: spec.get(k) for k in (
                "title", "description", "params", "metrics", "primary_metric", "owner", "url")})))
            return 0
        if a.cmd == "enqueue":
            fixed = {k: _val(v) for k, v in _kv(a.param, "param").items()}
            grid = {k: [_val(x) for x in v.split(",")] for k, v in _kv(a.grid, "grid").items()}
            combos = [dict(zip(grid, vals)) for vals in itertools.product(*grid.values())] if grid else [{}]
            plist = [{**fixed, **c, **({"repeat": i} if a.repeat > 1 else {})} for c in combos for i in range(a.repeat)]
            ids = enqueue(a.experiment, plist, priority=a.priority)
            print(f"queued {len(ids)} run(s) for {a.experiment}")
            for i in ids:
                print(i)
            return 0
        if a.cmd == "next":
            r = next_run(a.experiment)
            if not r:
                print("null")
                return 3
            print(json.dumps({"run": r.id, "experiment": r.experiment, "params": r.params}))
            return 0
        if a.cmd == "artifact":
            print(json.dumps(upload(a.run, a.path, a.name)))
            return 0
        if a.cmd == "runs":
            for r in runs(a.experiment, a.status):
                print(f"{r['run']:<40} {r['status']:<9} {json.dumps(r.get('params') or {})}  {json.dumps(r.get('metrics') or {})}")
            return 0
        if a.cmd == "show":
            print(json.dumps(get_run(a.run), indent=2))
            return 0
    except HubError as e:
        print(f"swarm-report: {e}", file=sys.stderr)
        return 1

    if not a.experiment and not a.run:
        ap.error("--experiment or --run is required")
    metrics = {}
    for k, v in _kv(a.metric, "metric").items():
        try:
            metrics[k] = float(v)
        except ValueError:
            ap.error(f"metric {k}: value must be a number")
    params = {k: _val(v) for k, v in _kv(a.param, "param").items()} or None
    ok = report(a.cmd, a.experiment, a.run, message=a.message, step=a.step, total=a.total, progress=a.progress,
                metrics=metrics or None, url=a.url, status=a.status, params=params, role=a.role, strict=a.strict)
    return 0 if ok or not a.strict else 1


if __name__ == "__main__":
    sys.exit(main())
