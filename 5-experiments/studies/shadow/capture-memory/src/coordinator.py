#!/usr/bin/env python3
"""Coordinator: register the exploratory experiment on the hub and queue a stage.

    python3 src/coordinator.py register
    python3 src/coordinator.py stage S0|S1|S1b [--dry-run]                       # scripted, free
    python3 src/coordinator.py stage Q0|S2_pilot --backend http --go "<who, when>"  # real model, capped
    python3 src/coordinator.py status

The holdout split in design.yaml is never opened by this code: every stage here reads dev tasks. Q0 and
S2_pilot are real-model stages on a labelled hunch (PR 82 is `proposed`, not accepted); queueing one needs
`--backend http` and an explicit `--go` string naming the human and time, which is stamped on every run.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import ALL_STAGES, MODEL_STAGES, load, runs_for_stage  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("register")
    s = sub.add_parser("stage")
    s.add_argument("stage", choices=list(ALL_STAGES))
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--backend", choices=["scripted", "http"], default="scripted")
    s.add_argument("--go", help="model stages only: who gave the GO and when (stamped on every run)")
    sub.add_parser("status")
    a = ap.parse_args()
    spec, d = load("experiment.yaml"), load("design.yaml")
    exp = spec["id"]

    if a.cmd == "stage" and a.dry_run:
        plist = runs_for_stage(d, a.stage, a.backend)
        eps = sum((int(p["tasks"].split("-")[1]) - int(p["tasks"].split("-")[0]) + 1) * len(p["seeds"]) for p in plist)
        print(f"{a.stage}: {len(plist)} runs, {eps} episodes x {len(plist[0]['arms']) if plist else 0} arms, backend {a.backend}")
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
            if a.stage not in MODEL_STAGES:
                sys.exit(f"refusing: {a.stage} is a scripted stage")
            if not a.go:
                sys.exit("refusing: a paid backend needs an explicit human GO (--go \"<who>, <when>\"), see README")
            if a.stage == "S2_pilot" and not any(r["params"].get("stage") == "Q0" and r["status"] == "done"
                                                 and (r.get("metrics") or {}).get("validity", 0) >= 0.9
                                                 for r in sr.runs(exp, limit=5000)):
                sys.exit("refusing: S2_pilot needs a finished Q0 run with validity >= 0.90 on the hub first")
        if a.stage != "S0" and not any(r["params"].get("stage") == "S0" and r["status"] == "done"
                                       for r in sr.runs(exp, limit=5000)):
            print("warning: no finished S0 runs yet; validate the clean world first")
        plist = runs_for_stage(d, a.stage, a.backend)
        if a.go:
            for p in plist:
                p["go"] = a.go
        existing = {(r["params"].get("stage"), r["params"].get("world"), r["params"].get("dose"),
                     r["params"].get("memory"), r["params"].get("tasks")) for r in sr.runs(exp, limit=5000)}
        plist = [p for p in plist if (p["stage"], p["world"], p["dose"], p["memory"], p["tasks"]) not in existing]
        if not plist:
            sys.exit(f"{a.stage}: every cell is already queued or done; nothing to add")
        ids = sr.enqueue(exp, plist, tags=[a.stage, "exploratory", a.backend])
        print(f"queued {len(ids)} runs for {a.stage}")


if __name__ == "__main__":
    main()
