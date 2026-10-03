#!/usr/bin/env python3
"""Offline checks to pass before anything goes to the hub. No network, a few seconds.

    python3 src/selftest.py

1. Determinism: the same (task, seed) gives byte-identical records.
2. Pairing: every arm in an episode sees the same reports (common random numbers).
3. Blindness: the rules never receive ground truth (reports carry no a_star).
4. Clean task: in W0_CLEAN every arm commits and is mostly right (S0's purpose, at small n).
5. Manipulation check: in W2_FALSE the plurality arm's false-commit rate is higher than in W0_CLEAN.
6. Splits: dev and holdout task ranges do not overlap; seeds are fixed lists.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sim  # noqa: E402
import yaml  # noqa: E402

d = yaml.safe_load((HERE.parent / "design.yaml").read_text())
cfg, arms = d["cfg"], d["arms"]
fails = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


a = sim.run_episode(3, 1, "W2_FALSE", 0.4, arms, cfg)
b = sim.run_episode(3, 1, "W2_FALSE", 0.4, arms, cfg)
strip = lambda recs: [{k: v for k, v in r.items() if k != "cost_actual"} for r in recs]  # noqa: E731
check(json.dumps(strip(a)) == json.dumps(strip(b)), "determinism: same task+seed gives identical records")
check(all(r["reports"] == a[0]["reports"] for r in a), "pairing: all arms see the same reports")
check(all("a_star" not in json.dumps(r["reports"]) for r in a), "blindness: reports carry no ground truth")
check(set(arms) <= set(sim.ARMS), f"arms in design.yaml exist in sim.ARMS {sorted(sim.ARMS)}")


def rate(world, dose, arm, metric, n=200):
    recs = [r for t in range(n) for r in sim.run_episode(t, 1, world, dose, [arm], cfg)]
    return sum(r["evaluation"][metric] for r in recs) / len(recs)


for arm in arms:
    check(rate("W0_CLEAN", 0.0, arm, "committed") > 0.8, f"clean task: {arm} commits in >80% of W0 episodes")
fc_clean, fc_false = rate("W0_CLEAN", 0.0, arms[0], "false_commit"), rate("W2_FALSE", 0.4, arms[0], "false_commit")
check(fc_false > fc_clean, f"manipulation check: {arms[0]} false commits W2 {fc_false:.2f} > W0 {fc_clean:.2f}")
dev, hold = d["splits"]["dev"], d["splits"]["holdout"]
check(dev[1] < hold[0] or hold[1] < dev[0], "splits: dev and holdout task ids do not overlap")
check(all(isinstance(st["seeds"], list) and st["seeds"] for st in d["stages"].values()), "seeds: every stage has a fixed list")
print("\nselftest", "FAILED" if fails else "passed")
sys.exit(1 if fails else 0)
