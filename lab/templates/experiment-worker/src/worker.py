#!/usr/bin/env python3
"""Worker: take queued runs for this experiment from the hub and execute them, until the queue is empty.

    SWARM_SOURCE=<you>/<tool>-<n> python3 src/worker.py            # one process per core: ./run-workers.sh
    python3 src/worker.py --forever                                # keep polling for new work

One hub run = one block of tasks in one cell (stage x world x dose). For every task and every seed in the
block, all arms run on the same draws. Output: results/episodes/<run>.jsonl (one JSON line per arm per
episode, append-only), uploaded to the hub as the run's `episodes.jsonl` artifact plus `summary.json`.
Failed episodes are recorded and counted; nothing is retried or dropped.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sim  # noqa: E402

try:
    import swarm_report as sr  # preinstalled on every fleet server
except ImportError:
    sys.exit("swarm_report not found: run on a fleet server, or copy agentops/hub/swarm_report.py from this repo")

ROOT = HERE.parent
EXP = None


def load_yaml(p: Path):
    import yaml  # python3-yaml is on every fleet server
    return yaml.safe_load(p.read_text())


def execute(run) -> None:
    p = run.params
    lo, hi = (int(x) for x in p["tasks"].split("-"))
    tasks = list(range(lo, hi + 1))
    seeds = p["seeds"]
    arms = p["arms"]
    total = len(tasks) * len(seeds)
    out = ROOT / "results" / "episodes" / (run.id.replace("/", "__") + ".jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    code = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    stats = {a: {"n": 0, "fc": 0, "delay": 0.0, "invalid": 0} for a in arms}
    done = 0
    with out.open("a") as f:                                   # append-only
        for t in tasks:
            for s in seeds:
                for rec in sim.run_episode(t, s, p["world"], p["dose"], arms, p["cfg"]):
                    rec.update({"run": run.id, "attempt": run.attempt, "stage": p["stage"], "split": p["split"],
                                "prereg": p.get("prereg"), "code": code or None, "worker": os.environ.get("SWARM_SOURCE")})
                    f.write(json.dumps(rec) + "\n")
                    a = stats[rec["arm"]]
                    if rec["validity"]["ok"]:
                        a["n"] += 1
                        a["fc"] += rec["evaluation"]["false_commit"]
                        a["delay"] += rec["decision"]["delay"]
                    else:
                        a["invalid"] += 1
                done += 1
                run.progress(done, total, **metrics(stats))
    summary = {"run": run.id, "params": p, "episodes_per_arm": total, "stats": stats, "metrics": metrics(stats),
               "file": out.name}
    (out.with_suffix(".summary.json")).write_text(json.dumps(summary, indent=2))
    res = run.artifact(out, "episodes.jsonl")
    run.artifact(out.with_suffix(".summary.json"), "summary.json")
    if res and not res.get("spooled"):
        # The hub confirmed this file (sha256). recover() checks it is still there on the next start.
        out.with_suffix(".uploaded").write_text(json.dumps({"run": run.id, "sha256": res.get("sha256")}))
    run.done(message=f"{total} episodes x {len(arms)} arms", **metrics(stats))


def recover() -> None:
    """Outbox: re-upload results the hub confirmed earlier but no longer has (e.g. it was restored from a
    backup taken before the upload). Episodes stay on this server's disk, so nothing has to be re-run."""
    d = ROOT / "results" / "episodes"
    for marker in sorted(d.glob("*.uploaded")) if d.exists() else []:
        try:
            info = json.loads(marker.read_text())
            have = {a["name"]: a.get("sha256") for a in sr.get_run(info["run"])["artifacts"]}
        except (sr.HubError, ValueError, KeyError) as e:
            print(f"recover: skipped {marker.name} ({e})")
            continue
        if have.get("episodes.jsonl") != info.get("sha256"):
            jsonl = marker.with_suffix(".jsonl")
            sr.upload(info["run"], jsonl, "episodes.jsonl")
            sr.upload(info["run"], marker.with_suffix(".summary.json"), "summary.json")
            print(f"recover: re-uploaded {jsonl.name} to {info['run']}")


def metrics(stats: dict) -> dict:
    m = {}
    for arm, a in stats.items():
        if a["n"]:
            m[f"fc_{arm}"] = round(a["fc"] / a["n"], 4)
            m[f"delay_{arm}"] = round(a["delay"] / a["n"], 3)
    if "fc_A0_plurality" in m and "fc_A1_provenance" in m:
        m["fc_diff"] = round(m["fc_A0_plurality"] - m["fc_A1_provenance"], 4)
    m["episodes"] = sum(a["n"] + a["invalid"] for a in stats.values())
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forever", action="store_true", help="keep polling when the queue is empty")
    a = ap.parse_args()
    if not os.environ.get("SWARM_SOURCE"):
        sys.exit("set SWARM_SOURCE=<you>/<tool>-<n> (e.g. vishesh/codex-1) so runs are attributed")
    exp = load_yaml(ROOT / "experiment.yaml")["id"]
    recover()
    n = sr.work(exp, execute, stop_when_empty=not a.forever)
    print(f"worker {os.environ['SWARM_SOURCE']}: {n} run(s) for {exp}")


if __name__ == "__main__":
    main()
