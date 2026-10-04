#!/usr/bin/env python3
"""Coordinator: register the exploratory experiment on the hub and queue S0 or S1.

    python3 src/coordinator.py register
    python3 src/coordinator.py stage S0 [--dry-run] [--backend scripted]
    python3 src/coordinator.py status

There is no S2 here. The hypothesis behind this build (PR 82) is not accepted, so the holdout split in
design.yaml is never opened by this code. S2 arrives with the gate, in experiments/<id>/.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import load, runs_for_stage  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("register")
    s = sub.add_parser("stage")
    s.add_argument("stage", choices=["S0", "S1"])
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--backend", choices=["scripted", "http"], default="scripted")
    sub.add_parser("status")
    a = ap.parse_args()
    spec, d = load("experiment.yaml"), load("design.yaml")
    exp = spec["id"]

    if a.cmd == "stage" and a.dry_run:
        plist = runs_for_stage(d, a.stage, a.backend)
        eps = sum((int(p["tasks"].split("-")[1]) - int(p["tasks"].split("-")[0]) + 1) * len(p["seeds"]) for p in plist)
        print(f"{a.stage}: {len(plist)} runs, {eps} episodes x {len(d['arms'])} arms, backend {a.backend}")
        for p in plist[:4]:
            print("  e.g.", {k: p[k] for k in ("world", "dose", "memory", "tasks", "seeds")})
        return

    try:
        import swarm_report as sr
    except ImportError:
        sys.exit("swarm_report not found: run on a fleet server (PYTHONPATH=/usr/local/lib/swarm)")

    if a.cmd == "register":
        sr.register(exp, **{k: spec[k] for k in ("title", "description", "params", "metrics",
                                                  "primary_metric", "owner", "url")})
        print(f"registered {exp}")
    elif a.cmd == "status":
        by = Counter((r["params"].get("stage"), r["status"]) for r in sr.runs(exp, limit=5000))
        for (stage, status), n in sorted(by.items(), key=lambda x: (str(x[0][0]), x[0][1])):
            print(f"{stage or '-':<4} {status:<9} {n}")
    else:
        if a.backend != "scripted":
            sys.exit("refusing: a paid backend needs an explicit human GO and a model pre-step (see README)")
        if a.stage == "S1" and not any(r["params"].get("stage") == "S0" and r["status"] == "done"
                                       for r in sr.runs(exp, limit=5000)):
            print("warning: no finished S0 runs yet; validate the clean world first")
        plist = runs_for_stage(d, a.stage, a.backend)
        existing = {(r["params"].get("stage"), r["params"].get("world"), r["params"].get("dose"),
                     r["params"].get("memory"), r["params"].get("tasks")) for r in sr.runs(exp, limit=5000)}
        plist = [p for p in plist if (p["stage"], p["world"], p["dose"], p["memory"], p["tasks"]) not in existing]
        if not plist:
            sys.exit(f"{a.stage}: every cell is already queued or done; nothing to add")
        ids = sr.enqueue(exp, plist, tags=[a.stage, "exploratory", a.backend])
        print(f"queued {len(ids)} runs for {a.stage}")


if __name__ == "__main__":
    main()
