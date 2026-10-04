#!/usr/bin/env python3
"""swarm hub: experiments, runs, a run queue, artifacts and progress for the whole team.

Standard library only (Python 3.9+). SQLite + a directory of artifact files.
The contract is docs/REPORTING.md; hub/swarm_report.py is the client.

  Experiments  POST /api/v1/experiments          register/update an experiment type (params schema, metrics)
               GET  /api/v1/experiments
  Runs         POST /api/v1/runs                 enqueue planned runs (one object or a list): the task queue
               POST /api/v1/runs/next            a worker atomically takes the next planned run
               GET  /api/v1/runs                 ?experiment=&status=&limit=
               GET  /api/v1/runs/<run>           params, metrics, series, artifacts, events
  Progress     POST /api/v1/report               events: start/progress/metric/log/done/fail/heartbeat/claim/release
  Artifacts    PUT  /api/v1/artifacts?run=&name= raw bytes (Content-Type kept)
               GET  /a/<run>/<name>              download / render
  Dashboard    GET  /api/v1/state, GET /
  Pause        POST /api/v1/pause {experiment?, reason}  stop new assignments (all, or one experiment)
               POST /api/v1/resume {experiment?}          GET /api/v1/pause
  Health       GET  /healthz (no auth: DB write, disk, backup age), GET /healthz/fleet (hosts + spools)

Auth: `Authorization: Bearer <team token>` (or the swarm_token cookie the dashboard sets).
The optional read token (SWARM_HUB_READ_TOKEN) is for the public site's proxy: GET only, image and
frame.json/replay.json artifacts only, and rate limited as one client.

    SWARM_HUB_TOKEN=... [SWARM_HUB_READ_TOKEN=...] python3 hub.py --data ./hubdata --port 8700
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import mimetypes
import os
import re
import sqlite3
import threading
import time
import uuid
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

KINDS = {"plan", "start", "progress", "metric", "log", "artifact", "done", "fail", "heartbeat", "claim", "release"}
ROLES = {"coordinator", "worker", "server", "human"}
STATUSES = {"planned", "assigned", "running", "done", "failed", "cancelled"}
TERMINAL = {"done", "failed", "cancelled"}
STALE_AFTER = 600          # running/assigned with no event for this long: shown as stale
LEASE = int(os.environ.get("SWARM_HUB_LEASE", 1200))               # a QUEUED run with no report or heartbeat for this long goes back in the queue
MAX_ATTEMPTS = 3           # ...at most this many times; then it is failed, with the reason
REAP_EVERY = int(os.environ.get("SWARM_HUB_REAP_EVERY", 60))
BACKUP_MAX_AGE = 45 * 60          # off-box backup runs every 15 min
RESTORE_MAX_AGE = 26 * 3600       # restore check runs daily
HOST_DOWN_AFTER = 5 * 60          # heartbeats run every minute
SPOOL_MAX_AGE = 10 * 60
STARTED = time.time()
HOST_STALE_AFTER = 180
MAX_JSON = 2_000_000
MAX_ARTIFACT = 512 * 1024 * 1024
READ_RATE, READ_BURST = 10.0, 40   # read-token requests per second, and the burst allowed
READ_ARTIFACT_TYPES = ("image/png", "image/jpeg", "image/webp", "image/gif")
READ_ARTIFACT_NAMES = ("frame.json", "replay.json")

# A public live site (a proxy holding the read token) reads /api/v1/public/state: the state, already reduced to the
# fields the site shows, with IP addresses masked, so the Cloudflare function can pass the bytes through
# without parsing them (it ran out of CPU parsing a 1.4 MB state). Built at most every PUBLIC_TTL seconds.
PUBLIC_TTL = 2.0
PUBLIC_FEED_KINDS = "plan,start,done,fail,claim,release,log"
PUBLIC_RUN_KEYS = ("run", "experiment", "params", "tags", "status", "stale", "progress", "step", "total", "metrics",
                   "message", "source", "host", "created", "started", "ended", "updated", "series", "series_metric")
PUBLIC_EVENT_KEYS = ("id", "ts", "kind", "experiment", "run", "source", "host", "status", "message", "step", "total",
                     "progress", "metrics")
PUBLIC_HOST_KEYS = ("host", "online", "updated", "load", "cpus", "mem_gb", "mem_used_gb", "disk_gb", "disk_used_gb",
                    "users", "containers", "gpus")
PUBLIC_EXP_KEYS = ("id", "title", "description", "owner", "params", "metrics", "primary_metric", "url", "created",
                   "updated", "counts")
PUBLIC_CLAIM_KEYS = ("id", "servers", "by", "status", "until", "note", "experiment", "updated")
_IPV4 = re.compile(r"\b(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}\b")
_IPV6 = re.compile(r"\b(?:[0-9a-f]{1,4}:){3,7}[0-9a-f]{1,4}\b|\b(?:[0-9a-f]{1,4}:)+:(?:[0-9a-f]{1,4}:?)*\b", re.I)


def scrub(v):
    """Mask anything shaped like an IPv4 or IPv6 address in every string, keys included."""
    if isinstance(v, str):
        return _IPV6.sub("[ip]", _IPV4.sub("[ip]", v))
    if isinstance(v, list):
        return [scrub(x) for x in v]
    if isinstance(v, dict):
        return {scrub(k): scrub(x) for k, x in v.items()}
    return v


def _pick(d: dict, keys) -> dict:
    return {k: d[k] for k in keys if d.get(k) is not None}


def _public_artifacts(arts) -> list:
    return [{"name": a["name"], "content_type": a["content_type"], "size": a["size"], "url": "/api" + a["url"]}
            for a in arts or [] if a["content_type"] in READ_ARTIFACT_TYPES or Path(a["name"]).name in READ_ARTIFACT_NAMES]


def _public_run(r: dict) -> dict:
    out = _pick(r, PUBLIC_RUN_KEYS)
    url = r.get("url")
    if isinstance(url, str) and url.startswith("https://github.com/"):   # a run's own plan document
        out["url"] = url
    out["artifacts"] = _public_artifacts(r.get("artifacts"))
    return out
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,199}$")

SCHEMA = """
CREATE TABLE IF NOT EXISTS experiments (
  id TEXT PRIMARY KEY, title TEXT, description TEXT, owner TEXT, params TEXT, metrics TEXT,
  primary_metric TEXT, url TEXT, created REAL, updated REAL
);
CREATE TABLE IF NOT EXISTS runs (
  run TEXT PRIMARY KEY, experiment TEXT NOT NULL, params TEXT, tags TEXT, priority INTEGER DEFAULT 0,
  source TEXT, role TEXT, host TEXT, status TEXT, progress REAL, step REAL, total REAL,
  metrics TEXT, message TEXT, url TEXT, created REAL, started REAL, ended REAL, updated REAL
);
CREATE INDEX IF NOT EXISTS runs_queue ON runs(experiment, status, priority DESC, created);
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts REAL NOT NULL, received REAL NOT NULL,
  experiment TEXT, run TEXT, source TEXT, role TEXT, host TEXT, kind TEXT NOT NULL,
  status TEXT, message TEXT, progress REAL, step REAL, total REAL, metrics TEXT, data TEXT, url TEXT
);
CREATE INDEX IF NOT EXISTS events_run ON events(run, id);
CREATE TABLE IF NOT EXISTS artifacts (
  run TEXT NOT NULL, name TEXT NOT NULL, experiment TEXT, content_type TEXT, size INTEGER, sha256 TEXT,
  source TEXT, created REAL, PRIMARY KEY (run, name)
);
CREATE TABLE IF NOT EXISTS hosts (host TEXT PRIMARY KEY, updated REAL, data TEXT);
CREATE TABLE IF NOT EXISTS pauses (scope TEXT PRIMARY KEY, reason TEXT, by TEXT, since REAL);
CREATE TABLE IF NOT EXISTS assign_requests (request_id TEXT PRIMARY KEY, run TEXT, ts REAL);
CREATE TABLE IF NOT EXISTS health_probe (id INTEGER PRIMARY KEY, ts REAL);
CREATE TABLE IF NOT EXISTS claims (
  id TEXT PRIMARY KEY, servers TEXT, by TEXT, status TEXT, until TEXT, note TEXT, experiment TEXT, updated REAL
);
"""


def jload(s, default=None):
    return json.loads(s) if s else default


def check_name(v: str, what: str) -> str:
    if not isinstance(v, str) or not NAME_RE.match(v) or ".." in v:
        raise ValueError(f"{what} must match {NAME_RE.pattern} (no '..')")
    return v


class Store:
    def __init__(self, data_dir: Path):
        self.dir = data_dir
        (data_dir / "artifacts").mkdir(parents=True, exist_ok=True)
        self._path = str(data_dir / "hub.db")
        self._local = threading.local()
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript(SCHEMA)
        self.lock = threading.Lock()
        self.public_lock = threading.Lock()
        self.public_cache = None
        self._migrate()

    @property
    def db(self) -> sqlite3.Connection:
        """One connection per thread. Sharing a single connection across request threads let a read
        (e.g. /api/v1/state) interleave with a write and return corrupted rows.
        WAL lets readers run beside the writer; writes are still serialized by self.lock, and every
        connection waits up to 15 s for a lock (Litestream checkpoints) instead of failing at once."""
        c = getattr(self._local, "conn", None)
        if c is None:
            c = sqlite3.connect(self._path, timeout=15)
            c.row_factory = sqlite3.Row
            c.execute("PRAGMA busy_timeout=15000")
            self._local.conn = c
        return c

    def _migrate(self):
        """Additive schema changes for hubs created by an earlier version."""
        cols = {r["name"] for r in self.db.execute("PRAGMA table_info(runs)")}
        with self.db:
            if "queued" not in cols:
                self.db.execute("ALTER TABLE runs ADD COLUMN queued INTEGER DEFAULT 0")
                # runs that came from the queue have a plan event; ad-hoc runs do not
                self.db.execute("UPDATE runs SET queued=1 WHERE run IN (SELECT run FROM events WHERE kind='plan')")
            if "attempts" not in cols:
                self.db.execute("ALTER TABLE runs ADD COLUMN attempts INTEGER DEFAULT 0")
                self.db.execute("UPDATE runs SET attempts=1 WHERE queued=1 AND status!='planned'")

    def reap(self) -> list:
        """Leases: a queued run whose worker went silent (crash, OOM, reboot, lost network) for LEASE
        seconds goes back in the queue so another worker runs it; after MAX_ATTEMPTS it is failed.
        Workers using swarm_report >= this version heartbeat every minute, so long silent steps are safe."""
        now = time.time()
        changed = []
        with self.lock, self.db:
            rows = self.db.execute(
                "SELECT run, experiment, attempts, host, source FROM runs WHERE queued=1"
                " AND status IN ('assigned','running') AND updated < ?", (now - LEASE,)).fetchall()
            for r in rows:
                n = r["attempts"] or 1
                if n < MAX_ATTEMPTS:
                    msg = (f"requeued: no report or heartbeat from {r['source']} on {r['host']} for "
                           f"{LEASE // 60} min (attempt {n} of {MAX_ATTEMPTS})")
                    self.db.execute("UPDATE runs SET status='planned', progress=NULL, step=NULL, message=?, updated=?"
                                    " WHERE run=?", (msg, now, r["run"]))
                    self._event(now, {"kind": "log", "experiment": r["experiment"], "run": r["run"],
                                      "status": "planned", "message": msg, "source": "hub"}, "server")
                else:
                    msg = f"failed: worker went silent on {MAX_ATTEMPTS} attempts (lease {LEASE // 60} min)"
                    self.db.execute("UPDATE runs SET status='failed', ended=?, message=?, updated=? WHERE run=?",
                                    (now, msg, now, r["run"]))
                    self._event(now, {"kind": "fail", "experiment": r["experiment"], "run": r["run"],
                                      "message": msg, "source": "hub"}, "server")
                changed.append(r["run"])
        return changed

    # ------------------------------------------------------------ experiments
    def upsert_experiment(self, e: dict) -> dict:
        eid = check_name(e.get("id") or e.get("experiment"), "experiment id")
        now = time.time()
        with self.lock, self.db:
            row = self.db.execute("SELECT * FROM experiments WHERE id=?", (eid,)).fetchone()
            vals = {
                "title": e.get("title") or (row["title"] if row else eid),
                "description": e.get("description") if "description" in e else (row["description"] if row else None),
                "owner": e.get("owner") or (row["owner"] if row else None),
                "params": json.dumps(e["params"]) if "params" in e else (row["params"] if row else None),
                "metrics": json.dumps(e["metrics"]) if "metrics" in e else (row["metrics"] if row else None),
                "primary_metric": e.get("primary_metric") or (row["primary_metric"] if row else None),
                "url": e.get("url") or (row["url"] if row else None),
                "created": row["created"] if row else now,
                "updated": now,
            }
            self.db.execute(
                f"INSERT OR REPLACE INTO experiments (id,{','.join(vals)}) VALUES (?,{','.join('?' * len(vals))})",
                (eid, *vals.values()))
        return {"id": eid}

    def _ensure_experiment(self, eid: str):
        if not self.db.execute("SELECT 1 FROM experiments WHERE id=?", (eid,)).fetchone():
            now = time.time()
            self.db.execute("INSERT INTO experiments (id, title, created, updated) VALUES (?,?,?,?)", (eid, eid, now, now))

    # ------------------------------------------------------------ emergency pause
    def paused_scopes(self) -> set:
        return {r["scope"] for r in self.db.execute("SELECT scope FROM pauses")}

    def pause(self, scope: str, reason: str | None, by: str | None) -> dict:
        """Stop handing out new runs (scope '*' = everything, or one experiment id). Runs in progress
        finish normally; idle workers wait instead of exiting. Undo with resume()."""
        if scope != "*":
            check_name(scope, "experiment")
        now = time.time()
        with self.lock, self.db:
            self.db.execute("INSERT OR REPLACE INTO pauses VALUES (?,?,?,?)", (scope, reason, by, now))
            self._event(now, {"kind": "log", "experiment": None if scope == "*" else scope, "source": by,
                              "message": f"PAUSED {'all experiments' if scope == '*' else scope}: {reason or ''}"}, "human")
        return self.pauses()

    def resume(self, scope: str, by: str | None) -> dict:
        now = time.time()
        with self.lock, self.db:
            if scope == "all":
                self.db.execute("DELETE FROM pauses")
            else:
                self.db.execute("DELETE FROM pauses WHERE scope=?", (scope,))
            self._event(now, {"kind": "log", "experiment": None if scope in ("*", "all") else scope, "source": by,
                              "message": f"RESUMED {scope}"}, "human")
        return self.pauses()

    def pauses(self) -> dict:
        return {"paused": [dict(r) for r in self.db.execute("SELECT * FROM pauses ORDER BY since")]}

    def health(self) -> dict:
        """What the uptime check calls. Fails (503) on a stuck DB, a nearly full disk, or stalled backups."""
        out, ok = {}, True
        try:
            with self.lock, self.db:
                self.db.execute("INSERT OR REPLACE INTO health_probe (id, ts) VALUES (1, ?)", (time.time(),))
            out["db"] = "ok"
        except sqlite3.Error as e:
            out["db"], ok = f"error: {e}", False
        st = os.statvfs(self.dir)
        free = st.f_bavail * st.f_frsize / (st.f_blocks * st.f_frsize)
        out["disk_free_pct"] = round(free * 100, 1)
        if free < 0.10:
            ok = False
        for name, limit in (("backup", BACKUP_MAX_AGE), ("restore_check", RESTORE_MAX_AGE)):
            f = self.dir / "backup" / f"last_{name}_ok"
            if f.exists():
                age = time.time() - f.stat().st_mtime
                out[f"{name}_age_min"] = round(age / 60, 1)
                if age > limit:
                    ok = False
            elif time.time() - STARTED > limit:
                out[f"{name}_age_min"] = None
                ok = False
        out["ok"] = ok
        return out

    def fleet_health(self) -> dict:
        """A second uptime check. Fails if a host that reported in the last day is now silent, or if a
        host has had reports spooled (hub unreachable from it) for more than SPOOL_MAX_AGE."""
        now, problems = time.time(), []
        for h in self.db.execute("SELECT host, updated, data FROM hosts WHERE updated > ?", (now - 86400,)):
            d = jload(h["data"], {})
            if not d.get("_server"):
                continue        # only the servers' own timer (`swarm-report heartbeat --server`) counts; worker labels do not
            if now - h["updated"] > HOST_DOWN_AFTER:
                problems.append(f"{h['host']} silent for {int((now - h['updated']) / 60)} min")
            if (d.get("spool_oldest_s") or 0) > SPOOL_MAX_AGE:
                problems.append(f"{h['host']} has {d.get('spool_items')} report(s) spooled for "
                                f"{int(d['spool_oldest_s'] / 60)} min")
        return {"ok": not problems, "problems": problems}

    def experiments(self) -> list:
        out = []
        for r in self.db.execute("SELECT * FROM experiments ORDER BY updated DESC"):
            d = dict(r)
            d["params"], d["metrics"] = jload(d["params"], {}), jload(d["metrics"], [])
            out.append(d)
        return out

    # ------------------------------------------------------------ run queue
    def enqueue(self, r: dict) -> str:
        exp = check_name(r.get("experiment"), "experiment")
        run = r.get("run") or f"{exp}/{uuid.uuid4().hex[:8]}"
        check_name(run, "run")
        params = r.get("params") or {}
        if not isinstance(params, dict):
            raise ValueError("params must be an object")
        now = time.time()
        with self.lock, self.db:
            self._ensure_experiment(exp)
            if self.db.execute("SELECT 1 FROM runs WHERE run=?", (run,)).fetchone():
                raise ValueError(f"run {run} already exists")
            self.db.execute(
                "INSERT INTO runs (run, experiment, params, tags, priority, source, role, status, message, created, updated,"
                " queued, attempts) VALUES (?,?,?,?,?,?,?,?,?,?,?,1,0)",
                (run, exp, json.dumps(params), json.dumps(r.get("tags") or []), int(r.get("priority") or 0),
                 r.get("source"), "coordinator", "planned", r.get("message"), now, now))
            self._event(now, {"kind": "plan", "experiment": exp, "run": run, "source": r.get("source"),
                              "role": "coordinator", "data": {"params": params}})
        return run

    def next_run(self, req: dict):
        """Atomically hand the highest-priority, oldest planned run to a worker."""
        now = time.time()
        rid = req.get("request_id")
        if rid:
            # A retried request (lost response) gets the same run back instead of a second one.
            seen = self.db.execute("SELECT run FROM assign_requests WHERE request_id=?", (rid,)).fetchone()
            if seen:
                return self.run_detail(seen["run"], light=True) if seen["run"] else None
        paused = self.paused_scopes()
        if "*" in paused or (req.get("experiment") and req["experiment"] in paused):
            return {"paused": True}
        where, args = ["status='planned'"], []
        if paused:
            where.append(f"experiment NOT IN ({','.join('?' * len(paused))})")
            args.extend(sorted(paused))
        if req.get("experiment"):
            where.append("experiment=?")
            args.append(req["experiment"])
        with self.lock, self.db:
            row = self.db.execute(
                f"SELECT run FROM runs WHERE {' AND '.join(where)} ORDER BY priority DESC, created LIMIT 1", args).fetchone()
            if not row:
                return None
            if rid:
                self.db.execute("INSERT OR REPLACE INTO assign_requests VALUES (?,?,?)", (rid, row["run"], now))
                self.db.execute("DELETE FROM assign_requests WHERE ts < ?", (now - 86400,))
            self.db.execute("UPDATE runs SET status='assigned', source=?, host=?, role='worker', updated=?,"
                            " attempts=COALESCE(attempts,0)+1 WHERE run=?",
                            (req.get("source"), req.get("host"), now, row["run"]))
            self._event(now, {"kind": "log", "run": row["run"], "source": req.get("source"), "host": req.get("host"),
                              "message": "assigned", "status": "assigned"})
        return self.run_detail(row["run"], light=True)

    # ------------------------------------------------------------ events
    def ingest(self, ev: dict) -> int:
        kind = ev.get("kind")
        if kind not in KINDS:
            raise ValueError(f"kind must be one of {sorted(KINDS)}")
        role = ev.get("role") or ("server" if kind == "heartbeat" and not ev.get("experiment") else "worker")
        if role not in ROLES:
            raise ValueError(f"role must be one of {sorted(ROLES)}")
        if ev.get("metrics") is not None and not isinstance(ev["metrics"], dict):
            raise ValueError("metrics must be an object of name -> number")
        now = time.time()
        if kind == "heartbeat" and ev.get("run"):
            # A worker's per-run keepalive: extends the lease, writes no event (keeps the feed quiet).
            with self.lock, self.db:
                self.db.execute("UPDATE runs SET updated=? WHERE run=? AND status IN ('assigned','running')",
                                (now, ev["run"]))
            return 0
        with self.lock, self.db:
            if kind == "heartbeat" and not ev.get("experiment") and not ev.get("run"):
                if ev.get("host"):
                    self.db.execute("INSERT OR REPLACE INTO hosts (host, updated, data) VALUES (?,?,?)",
                                    (ev["host"], now, json.dumps(ev.get("data") or {})))
                return self._event(now, ev, role)
            if kind in ("claim", "release"):
                d = ev.get("data") or {}
                cid = d.get("id") or ev.get("run")
                if cid:
                    self.db.execute(
                        "INSERT OR REPLACE INTO claims (id, servers, by, status, until, note, experiment, updated)"
                        " VALUES (?,?,?,?,?,?,?,?)",
                        (cid, json.dumps(d.get("servers") or []), ev.get("source"),
                         ev.get("status") or ("running" if kind == "claim" else "done"), d.get("until"),
                         ev.get("message"), d.get("experiment"), now))
                return self._event(now, {**ev, "run": None}, role)
            run = ev.get("run")
            exp = ev.get("experiment")
            if run and not exp:
                row = self.db.execute("SELECT experiment FROM runs WHERE run=?", (run,)).fetchone()
                exp = row["experiment"] if row else None
            if not exp:
                raise ValueError("experiment is required (or a run that already exists)")
            check_name(exp, "experiment")
            run = check_name(run or exp, "run")
            ev = {**ev, "experiment": exp, "run": run}
            self._ensure_experiment(exp)
            if self._superseded(run, ev.get("attempt")):
                ev = {**ev, "status": "superseded",
                      "message": f"[superseded attempt {ev['attempt']}] " + (ev.get("message") or "")}
                return self._event(now, ev, role)
            self._update_run(ev, kind, now)
            return self._event(now, ev, role)

    def _superseded(self, run, attempt) -> bool:
        if attempt is None:
            return False
        row = self.db.execute("SELECT attempts FROM runs WHERE run=?", (run,)).fetchone()
        try:
            return bool(row and row["attempts"] and int(attempt) < int(row["attempts"]))
        except (TypeError, ValueError):
            return False

    def _event(self, now, ev, role=None) -> int:
        prog, step, total = _progress(ev)
        cur = self.db.execute(
            "INSERT INTO events (ts, received, experiment, run, source, role, host, kind, status, message,"
            " progress, step, total, metrics, data, url) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (float(ev.get("ts") or now), now, ev.get("experiment"), ev.get("run"), ev.get("source"),
             role or ev.get("role"), ev.get("host"), ev["kind"], ev.get("status"), ev.get("message"),
             prog, step, total, json.dumps(ev["metrics"]) if ev.get("metrics") else None,
             json.dumps(ev["data"]) if ev.get("data") else None, ev.get("url")))
        return cur.lastrowid

    def _update_run(self, ev, kind, now):
        run = ev["run"]
        row = self.db.execute("SELECT * FROM runs WHERE run=?", (run,)).fetchone()
        prog, step, total = _progress(ev)
        status = ev.get("status")
        if status is None:
            status = {"plan": "planned", "start": "running", "done": "done", "fail": "failed"}.get(kind)
        if status is None:
            status = "running" if (row is None or row["status"] in ("planned", "assigned")) and kind in ("progress", "metric") \
                else (row["status"] if row else "running")
        if status not in STATUSES:
            raise ValueError(f"status must be one of {sorted(STATUSES)}")
        metrics = jload(row["metrics"], {}) if row else {}
        metrics.update(ev.get("metrics") or {})
        params = jload(row["params"], {}) if row else {}
        params.update((ev.get("data") or {}).get("params") or {})
        g = (lambda k, d=None: row[k] if row and row[k] is not None else d)
        vals = {
            "experiment": ev["experiment"],
            "params": json.dumps(params),
            "tags": g("tags", "[]"),
            "priority": g("priority", 0),
            "source": ev.get("source") or g("source"),
            "role": ev.get("role") or g("role", "worker"),
            "host": ev.get("host") or g("host"),
            "status": status,
            "progress": 1.0 if kind == "done" else (prog if prog is not None else g("progress")),
            "step": (total or g("total")) if kind == "done" and (total or g("total")) else (step if step is not None else g("step")),
            "total": total if total is not None else g("total"),
            "metrics": json.dumps(metrics) if metrics else None,
            "message": ev.get("message") or g("message"),
            "url": ev.get("url") or g("url"),
            "created": g("created", now),
            "started": g("started") or (now if status == "running" else None),
            "ended": now if status in TERMINAL else None,
            "updated": now,
        }
        self.db.execute(
            f"INSERT INTO runs (run,{','.join(vals)}) VALUES (?,{','.join('?' * len(vals))})"
            f" ON CONFLICT(run) DO UPDATE SET {','.join(f'{k}=excluded.{k}' for k in vals)}",
            (run, *vals.values()))

    # ------------------------------------------------------------ artifacts
    def artifact_path(self, run: str, name: str) -> Path:
        return self.dir / "artifacts" / check_name(run, "run") / check_name(name, "artifact name")

    def put_artifact(self, run, name, ctype, stream, length, source, attempt=None) -> dict:
        if length > MAX_ARTIFACT:
            raise ValueError(f"artifact larger than {MAX_ARTIFACT >> 20} MB")
        row = self.db.execute("SELECT experiment FROM runs WHERE run=?", (run,)).fetchone()
        if not row:
            raise ValueError(f"unknown run {run}; report `start` (or enqueue it) first")
        if self._superseded(run, attempt):
            name = f"attempt-{int(attempt)}/{name}"     # never overwrite the current attempt's files
        path = self.artifact_path(run, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(path.name + ".part")
        h, left = hashlib.sha256(), length
        with open(tmp, "wb") as f:
            while left > 0:
                chunk = stream.read(min(1 << 20, left))
                if not chunk:
                    break
                f.write(chunk)
                h.update(chunk)
                left -= len(chunk)
        if left:
            tmp.unlink(missing_ok=True)
            raise ValueError("upload ended early")
        tmp.replace(path)
        ctype = ctype if ctype and ctype != "application/octet-stream" else (mimetypes.guess_type(name)[0] or "application/octet-stream")
        now = time.time()
        with self.lock, self.db:
            self.db.execute("INSERT OR REPLACE INTO artifacts VALUES (?,?,?,?,?,?,?,?)",
                            (run, name, row["experiment"], ctype, length, h.hexdigest(), source, now))
            self._event(now, {"kind": "artifact", "experiment": row["experiment"], "run": run, "source": source,
                              "message": name, "url": f"/a/{quote(run)}/{quote(name)}"})
            self.db.execute("UPDATE runs SET updated=? WHERE run=?", (now, run))
        return {"run": run, "name": name, "size": length, "sha256": h.hexdigest(), "url": f"/a/{quote(run)}/{quote(name)}"}

    def artifacts(self, run: str) -> list:
        return [{**dict(a), "url": f"/a/{quote(a['run'])}/{quote(a['name'])}"}
                for a in self.db.execute("SELECT * FROM artifacts WHERE run=? ORDER BY created", (run,))]

    # ------------------------------------------------------------ reads
    def events(self, q: dict) -> list:
        where, args = [], []
        for col in ("experiment", "run", "host", "source", "kind"):
            if q.get(col):
                where.append(f"{col}=?")
                args.append(q[col])
        if q.get("since"):
            where.append("id>?")
            args.append(int(q["since"]))
        if q.get("kinds"):
            ks = [k for k in q["kinds"].split(",") if k in KINDS]
            where.append(f"kind IN ({','.join('?' * len(ks))})" if ks else "0")
            args.extend(ks)
        limit = min(int(q.get("limit") or 100), 2000)
        sql = "SELECT * FROM events" + (" WHERE " + " AND ".join(where) if where else "") + " ORDER BY id DESC LIMIT ?"
        return [_clean(r) for r in self.db.execute(sql, (*args, limit))]

    def series(self, run: str, metric: str | None = None, limit: int = 1000) -> dict:
        out = {}
        for r in self.db.execute("SELECT ts, step, metrics FROM events WHERE run=? AND metrics IS NOT NULL ORDER BY id",
                                 (run,)):
            for k, v in json.loads(r["metrics"]).items():
                if isinstance(v, (int, float)) and (metric is None or k == metric):
                    out.setdefault(k, []).append([r["ts"], r["step"], v])
        return {k: v[-limit:] for k, v in out.items()}

    def _run_dict(self, r, now) -> dict:
        d = dict(r)
        for k, dflt in (("params", {}), ("tags", []), ("metrics", {})):
            d[k] = jload(d[k], dflt)
        if d["status"] in ("running", "assigned") and now - (d["updated"] or 0) > STALE_AFTER:
            d["stale"] = True
        return d

    def runs(self, q: dict) -> list:
        where, args = [], []
        for col in ("experiment", "status", "host", "source"):
            if q.get(col):
                where.append(f"{col}=?")
                args.append(q[col])
        limit = min(int(q.get("limit") or 200), 5000)
        sql = "SELECT * FROM runs" + (" WHERE " + " AND ".join(where) if where else "") + " ORDER BY updated DESC LIMIT ?"
        now = time.time()
        return [self._run_dict(r, now) for r in self.db.execute(sql, (*args, limit))]

    def run_detail(self, run: str, light=False):
        r = self.db.execute("SELECT * FROM runs WHERE run=?", (run,)).fetchone()
        if not r:
            return None
        d = self._run_dict(r, time.time())
        if not light:
            d["series"] = self.series(run)
            d["artifacts"] = self.artifacts(run)
            d["events"] = self.events({"run": run, "limit": 200})
        return d

    def public_state(self, since: float | None = None) -> bytes:
        """The live site's state as compact JSON, rebuilt at most every PUBLIC_TTL seconds.

        With `since` (the `now` of a response the client already has) only runs updated after it are sent,
        plus every experiment's metadata and counts, hosts, claims and the feed: a few KB instead of the
        whole state. Clients merge the runs into what they have.
        """
        with self.public_lock:
            if not (self.public_cache and time.monotonic() - self.public_cache[0] < PUBLIC_TTL):
                self.public_cache = self._build_public()
            _, full, body = self.public_cache
        if since is None:
            return body
        cut = since - 5      # overlap: a run written while the previous build ran is sent twice, never missed
        delta = {**full, "since": since,
                 "experiments": [{**e, "runs": [r for r in e["runs"] if (r.get("updated") or 0) > cut]}
                                 for e in full["experiments"]]}
        return json.dumps(delta, separators=(",", ":"), default=str).encode()

    def _build_public(self):
        d = self.state()
        out = {
            "now": d["now"],
            "hosts": [_pick(h, PUBLIC_HOST_KEYS) for h in d["hosts"]],
            "claims": [_pick(c, PUBLIC_CLAIM_KEYS) for c in d["claims"]],
            "experiments": [{**_pick(e, PUBLIC_EXP_KEYS), "runs": [_public_run(r) for r in e["runs"]]}
                            for e in d["experiments"]],
            "events": [_pick(e, PUBLIC_EVENT_KEYS) for e in self.events({"limit": 80, "kinds": PUBLIC_FEED_KINDS})],
        }
        out = scrub(out)
        return time.monotonic(), out, json.dumps(out, separators=(",", ":"), default=str).encode()

    def state(self) -> dict:
        now = time.time()
        exps = {e["id"]: {**e, "runs": [], "counts": {}} for e in self.experiments()}
        for r in self.db.execute("SELECT * FROM runs ORDER BY updated DESC LIMIT 2000"):
            d = self._run_dict(r, now)
            e = exps.setdefault(d["experiment"], {"id": d["experiment"], "title": d["experiment"], "params": {},
                                                  "metrics": [], "runs": [], "counts": {}, "updated": 0})
            st = "stale" if d.get("stale") else d["status"]
            e["counts"][st] = e["counts"].get(st, 0) + 1
            e["updated"] = max(e.get("updated") or 0, d["updated"] or 0)
            if len(e["runs"]) < 200:
                pm = e.get("primary_metric") or next((k for k, v in d["metrics"].items() if isinstance(v, (int, float))), None)
                d["series_metric"] = pm
                d["series"] = [p[2] for p in self.series(d["run"], pm, 60).get(pm, [])] if pm else []
                d["artifacts"] = [{"name": a["name"], "content_type": a["content_type"], "size": a["size"], "url": a["url"]}
                                  for a in self.artifacts(d["run"])]
                e["runs"].append(d)
        hosts = [{"host": h["host"], "updated": h["updated"], "online": now - h["updated"] < HOST_STALE_AFTER,
                  **jload(h["data"], {})} for h in self.db.execute("SELECT * FROM hosts ORDER BY host")]
        claims = []
        for c in self.db.execute("SELECT * FROM claims WHERE status IN ('planned','running') ORDER BY updated DESC"):
            claims.append({**dict(c), "servers": jload(c["servers"], [])})
        return {"now": now, "hosts": hosts, "claims": claims, "paused": self.pauses()["paused"],
                "experiments": sorted(exps.values(), key=lambda e: -(e.get("updated") or 0)),
                "events": [_clean(r) for r in self.db.execute(
                    "SELECT * FROM events WHERE kind != 'heartbeat' ORDER BY id DESC LIMIT 60")]}


def _progress(ev):
    prog, step, total = ev.get("progress"), ev.get("step"), ev.get("total")
    if isinstance(prog, dict):
        step, total, prog = prog.get("step"), prog.get("total"), None
    if prog is None and step is not None and total:
        prog = float(step) / float(total)
    return prog, step, total


def _clean(r) -> dict:
    d = dict(r)
    for k in ("metrics", "data"):
        d[k] = jload(d[k])
    return {k: v for k, v in d.items() if v is not None}


class ReadBucket:
    """Token bucket shared by every read-token request (they all come through one proxy)."""

    def __init__(self, rate: float, burst: int):
        self.rate, self.burst, self.level, self.t = rate, burst, float(burst), time.monotonic()
        self.lock = threading.Lock()

    def take(self) -> bool:
        with self.lock:
            now = time.monotonic()
            self.level = min(self.burst, self.level + (now - self.t) * self.rate)
            self.t = now
            if self.level < 1:
                return False
            self.level -= 1
            return True


class Handler(BaseHTTPRequestHandler):
    server_version = "swarm-hub/2"
    protocol_version = "HTTP/1.1"
    store: Store
    token: str
    read_token: str = ""
    read_bucket = ReadBucket(READ_RATE, READ_BURST)
    dashboard_path: Path

    def log_message(self, fmt, *args):
        if self.command != "GET":
            super().log_message(fmt, *args)

    def _send(self, code: int, body, ctype="application/json", extra=None):
        raw = body if isinstance(body, bytes) else json.dumps(body, default=str).encode()
        # A rejected POST/PUT may leave its body unread on the socket. Never reuse that
        # connection, or the leftover bytes become the start of the next request.
        if code >= 400 and self.command in ("POST", "PUT"):
            self.close_connection = True
            extra = {**(extra or {}), "Connection": "close"}
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(raw)

    def _access(self) -> str | None:
        """'team' for the team token, 'read' for the read token, else None (401 already sent)."""
        got = self.headers.get("Authorization", "")
        got = got[7:] if got.startswith("Bearer ") else self.headers.get("X-Swarm-Token", "")
        if not got and self.headers.get("Cookie"):
            c = SimpleCookie(self.headers["Cookie"]).get("swarm_token")
            got = unquote(c.value) if c else ""
        if self.token and got and hmac.compare_digest(got.encode(), self.token.encode()):
            return "team"
        if self.read_token and got and hmac.compare_digest(got.encode(), self.read_token.encode()):
            if self.command not in ("GET", "HEAD"):
                self._send(403, {"error": "read token is GET only"})
                return None
            if not self.read_bucket.take():
                self._send(429, {"error": "rate limited"}, extra={"Retry-After": "1"})
                return None
            return "read"
        self._send(401, {"error": "missing or wrong token"})
        return None

    def _authed(self) -> bool:
        """Writes: the team token only."""
        got = self._access()
        if got == "read":
            self._send(403, {"error": "read token is GET only"})
        return got == "team"

    def _json(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAX_JSON:
            raise ValueError("body too large")
        return json.loads(self.rfile.read(n) or b"null")

    def _source(self):
        return self.headers.get("X-Swarm-Source")

    def _guard(self, handler):
        """Any unexpected error becomes a 500 JSON answer instead of a dropped connection. Clients treat
        500 as retryable (spool + replay), so a hub bug never silently loses a report."""
        try:
            handler()
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            try:
                self._send(500, {"error": f"hub error: {type(e).__name__}"})
            except Exception:  # noqa: BLE001 - headers may already be on the wire
                self.close_connection = True

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        self._guard(self._do_GET)

    def _do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        path = u.path
        if path in ("/", "/index.html"):
            return self._send(200, self.dashboard_path.read_bytes(), "text/html; charset=utf-8")
        if path == "/healthz":                       # deep: DB write, disk, backup + restore-check age
            h = self.store.health()
            return self._send(200 if h["ok"] else 503, h)
        if path == "/healthz/fleet":                 # every host heartbeating, nothing stuck in a spool
            h = self.store.fleet_health()
            return self._send(200 if h["ok"] else 503, h)
        if not (path.startswith("/api/v1/") or path.startswith("/a/")):
            return self._send(404, {"error": "not found"})
        access = self._access()
        if not access:
            return
        try:
            if path.startswith("/a/"):
                return self._artifact(unquote(path[3:]), public=access == "read")
            if path == "/api/v1/state":
                return self._send(200, self.store.state())
            if path == "/api/v1/public/state":
                since = float(q["since"]) if q.get("since") else None
                return self._send(200, self.store.public_state(since))
            if path == "/api/v1/experiments":
                return self._send(200, self.store.experiments())
            if path == "/api/v1/pause":
                return self._send(200, self.store.pauses())
            if path == "/api/v1/runs":
                return self._send(200, self.store.runs(q))
            if path.startswith("/api/v1/runs/"):
                d = self.store.run_detail(unquote(path[len("/api/v1/runs/"):]))
                return self._send(200, d) if d else self._send(404, {"error": "no such run"})
            if path == "/api/v1/events":
                return self._send(200, self.store.events(q))
            if path == "/api/v1/series":
                return self._send(200, self.store.series(q.get("run", ""), q.get("metric")))
        except (ValueError, sqlite3.Error) as e:
            return self._send(400, {"error": str(e)})
        self._send(404, {"error": "not found"})

    def _artifact(self, rest: str, public: bool = False):
        run, _, name = rest.rpartition("/")
        # run ids may contain '/', names may not start a new run segment: look up the longest known run prefix
        parts = rest.split("/")
        for i in range(len(parts) - 1, 0, -1):
            cand_run, cand_name = "/".join(parts[:i]), "/".join(parts[i:])
            row = self.store.db.execute("SELECT content_type FROM artifacts WHERE run=? AND name=?",
                                        (cand_run, cand_name)).fetchone()
            if row:
                run, name = cand_run, cand_name
                break
        else:
            return self._send(404, {"error": "no such artifact"})
        if public and not (row["content_type"] in READ_ARTIFACT_TYPES or Path(name).name in READ_ARTIFACT_NAMES):
            return self._send(404, {"error": "no such artifact"})
        p = self.store.artifact_path(run, name)
        size = p.stat().st_size
        self.send_response(200)
        self.send_header("Content-Type", row["content_type"])
        self.send_header("Content-Length", str(size))
        self.send_header("Cache-Control", "private, max-age=3600")
        self.send_header("X-Content-Type-Options", "nosniff")
        # html/svg could run script on the hub origin; serve them as attachments
        if row["content_type"].startswith(("text/html", "image/svg")):
            self.send_header("Content-Disposition", f'attachment; filename="{Path(name).name}"')
        self.end_headers()
        if self.command == "HEAD":
            return
        with open(p, "rb") as f:
            while chunk := f.read(1 << 20):
                self.wfile.write(chunk)

    def do_PUT(self):
        self._guard(self._do_PUT)

    def _do_PUT(self):
        u = urlparse(self.path)
        if u.path != "/api/v1/artifacts":
            return self._send(404, {"error": "not found"})
        if not self._authed():
            return
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            res = self.store.put_artifact(q.get("run", ""), q.get("name", ""), self.headers.get("Content-Type"),
                                          self.rfile, int(self.headers.get("Content-Length") or 0), self._source(),
                                          q.get("attempt"))
        except (ValueError, OSError) as e:
            self.close_connection = True
            return self._send(400, {"error": str(e)})
        self._send(200, res)

    def do_POST(self):
        self._guard(self._do_POST)

    def _do_POST(self):
        path = urlparse(self.path).path
        if not path.startswith("/api/v1/"):
            return self._send(404, {"error": "not found"})
        if not self._authed():
            return
        try:
            body = self._json()
            items = body if isinstance(body, list) else [body]
            if not all(isinstance(x, dict) for x in items):
                raise ValueError("each item must be a JSON object")
            if path == "/api/v1/report":
                return self._send(200, {"ok": True, "ids": [self.store.ingest(ev) for ev in items]})
            if path == "/api/v1/experiments":
                return self._send(200, {"ok": True, "experiments": [self.store.upsert_experiment(e) for e in items]})
            if path == "/api/v1/runs":
                return self._send(200, {"ok": True, "runs": [self.store.enqueue(r) for r in items]})
            if path == "/api/v1/runs/next":
                r = self.store.next_run(items[0])
                if isinstance(r, dict) and r.get("paused"):
                    return self._send(200, {"run": None, "paused": True})
                return self._send(200, {"run": r})
            if path == "/api/v1/pause":
                b = items[0]
                return self._send(200, self.store.pause(b.get("experiment") or "*", b.get("reason"), self._source()))
            if path == "/api/v1/resume":
                b = items[0]
                return self._send(200, self.store.resume(b.get("experiment") or "all", self._source()))
        except (ValueError, TypeError, json.JSONDecodeError, sqlite3.IntegrityError) as e:
            return self._send(400, {"error": str(e)})
        self._send(404, {"error": "not found"})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.environ.get("SWARM_HUB_DATA", "hubdata"))
    ap.add_argument("--bind", default=os.environ.get("SWARM_HUB_BIND", "127.0.0.1"))
    ap.add_argument("--port", type=int, default=int(os.environ.get("SWARM_HUB_PORT", "8700")))
    args = ap.parse_args()
    token = os.environ.get("SWARM_HUB_TOKEN", "")
    if len(token) < 16:
        raise SystemExit("set SWARM_HUB_TOKEN (16+ chars)")
    Handler.store = Store(Path(args.data))
    Handler.token = token
    read_token = os.environ.get("SWARM_HUB_READ_TOKEN", "")
    if read_token and (len(read_token) < 16 or read_token == token):
        raise SystemExit("SWARM_HUB_READ_TOKEN must be 16+ chars and differ from SWARM_HUB_TOKEN")
    Handler.read_token = read_token
    Handler.dashboard_path = Path(__file__).parent / "dashboard.html"
    srv = ThreadingHTTPServer((args.bind, args.port), Handler)
    srv.daemon_threads = True

    def reaper():
        while True:
            time.sleep(REAP_EVERY)
            try:
                for run in Handler.store.reap():
                    print(f"lease expired: {run}", flush=True)
            except Exception as e:  # noqa: BLE001 - the reaper must never take the hub down
                print(f"reaper error: {e!r}", flush=True)

    threading.Thread(target=reaper, daemon=True, name="reaper").start()
    print(f"swarm hub on {args.bind}:{args.port}, data {args.data}, lease {LEASE}s", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
