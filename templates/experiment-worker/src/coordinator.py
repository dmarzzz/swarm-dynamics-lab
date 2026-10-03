#!/usr/bin/env python3
"""Coordinator: register the experiment and queue each stage's runs on the hub.

    python3 src/coordinator.py register                 # once, and after editing experiment.yaml
    python3 src/coordinator.py stage S0 [--dry-run]     # queue a stage from design.yaml
    python3 src/coordinator.py status                   # queue + results per stage

S2 (the holdout) is guarded:
  - design.yaml and preregistration.md must be committed with no local edits; their commit is stamped
    on every S2 run (`prereg`), so results can be traced to exactly what was pre-registered;
  - S2 refuses to queue twice (the holdout is opened once), unless --reopen with a dated amendment.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
try:
    import swarm_report as sr
except ImportError:
    sys.exit("swarm_report not found: run on a fleet server, or copy hub/swarm_report.py from swarm-labs-agentops")
import yaml


def load(name):
    return yaml.safe_load((ROOT / name).read_text())


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)


def prereg_commit() -> str:
    files = ["design.yaml", "preregistration.md"]
    dirty = git("status", "--porcelain", "--", *files).stdout.strip()
    if dirty:
        sys.exit(f"S2 refused: commit your pre-registration first (uncommitted: {dirty})")
    c = git("log", "-1", "--format=%H", "--", *files).stdout.strip()
    if not c:
        sys.exit("S2 refused: design.yaml / preregistration.md are not committed")
    if "TODO" in (ROOT / "preregistration.md").read_text():
        sys.exit("S2 refused: preregistration.md still has TODOs")
    return c


def runs_for_stage(exp, d, stage, prereg=None) -> list:
    st = d["stages"][stage]
    lo, hi = d["splits"][st["split"]]
    first = lo
    last = min(hi, lo + st["tasks"] - 1)
    out = []
    for world in st["worlds"]:
        for dose in st["doses"]:
            for b in range(first, last + 1, d["block"]):
                e = min(b + d["block"] - 1, last)
                p = {"stage": stage, "split": st["split"], "world": world, "dose": dose, "tasks": f"{b}-{e}",
                     "seeds": st["seeds"], "arms": d["arms"], "cfg": d["cfg"]}
                if prereg:
                    p["prereg"] = prereg
                out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("register")
    s = sub.add_parser("stage")
    s.add_argument("stage", choices=["S0", "S1", "S2"])
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--reopen", action="store_true", help="S2 again: only with a dated amendment in preregistration.md")
    sub.add_parser("status")
    a = ap.parse_args()
    spec, d = load("experiment.yaml"), load("design.yaml")
    exp = spec["id"]

    if a.cmd == "register":
        sr.register(exp, **{k: spec.get(k) for k in ("title", "description", "params", "metrics",
                                                       "primary_metric", "owner", "url")})
        print(f"registered {exp}")
        return

    if a.cmd == "status":
        runs = sr.runs(exp, limit=5000)
        by = Counter((r["params"].get("stage"), r["status"]) for r in runs)
        for (stage, status), n in sorted(by.items(), key=lambda x: (str(x[0][0]), x[0][1])):
            print(f"{stage or '-':<4} {status:<9} {n}")
        return

    prereg = None
    if a.stage == "S2":
        prereg = prereg_commit()
        if not a.reopen and any(r["params"].get("stage") == "S2" and r["params"].get("kind") != "analysis"
                                    for r in sr.runs(exp, limit=5000)):
            sys.exit("S2 refused: the holdout was already queued once (see --reopen)")
    elif a.stage == "S1" and not any(r["params"].get("stage") == "S0" and r["status"] == "done"
                                     for r in sr.runs(exp, limit=5000)):
        print("warning: no finished S0 runs yet; validate the clean task first")
    plist = runs_for_stage(exp, d, a.stage, prereg)
    eps = sum((int(p["tasks"].split("-")[1]) - int(p["tasks"].split("-")[0]) + 1) * len(p["seeds"]) for p in plist)
    print(f"{a.stage}: {len(plist)} runs, {eps} episodes x {len(d['arms'])} arms" + (f", prereg {prereg[:8]}" if prereg else ""))
    if a.dry_run:
        for p in plist[:3]:
            print("  e.g.", {k: p[k] for k in ("world", "dose", "tasks", "seeds")})
        return
    ids = sr.enqueue(exp, plist, tags=[a.stage])
    print(f"queued {len(ids)} runs; start workers on claimed servers (README step 6)")


if __name__ == "__main__":
    main()
