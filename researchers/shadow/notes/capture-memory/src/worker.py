#!/usr/bin/env python3
"""Worker: run capture-memory cells, locally or from the hub queue.

    python3 src/worker.py --stage S0 --out results/local-s0            # local, scripted, no hub
    SWARM_SOURCE=shadow/sol-capture python3 src/worker.py --hub           # take queued runs until empty
    SWARM_SOURCE=... python3 src/worker.py --hub --forever

One hub run = one block of tasks in one cell (stage x world x dose x memory); every arm runs on the same
draws inside it. Output: results/episodes/<run>.jsonl, one JSON line per arm per episode, append-only,
uploaded as the run's `episodes.jsonl` plus `summary.json`. Failed episodes are recorded, never retried.
Backend defaults to scripted; `--backend http` is refused unless SWARM_MODEL_CONFIG carries a dollar cap.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sim  # noqa: E402
import model  # noqa: E402
from common import ROOT, load, memory_value, runs_for_stage, task_range  # noqa: E402


def code_commit() -> str | None:
    r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip() or None


def metrics(stats: dict) -> dict:
    m = {}
    n_cap = sum(a["captured"] for a in stats.values()) / max(1, len(stats))
    tot = next(iter(stats.values()))["n"] if stats else 0
    m["captured"] = round(n_cap / tot, 4) if tot else None
    for arm, a in stats.items():
        if a["n"]:
            m[f"frac_T_{arm}"] = round(a["frac_T"] / a["n"], 4)
            m[f"rec_{arm}"] = round(a["rec"] / a["n"], 4)
    if "frac_T_A2_purge_wipe" in m and "frac_T_A1_purge" in m:
        m["wipe_minus_purge"] = round(m["frac_T_A2_purge_wipe"] - m["frac_T_A1_purge"], 4)
    m["episodes"] = sum(a["n"] for a in stats.values())
    m["invalid"] = sum(a["invalid"] for a in stats.values())
    return m


def execute(p: dict, out: Path, policy, backend_name: str, progress=lambda *a, **k: None, run_id=None, attempt=None):
    tasks, seeds, arms = task_range(p["tasks"]), p["seeds"], p["arms"]
    memory = memory_value(p["memory"])
    out.parent.mkdir(parents=True, exist_ok=True)
    code = code_commit()
    stats = {a: {"n": 0, "captured": 0, "frac_T": 0.0, "rec": 0, "invalid": 0} for a in arms}
    total, done = len(tasks) * len(seeds), 0
    with out.open("a") as f:
        for t in tasks:
            for s in seeds:
                for rec in sim.run_episode(t, s, p["world"], p["dose"], arms, p["cfg"], memory=memory,
                                           policy=policy, backend=backend_name):
                    rec.update({"run": run_id, "attempt": attempt, "stage": p["stage"], "split": p["split"],
                                "code": code, "worker": os.environ.get("SWARM_SOURCE"),
                                "python": platform.python_version()})
                    f.write(json.dumps(rec) + "\n")
                    a = stats[rec["arm"]]
                    if rec["validity"]["ok"]:
                        e = rec["evaluation"]
                        a["n"] += 1
                        a["captured"] += e["captured"]
                        a["frac_T"] += e["frac_original_T"]
                        a["rec"] += e["recovered"]
                    else:
                        a["invalid"] += 1
                done += 1
                progress(done, total, **metrics(stats))
    summary = {"run": run_id, "params": p, "episodes_per_arm": total, "stats": stats, "metrics": metrics(stats),
               "backend": backend_name, "code": code, "file": out.name}
    out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hub", action="store_true", help="take queued runs from the hub (needs swarm_report)")
    ap.add_argument("--forever", action="store_true")
    ap.add_argument("--stage", choices=["S0", "S1"], default="S0")
    ap.add_argument("--backend", choices=["scripted", "http"], default="scripted")
    ap.add_argument("--out", help="local mode: output directory (must not exist)")
    ap.add_argument("--limit", type=int, help="local mode: run only the first N cells")
    a = ap.parse_args()
    d = load("design.yaml")
    policy, backend_name = model.build(a.backend)

    if a.hub:
        try:
            import swarm_report as sr
        except ImportError:
            sys.exit("swarm_report not found: run on a fleet server (PYTHONPATH=/usr/local/lib/swarm)")
        if not os.environ.get("SWARM_SOURCE"):
            sys.exit("set SWARM_SOURCE=<you>/<tool>-<n>")
        exp = load("experiment.yaml")["id"]

        def work(run):
            p = run.params
            if p.get("stage") not in ("S0", "S1"):
                raise ValueError("only S0/S1 exist before hypothesis acceptance")
            if p.get("backend", "scripted") != a.backend:
                raise ValueError("worker backend mismatch")
            out = ROOT / "results" / "episodes" / (run.id.replace("/", "__") + ".jsonl")
            summary = execute(p, out, policy, backend_name,
                              lambda done, total, **m: run.progress(done, total, **m),
                              run_id=run.id, attempt=run.attempt)
            run.artifact(out, "episodes.jsonl")
            run.artifact(out.with_suffix(".summary.json"), "summary.json")
            msg = f"{summary['episodes_per_arm']} episodes x {len(p['arms'])} arms, {backend_name}"
            if backend_name == "scripted":
                msg += "; scripted policy, not LLM evidence"
            run.done(message=msg, **summary["metrics"])

        n = sr.work(exp, work, stop_when_empty=not a.forever)
        print(f"worker {os.environ['SWARM_SOURCE']}: {n} run(s) for {exp}")
        return

    if not a.out:
        ap.error("--out required for local execution")
    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=False)
    plist = runs_for_stage(d, a.stage, a.backend)[: a.limit or None]
    t0 = time.monotonic()
    sums = []
    for i, p in enumerate(plist):
        name = f"{p['world']}_d{p['dose']}_m{p['memory']}_{p['tasks']}"
        sums.append(execute(p, outdir / (name + ".jsonl"), policy, backend_name, run_id=name))
        print(f"[{i + 1}/{len(plist)}] {name}: {sums[-1]['metrics']}", flush=True)
    (outdir / "summary.json").write_text(json.dumps({"stage": a.stage, "backend": backend_name,
                                                     "seconds": round(time.monotonic() - t0, 2),
                                                     "cells": sums}, indent=2))


if __name__ == "__main__":
    main()
