#!/usr/bin/env python3
"""Empty-memory label prior per task for the pilot model: P(original | nothing heard), averaged over both
allowed-name orders. Picks tasks whose prior favours the ORIGINAL word (the de-marzo-2026-conformity inside-spinodal
setting: the committed minority pushes toward the label the model itself disfavours). Writes results/priors-<tag>.json.

    SWARM_MODEL_CONFIG='{"model":"openai/gpt-4o-mini","max_cost_usd":0.1}' python3 src/priors.py --tag 4omini --tasks 0-39
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model  # noqa: E402
import sim  # noqa: E402
from common import task_range  # noqa: E402


class Fake:
    mem = []
    L = None
    kind = "probe"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--tasks", default="0-39")
    ap.add_argument("--reps", type=int, default=1)
    a = ap.parse_args()
    pol, name = model.build("http")
    out = {"model": name, "tasks": {}}
    for t in task_range(a.tasks):
        words = sim.task(t)["words"]
        ctx = {"task": sim.task(t), "low_mass": 0}
        ps = []
        for flip in (False, True):
            for _ in range(a.reps):
                ps.append(pol.one(Fake(), words, ctx, flip))
        p = sum(ps) / len(ps)
        out["tasks"][t] = {"orig": words[sim.ORIG], "atk": words[sim.ATK], "p_orig_empty": round(p, 4),
                           "per_order": [round(x, 4) for x in ps]}
        print(t, words[sim.ORIG], words[sim.ATK], round(p, 3), [round(x, 3) for x in ps], flush=True)
    out["spend_usd"] = round(pol.spent_session, 5)
    (HERE.parent / "results" / f"priors-{a.tag}.json").write_text(json.dumps(out, indent=1))
    fav = [t for t, v in out["tasks"].items() if v["p_orig_empty"] >= 0.6]
    print("tasks with prior toward the original (>= 0.6):", fav)
    print(f"spend {pol.spent_session:.5f}")


if __name__ == "__main__":
    main()
