#!/usr/bin/env python3
"""Worker: run capture-memory-mix cells locally (scripted) or from the hub queue.

    python3 src/worker.py --stage M1 --out results/local-m1 [--jobs 8]      # local, scripted, parallel over cells
    SWARM_SOURCE=shadow/sol-goal python3 src/worker.py --hub                  # take queued runs until empty
    python3 src/worker.py --pilot results/pilot-mp --backend http             # real-model pilot (design pilot_MP)

Output: one JSON line per arm per episode, append-only. Failed episodes are recorded, never retried.
`--backend http` needs SWARM_MODEL_CONFIG (JSON) with model + max_cost_usd; the cap is clamped to USD 5 in model.py.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sim  # noqa: E402
import model  # noqa: E402
from common import ROOT, SCRIPTED_STAGES, load, parse_memory, runs_for_stage, task_range  # noqa: E402


def code_commit() -> str | None:
    r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip() or None


def metrics(stats: dict) -> dict:
    m = {}
    tot = next(iter(stats.values()))["n"] if stats else 0
    n_cap = sum(a["captured"] for a in stats.values()) / max(1, len(stats))
    m["captured"] = round(n_cap / tot, 4) if tot else None
    for arm, a in stats.items():
        if a["n"]:
            m[f"frac_T_{arm}"] = round(a["frac_T"] / a["n"], 4)
            m[f"delta_{arm}"] = round(a["delta"] / a["n"], 4)
    if "frac_T_A2_purge_wipe" in m and "frac_T_A1_purge" in m:
        m["wipe_minus_purge"] = round(m["frac_T_A2_purge_wipe"] - m["frac_T_A1_purge"], 4)
    m["episodes"] = sum(a["n"] for a in stats.values())
    m["invalid"] = sum(a["invalid"] for a in stats.values())
    m["model_calls"] = sum(a["calls"] for a in stats.values())
    m["cost_usd"] = round(sum(a["usd"] for a in stats.values()), 4)
    return m


def execute(p: dict, out: Path, policy, backend_name: str, progress=lambda *a, **k: None, run_id=None, attempt=None):
    tasks, seeds, arms = task_range(p["tasks"]), p["seeds"], p["arms"]
    memory = parse_memory(p["memory"])
    out.parent.mkdir(parents=True, exist_ok=True)
    code = code_commit()
    stats = {a: {"n": 0, "captured": 0, "frac_T": 0.0, "delta": 0.0, "invalid": 0, "calls": 0, "usd": 0.0} for a in arms}
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
                    f.flush()
                    a = stats[rec["arm"]]
                    a["calls"] += rec["cost_actual"]["model_calls"]
                    a["usd"] += rec["cost_actual"].get("cost_usd", 0.0)
                    if rec["validity"]["ok"]:
                        e = rec["evaluation"]
                        a["n"] += 1
                        a["captured"] += e["captured"]
                        a["frac_T"] += e["frac_original_T"]
                        a["delta"] += e["delta_original"]
                    else:
                        a["invalid"] += 1
                done += 1
                progress(done, total, **metrics(stats))
    summary = {"run": run_id, "params": p, "episodes_per_arm": total, "stats": stats, "metrics": metrics(stats),
               "backend": backend_name, "code": code, "file": out.name}
    out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def _local_cell(args):
    p, outdir, backend = args
    policy, backend_name = model.build(backend)
    name = f"{p['world']}_d{p['dose']}_m{p['memory']}_{p['tasks']}".replace("/", "-").replace("@", "_f").replace(":", "-")
    return execute(p, Path(outdir) / (name + ".jsonl"), policy, backend_name, run_id=name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hub", action="store_true")
    ap.add_argument("--forever", action="store_true")
    ap.add_argument("--stage", choices=list(SCRIPTED_STAGES), default="M1")
    ap.add_argument("--backend", choices=["scripted", "http"], default="scripted")
    ap.add_argument("--out")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--pilot", help="directory for the real-model pilot (design pilot_MP); needs --backend http")
    ap.add_argument("--pilot-cells", help="JSON list of {world,dose,memory,tasks,seeds,arms} overriding pilot_MP cells")
    a = ap.parse_args()
    d = load("design.yaml")

    if a.pilot:
        if a.backend != "http":
            sys.exit("the pilot is a real-model run: pass --backend http with SWARM_MODEL_CONFIG")
        policy, backend_name = model.build(a.backend)
        outdir = Path(a.pilot)
        outdir.mkdir(parents=True, exist_ok=True)
        cfg = {**d["cfg"], **d["pilot_MP"]["cfg_overrides"]}
        cells = json.loads(a.pilot_cells) if a.pilot_cells else json.loads((outdir / "cells.json").read_text())
        t0 = time.monotonic()
        sums = []
        for i, c in enumerate(cells):
            p = {"stage": "MP", "split": "dev", "world": c["world"], "dose": c["dose"], "memory": c["memory"],
                 "tasks": c["tasks"], "seeds": c.get("seeds", [1]), "arms": c.get("arms", d["arms"]),
                 "cfg": {**cfg, **c.get("cfg_overrides", {})}, "backend": "http"}
            name = f"MP_{p['world']}_d{p['dose']}_m{p['memory']}_{p['tasks']}".replace("/", "-").replace("@", "_f").replace(":", "-")
            try:
                sums.append(execute(p, outdir / (name + ".jsonl"), policy, backend_name, run_id=name,
                                    progress=lambda done, total, **m: print(f"    {name} {done}/{total} {m}", flush=True)))
                print(f"[{i + 1}/{len(cells)}] {name}: {sums[-1]['metrics']}", flush=True)
            except model.ModelFailure as e:
                print(f"[{i + 1}/{len(cells)}] {name}: STOPPED {e}", flush=True)
                break
        (outdir / "summary.json").write_text(json.dumps({"stage": "MP", "backend": backend_name,
                                                         "seconds": round(time.monotonic() - t0, 2),
                                                         "ledger": json.loads(policy.ledger.path.read_text()),
                                                         "cells": sums}, indent=2))
        return

    if a.hub:
        try:
            import swarm_report as sr
        except ImportError:
            sys.exit("swarm_report not found")
        if not os.environ.get("SWARM_SOURCE"):
            sys.exit("set SWARM_SOURCE=<you>/<tool>-<n>")
        policy, backend_name = model.build(a.backend)
        exp = load("experiment.yaml")["id"]

        def work(run):
            p = run.params
            if p.get("stage") not in SCRIPTED_STAGES:
                raise ValueError("only M0/M1/M2 are hub stages")
            if p.get("backend", "scripted") != a.backend:
                raise ValueError("worker backend mismatch")
            out = ROOT / "results" / "episodes" / (run.id.replace("/", "__") + ".jsonl")
            summary = execute(p, out, policy, backend_name,
                              lambda done, total, **m: run.progress(done, total, **m),
                              run_id=run.id, attempt=run.attempt)
            run.artifact(out, "episodes.jsonl")
            run.artifact(out.with_suffix(".summary.json"), "summary.json")
            run.done(message=f"{summary['episodes_per_arm']} episodes x {len(p['arms'])} arms, {backend_name}"
                     + ("; scripted policy, not LLM evidence" if backend_name == "scripted" else ""),
                     **summary["metrics"])

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
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        for i, s in enumerate(ex.map(_local_cell, [(p, str(outdir), a.backend) for p in plist])):
            sums.append(s)
            print(f"[{i + 1}/{len(plist)}] {s['run']}: {s['metrics']}", flush=True)
    (outdir / "summary.json").write_text(json.dumps({"stage": a.stage, "backend": a.backend,
                                                     "seconds": round(time.monotonic() - t0, 2),
                                                     "cells": sums}, indent=2))


if __name__ == "__main__":
    main()
