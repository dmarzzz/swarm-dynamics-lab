#!/usr/bin/env python3
"""Scripted reference for a model stage: run the scripted tanh policy on exactly the stage's cfg, worlds, per-memory
doses and arms (N = 12 etc.), over the stage's own tasks and over a wider dev range, so the model pilot is compared
with the scripted prediction at the SAME configuration rather than with the N = 24 S1b tables.

    python3 src/pilot_reference.py --stage S2_pilot [--tasks 0-99] [--seeds 1,2]

Zero cost. Prints capture rate, median latency, frac_original_T and delta_original under each arm (captured
episodes), with a cluster bootstrap over tasks, and writes results/<stage>_scripted_reference.md.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sim  # noqa: E402
from analyze import boot_ci, mean, _median  # noqa: E402
from common import ROOT, load, memory_value, stage_cfg, task_range  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="S2_pilot")
    ap.add_argument("--tasks", default=None, help="task range, default: the stage's own tasks")
    ap.add_argument("--seeds", default=None, help="comma list, default: the stage's seeds")
    a = ap.parse_args()
    d = load("design.yaml")
    st = d["stages"][a.stage]
    cfg = stage_cfg(d, a.stage)
    lo, hi = d["splits"][st["split"]]
    tasks = task_range(a.tasks) if a.tasks else list(range(lo, lo + st["tasks"]))
    seeds = [int(x) for x in a.seeds.split(",")] if a.seeds else st["seeds"]
    arms = st.get("arms", d["arms"])
    dbm = st.get("doses_by_memory") or {str(m): st["doses"][0] for m in st["memories"]}
    lines = [f"# {a.stage}: scripted reference at the stage's own configuration", "",
             f"Scripted tanh policy (beta {cfg['beta']}, h_inside {cfg['h_inside']}), cfg {cfg}, tasks {tasks[0]}-{tasks[-1]}, seeds {seeds}. "
             "This is what the scripted model predicts for the pilot's exact N, doses, horizons and tasks; it is not a model result.", "",
             "| world | memory | dose | k | n | captured | latency med | arm | frac_orig_T (captured) | 95% CI | delta_original | 95% CI |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for world in st["worlds"]:
        for memory in sorted(dbm, key=lambda m: (0, int(m)) if m != "full" else (1, 0)):
            dose = dbm[memory]
            recs = [r for t in tasks for s in seeds
                    for r in sim.run_episode(t, s, world, dose, arms, cfg, memory=memory_value(memory))]
            for arm in arms:
                xs = [r for r in recs if r["arm"] == arm and r["validity"]["ok"]]
                cap = [r for r in xs if r["evaluation"]["captured"]]
                def bt(metric):
                    by = defaultdict(list)
                    for r in cap:
                        by[r["task_id"]].append(float(r["evaluation"][metric]))
                    by = {t: mean(v) for t, v in by.items()}
                    return mean(list(by.values())), boot_ci(by)
                fT, (flo, fhi) = bt("frac_original_T") if cap else (float("nan"), (float("nan"),) * 2)
                dT, (dlo, dhi) = bt("delta_original") if cap else (float("nan"), (float("nan"),) * 2)
                lines.append(f"| {world} | {memory} | {dose} | {xs[0]['trajectory']['k']} | {len(xs)} | {len(cap)}/{len(xs)} | "
                             f"{_median([r['evaluation']['capture_latency'] for r in cap])} | {arm} | {fT:.3f} | [{flo:.2f}, {fhi:.2f}] | {dT:+.3f} | [{dlo:+.2f}, {dhi:+.2f}] |")
    out = ROOT / "results" / f"{a.stage}_scripted_reference{'' if not a.tasks else '_' + a.tasks}.md"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
