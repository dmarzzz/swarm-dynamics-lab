#!/usr/bin/env python3
"""Pilot summary statistics that respect the bimodal outcomes: per memory spec under A1_purge (captured episodes),
count of episodes that (a) fully recovered (>= 0.75 on the original for 10 consecutive rounds), (b) reached >= 0.5 at
round 30, plus Fisher exact tests (one-sided, exact hypergeometric, stdlib) of mixture cells vs the pure/edge cells,
and a paired per-task comparison of each mixture against the all-full cell. Also the A2 (wipe) counts.

    python3 src/mp_stats.py results/pilot-mp [mixture fractions, default 0.625,0.75,0.875]
"""
import json, sys
from collections import defaultdict
from math import comb
from pathlib import Path


def fisher_one_sided(a, b, c, d):
    """P(X >= a) for the 2x2 table [[a, b], [c, d]] under the hypergeometric null."""
    n1, n2, k, N = a + b, c + d, a + c, a + b + c + d
    return sum(comb(n1, x) * comb(n2, k - x) for x in range(a, min(n1, k) + 1)) / comb(N, k)


def main():
    d = Path(sys.argv[1])
    mixf = [float(x) for x in (sys.argv[2] if len(sys.argv) > 2 else "0.625,0.75,0.875").split(",")]
    ep = defaultdict(dict)   # (memory, task) -> {arm: evaluation}
    for f in sorted(d.glob("MP_*.jsonl")):
        for l in f.read_text().splitlines():
            e = json.loads(l)
            if e["validity"]["ok"] and e["evaluation"]["captured"]:
                ep[(e["memory"], e["task_id"])][e["arm"]] = e["evaluation"]

    def fval(m):
        return float(m.split("@")[1]) if m.startswith("mix") else (0.0 if m == "full" else 1.0)
    mems = sorted({m for m, _ in ep}, key=fval)
    print(f"{'memory':18s} {'n':>3s} {'recovered':>9s} {'T>=0.5':>7s} {'T>=0.75':>8s} {'mean T':>7s} | wipe: {'rec':>3s} {'T>=0.5':>7s} {'mean T':>7s}")
    rows = {}
    for m in mems:
        A1 = [v["A1_purge"] for (mm, t), v in ep.items() if mm == m and "A1_purge" in v]
        A2 = [v["A2_purge_wipe"] for (mm, t), v in ep.items() if mm == m and "A2_purge_wipe" in v]
        r = dict(n=len(A1), rec=sum(x["recovered"] for x in A1), half=sum(x["frac_original_T"] >= 0.5 for x in A1),
                 q=sum(x["frac_original_T"] >= 0.75 for x in A1), mean=sum(x["frac_original_T"] for x in A1) / max(1, len(A1)),
                 w_rec=sum(x["recovered"] for x in A2), w_half=sum(x["frac_original_T"] >= 0.5 for x in A2),
                 w_mean=sum(x["frac_original_T"] for x in A2) / max(1, len(A2)))
        rows[m] = r
        print(f"{m:18s} {r['n']:3d} {r['rec']:9d} {r['half']:7d} {r['q']:8d} {r['mean']:7.3f} | wipe: {r['w_rec']:3d} {r['w_half']:7d} {r['w_mean']:7.3f}")

    mix = [m for m in mems if m.startswith("mix") and fval(m) in mixf]
    rest = [m for m in mems if m not in mix]
    for key, label in (("rec", "fully recovered"), ("half", "frac_T >= 0.5")):
        a = sum(rows[m][key] for m in mix); b = sum(rows[m]["n"] for m in mix) - a
        c = sum(rows[m][key] for m in rest); dd = sum(rows[m]["n"] for m in rest) - c
        print(f"\n{label}: mixtures f in {mixf}: {a}/{a+b}; all other cells: {c}/{c+dd}; Fisher one-sided p = {fisher_one_sided(a, b, c, dd):.4f}")
    # paired vs all-full per task
    full = {t: v["A1_purge"]["frac_original_T"] for (m, t), v in ep.items() if m == "full" and "A1_purge" in v}
    for m in [x for x in mems if x.startswith("mix")]:
        pairs = [(v["A1_purge"]["frac_original_T"], full[t]) for (mm, t), v in ep.items() if mm == m and "A1_purge" in v and t in full]
        if pairs:
            wins = sum(x > y for x, y in pairs); losses = sum(x < y for x, y in pairs)
            print(f"paired vs all-full, {m}: {len(pairs)} tasks, mixture higher in {wins}, lower in {losses}, mean diff {sum(x - y for x, y in pairs) / len(pairs):+.3f}")


if __name__ == "__main__":
    main()
