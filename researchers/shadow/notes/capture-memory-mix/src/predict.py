#!/usr/bin/env python3
"""Model-calibrated scripted prediction for the pilot cells.

Runs the pilot cells (results/pilot-mp/cells.json) with the scripted tanh policy at the (beta, h) measured on the
model (src/calibrate.py or the probe log), over many tasks, so the real-model pilot has a quantitative prediction
per cell BEFORE it runs. The cached-policy construction of flint-2026-group, reduced to two parameters.

    python3 src/predict.py --beta 8 --h 0.0 --tasks 0-99 --out results/pilot-pred-b8h0
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sim  # noqa: E402
from common import load, parse_memory  # noqa: E402
from worker import execute  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--beta", type=float, required=True)
    ap.add_argument("--h", type=float, required=True)
    ap.add_argument("--tasks", default="0-99")
    ap.add_argument("--seeds", default="1")
    ap.add_argument("--cells", default="results/pilot-mp/cells.json")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = load("design.yaml")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    cells = json.loads(Path(a.cells).read_text())
    cfg0 = {**d["cfg"], **d["pilot_MP"]["cfg_overrides"], "beta": a.beta, "h_inside": a.h, "h_outside": a.h}
    for c in cells:
        p = {"stage": "MP", "split": "dev", "world": c["world"], "dose": c["dose"], "memory": c["memory"],
             "tasks": a.tasks, "seeds": [int(s) for s in a.seeds.split(",")], "arms": c.get("arms", d["arms"]),
             "cfg": {**cfg0, **c.get("cfg_overrides", {}), "beta": a.beta, "h_inside": a.h, "h_outside": a.h},
             "backend": "scripted"}
        name = f"PRED_{p['world']}_d{p['dose']}_m{p['memory']}".replace("/", "-").replace("@", "_f").replace(":", "-")
        s = execute(p, out / (name + ".jsonl"), sim.scripted_policy, f"scripted(beta={a.beta},h={a.h})", run_id=name)
        print(name, s["metrics"], flush=True)


if __name__ == "__main__":
    main()
