#!/usr/bin/env python3
"""Example launcher: start workers for one experiment on a claimed server.

The pattern every launcher in the lab followed:
  1. refuse unless an active claim (claims/<id>.yml) covers the server
  2. pin the research repo on the server to one full commit
  3. decrypt the model credentials with sops and pass them over stdin (never argv, never disk)
  4. enqueue the runs on the hub and start detached workers that report to it

    python3 scripts/example-launcher.py <commit> --server sim-01 --claim alice-boids-sweep \
        --experiment boids-noise --workers 4

Adapt REPO_DIR, WORKER_CMD, SECRETS_FILE and the params list to your experiment.
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REPO_DIR = "/srv/swarm/swarm-dynamics-lab"           # checkout of the research repo on the server
WORKER_CMD = ["python3", "src/worker.py", "--hub"]   # must call swarm_report.work(experiment, fn)
SECRETS_FILE = "secrets/sim.sops.env"                # KEY=value lines, e.g. SWARM_MODEL_API_KEY
SECRET_KEYS = ("SWARM_MODEL_API_KEY",)

# Runs on the server. Reads one JSON payload from stdin, prints one JSON line.
REMOTE = r'''
import json, os, subprocess, sys
p = json.load(sys.stdin)
os.chdir(p["repo_dir"])
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
assert head == p["revision"], f"server checkout is at {head}, not the requested commit"
assert not subprocess.check_output(["git", "status", "--porcelain"], text=True).strip(), "checkout has local edits"
sys.path.insert(0, "/usr/local/lib/swarm")
import swarm_report as sr
os.environ["SWARM_SOURCE"] = p["source"]
ids = sr.enqueue(p["experiment"], p["params"], tags=[p["revision"][:12]])
env = dict(os.environ, **p["secrets"], PYTHONPATH="/usr/local/lib/swarm", SWARM_ROLE="worker")
os.makedirs("results", exist_ok=True)
pids = []
for i in range(p["workers"]):
    log = open(f"results/worker-{p['revision'][:12]}-{i}.log", "x")
    pids.append(subprocess.Popen(p["worker_cmd"] + ["--experiment", p["experiment"]], env=env, stdout=log,
                                 stderr=log, stdin=subprocess.DEVNULL, start_new_session=True).pid)
print(json.dumps({"runs": ids, "worker_pids": pids, "revision": head}))
'''


def active_claim(claim_id: str, server: str, handle: str) -> dict:
    claim = yaml.safe_load((ROOT / "claims" / f"{claim_id}.yml").read_text())
    until = claim.get("until")
    if until and not isinstance(until, datetime):
        until = datetime.fromisoformat(str(until).replace("Z", "+00:00"))
    assert str(claim["by"]).startswith(handle + "/"), "claim belongs to someone else"
    assert server in claim["servers"], "claim does not cover this server"
    assert claim["status"] in ("planned", "running"), "claim is not active"
    assert until is None or until > datetime.now(timezone.utc), "claim has expired: extend it or claim again"
    return claim


def secrets() -> dict:
    env = dict(os.environ)
    env.setdefault("SOPS_AGE_KEY_FILE", str(ROOT / "keys.txt"))
    dec = subprocess.run(["sops", "--decrypt", str(ROOT / SECRETS_FILE)], env=env, text=True, capture_output=True)
    if dec.returncode:
        sys.exit(f"cannot decrypt {SECRETS_FILE} (is your age key in .sops.yaml?)")
    pairs = dict(line.split("=", 1) for line in dec.stdout.splitlines() if "=" in line)
    missing = [k for k in SECRET_KEYS if not pairs.get(k)]
    if missing:
        sys.exit(f"{SECRETS_FILE} lacks {', '.join(missing)}")
    return {k: pairs[k] for k in SECRET_KEYS}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("revision", help="full commit of the research repo to run")
    ap.add_argument("--server", required=True)
    ap.add_argument("--claim", required=True)
    ap.add_argument("--experiment", required=True)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if not re.fullmatch("[0-9a-f]{40}", a.revision):
        ap.error("give the full 40-character commit, so the run is reproducible")
    sys.path.insert(0, str(ROOT / "scripts"))
    import agentops
    handle = agentops.me() or sys.exit("set AGENTOPS_ME in .env")
    claim = active_claim(a.claim, a.server, handle)
    params = [{"eta": e / 10, "seed": s} for e in range(11) for s in (1, 2, 3)]   # your sweep
    payload = {"revision": a.revision, "repo_dir": REPO_DIR, "experiment": a.experiment, "params": params,
               "workers": a.workers, "worker_cmd": WORKER_CMD, "source": claim["by"], "secrets": secrets()}
    config = subprocess.run([sys.executable, "scripts/agentops.py", "ssh-config"], cwd=ROOT, capture_output=True,
                            text=True, check=True).stdout
    with tempfile.NamedTemporaryFile(mode="w") as f:
        os.chmod(f.name, 0o600)
        f.write(config)
        f.flush()
        r = subprocess.run(["ssh", "-F", f.name, "-o", "BatchMode=yes", a.server, "python3 -c " + shlex.quote(REMOTE)],
                           input=json.dumps(payload), text=True, capture_output=True)
    if r.returncode:   # do not echo remote stderr: it could contain the payload
        sys.exit("remote launch refused: check the claim, the commit on the server, the queue and the worker log")
    print(r.stdout.strip())


if __name__ == "__main__":
    main()
