#!/usr/bin/env python3
"""Calibration pass for the real-model pilot (cheap, a few hundred calls, logged to results/calib-<tag>.json).

For each candidate word pair and both label orders, query P(word | memory window) from first-token log-probs for
memory windows that are (a) a 5-slot window with 0..5 copies of word A (order-shuffled), (b) a 20-slot window with
0..20 copies, (c) a 40-slot window whose first 30 entries are all A and last 10 are all B, versus the reverse
(recency check: does the model weight the whole list or the tail?). From (a)/(b) fit beta and h of
P(A) = [tanh(beta (m + h)) + 1] / 2 by least squares on a grid. Decides: which pairs are inside the spinodal
(|h| < h_s(beta)) for the pilot, and whether "full memory" is a running mean for this model.

    SWARM_MODEL_CONFIG='{"model":"meta-llama/llama-3.1-8b-instruct","max_cost_usd":0.3}' python3 src/calibrate.py --tag llama8b
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model  # noqa: E402
import sim  # noqa: E402


class Fake:
    def __init__(self, mem):
        self.mem = mem


def p_orig(pol, words, mem, ctx):
    return pol.one(Fake(mem), words, ctx)


def fit(points):
    """points: list of (m, p). grid search beta in [0.2, 6], h in [-1, 1]."""
    best = None
    for bi in range(2, 61):
        beta = bi / 10
        for hi in range(-100, 101):
            h = hi / 100
            err = sum((((math.tanh(beta * (m + h)) + 1) / 2) - p) ** 2 for m, p in points)
            if best is None or err < best[0]:
                best = (err, beta, h)
    return {"sse": round(best[0], 5), "beta": best[1], "h": best[2]}


def spinodal_h(beta):
    """|h_s| for m = tanh(beta (m + h)): h_s = sqrt(1 - 1/beta) - atanh(sqrt(1 - 1/beta)) / beta (beta > 1)."""
    if beta <= 1:
        return 0.0
    s = math.sqrt(1 - 1 / beta)
    return abs(s - math.atanh(s) / beta)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--pairs", type=int, default=4)
    a = ap.parse_args()
    pol, name = model.build("http")
    r = random.Random(11)
    out = {"model": name, "pairs": []}
    pairs = [sim.task(t)["words"] for t in range(a.pairs)]
    for words in pairs:
        A, B = words[sim.ORIG], words[sim.ATK]
        rec = {"orig": A, "atk": B, "L5": [], "L20": [], "recency": {}}
        ctx = {"low_mass": 0}
        for n in range(6):
            mem = [sim.ORIG] * n + [sim.ATK] * (5 - n)
            ps = []
            for _ in range(3):
                r.shuffle(mem)
                ps.append(p_orig(pol, words, list(mem), ctx))
            rec["L5"].append({"n_orig": n, "m": (2 * n - 5) / 5, "p": round(sum(ps) / len(ps), 4)})
        for n in range(0, 21, 2):
            mem = [sim.ORIG] * n + [sim.ATK] * (20 - n)
            ps = []
            for _ in range(2):
                r.shuffle(mem)
                ps.append(p_orig(pol, words, list(mem), ctx))
            rec["L20"].append({"n_orig": n, "m": (2 * n - 20) / 20, "p": round(sum(ps) / len(ps), 4)})
        # recency: 30 A then 10 B (running mean m = +0.5; last-5 m = -1) vs 30 B then 10 A (m = -0.5; last-5 m = +1)
        rec["recency"]["A30_B10"] = round(p_orig(pol, words, [sim.ORIG] * 30 + [sim.ATK] * 10, ctx), 4)
        rec["recency"]["B30_A10"] = round(p_orig(pol, words, [sim.ATK] * 30 + [sim.ORIG] * 10, ctx), 4)
        rec["recency"]["A10_B30"] = round(p_orig(pol, words, [sim.ORIG] * 10 + [sim.ATK] * 30, ctx), 4)
        rec["recency"]["B10_A30"] = round(p_orig(pol, words, [sim.ATK] * 10 + [sim.ORIG] * 30, ctx), 4)
        rec["recency"]["A40"] = round(p_orig(pol, words, [sim.ORIG] * 40, ctx), 4)
        rec["recency"]["B40"] = round(p_orig(pol, words, [sim.ATK] * 40, ctx), 4)
        rec["recency"]["empty"] = round(p_orig(pol, words, [], ctx), 4)
        rec["recency"]["A1"] = round(p_orig(pol, words, [sim.ORIG], ctx), 4)
        rec["recency"]["B1"] = round(p_orig(pol, words, [sim.ATK], ctx), 4)
        rec["fit_L5"] = fit([(x["m"], x["p"]) for x in rec["L5"]])
        rec["fit_L20"] = fit([(x["m"], x["p"]) for x in rec["L20"]])
        for k in ("fit_L5", "fit_L20"):
            b, h = rec[k]["beta"], rec[k]["h"]
            rec[k]["h_spinodal"] = round(spinodal_h(b), 4)
            rec[k]["inside"] = b > 1 and abs(h) < spinodal_h(b)
        rec["low_mass_calls"] = ctx["low_mass"]
        out["pairs"].append(rec)
        print(json.dumps({k: v for k, v in rec.items() if k not in ("L5", "L20")}), flush=True)
    out["spend_usd"] = round(pol.spent_session, 5)
    out["calls"] = pol.calls
    (HERE.parent / "results").mkdir(exist_ok=True)
    (HERE.parent / "results" / f"calib-{a.tag}.json").write_text(json.dumps(out, indent=1))
    print(f"calls {pol.calls}, spend {pol.spent_session:.5f} USD")


if __name__ == "__main__":
    main()
