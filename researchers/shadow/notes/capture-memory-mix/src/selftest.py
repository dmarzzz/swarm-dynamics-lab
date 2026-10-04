#!/usr/bin/env python3
"""Offline checks, standard library only, no network, no model.

1. Equivalence: for homogeneous memory the forked-prefix simulator reproduces capture-memory's sim.py exactly
   (same series_original, same evaluation) on 24 (task, seed, memory, dose) draws x 3 arms.
2. Determinism: the same inputs give identical records.
3. Pairing: all arms share the prefix and the capture status; the short set does not depend on arm or world.
4. Mix bookkeeping: round(f * n_honest) honest agents are short; f = 0 and f = 1 equal the homogeneous cases.
5. Blindness: the policy sees agent objects (memory, kind) and ctx without evaluation fields or the original label.
6. Totality: a policy that raises yields validity.ok = false, recorded, for every arm.
7. Plan: every M stage covers each cell once; memory strings round-trip through parse_memory.
8. Model adapter: refuses to build without a cap; the cap clamps at HARD_CAP_USD; the first-token mass parser
   handles leading-space and capitalised tokens.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model  # noqa: E402
import sim  # noqa: E402
from common import SCRIPTED_STAGES, load, memory_param, parse_memory, runs_for_stage, stage_cfg  # noqa: E402

d = load("design.yaml")
cfg, arms = d["cfg"], d["arms"]
fails = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


# 1. equivalence with the parent simulator
old_path = HERE.parent.parent / "capture-memory" / "src" / "sim.py"
spec = importlib.util.spec_from_file_location("oldsim", old_path)
oldsim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oldsim)
same = 0
cases = [(t, s, m, dose, w) for t in (0, 1, 7) for s in (1, 2) for m, dose in ((1, 0.42), (20, 0.42), ("full", 0.54), (5, 0.5))
         for w in ("W1_INSIDE",)]
for t, s, m, dose, w in cases:
    new = sim.run_episode(t, s, w, dose, arms, cfg, memory=m)
    old = oldsim.run_episode(t, s, w, dose, arms, cfg, memory=m)
    for rn, ro in zip(new, old):
        ok = (rn["trajectory"]["series_original"] == ro["trajectory"]["series_original"]
              and {k: v for k, v in rn["evaluation"].items() if k in ro["evaluation"]} == ro["evaluation"])
        same += ok
check(same == len(cases) * len(arms), f"equivalence with capture-memory sim.py on {len(cases)} draws x {len(arms)} arms ({same} identical)")
w2 = sim.run_episode(3, 1, "W2_OUTSIDE", 0.54, arms, cfg, memory=20)
o2 = oldsim.run_episode(3, 1, "W2_OUTSIDE", 0.54, arms, cfg, memory=20)
check(all(a["trajectory"]["series_original"] == b["trajectory"]["series_original"] for a, b in zip(w2, o2)), "equivalence holds in W2_OUTSIDE")

# 2. determinism
mix = {"short": 1, "long": "full", "f": 0.5}
a1 = sim.run_episode(5, 1, "W1_INSIDE", 0.54, arms, cfg, memory=mix)
a2 = sim.run_episode(5, 1, "W1_INSIDE", 0.54, arms, cfg, memory=mix)
check(json.dumps([r["trajectory"] for r in a1]) == json.dumps([r["trajectory"] for r in a2]), "determinism (mix)")

# 3. pairing
rem = a1[0]["trajectory"]["removal_round"]
check(all(r["trajectory"]["series_original"][:rem] == a1[0]["trajectory"]["series_original"][:rem] for r in a1), "arms share the prefix")
check(len({r["trajectory"]["captured"] for r in a1}) == 1, "capture status shared across arms")
honest = [i for i in range(24) if i not in sim.replaced(5, 1, 24, 13)]
s_a = sim.short_set(5, 1, honest, 0.5)
check(s_a == sim.short_set(5, 1, honest, 0.5) and len(s_a) == round(0.5 * len(honest)), "short set keyed on (task, seed), size round(f n_honest)")

# 4. mix bookkeeping
f0 = sim.run_episode(5, 1, "W1_INSIDE", 0.54, arms, cfg, memory={"short": 1, "long": "full", "f": 0.0})
hf = sim.run_episode(5, 1, "W1_INSIDE", 0.54, arms, cfg, memory="full")
check(all(x["trajectory"]["series_original"] == y["trajectory"]["series_original"] for x, y in zip(f0, hf)), "f = 0 equals homogeneous long")
f1 = sim.run_episode(5, 1, "W1_INSIDE", 0.54, arms, cfg, memory={"short": 1, "long": "full", "f": 1.0})
h1 = sim.run_episode(5, 1, "W1_INSIDE", 0.54, arms, cfg, memory=1)
check(all(x["trajectory"]["series_original"] == y["trajectory"]["series_original"] for x, y in zip(f1, h1)), "f = 1 equals homogeneous short")
check(a1[0]["trajectory"]["n_short"] == round(0.5 * 11), f"n_short recorded ({a1[0]['trajectory']['n_short']} of 11 honest at dose 0.54)")
check(a1[1]["evaluation"]["short_T"] is not None and a1[1]["evaluation"]["long_T"] is not None, "per-kind metrics present")

# 5. blindness
seen = {}


def spy(batch, c, ctx):
    seen.update({"ctx_keys": sorted(ctx), "attrs": sorted(set(sim.Honest.__slots__))})
    return sim.scripted_policy(batch, c, ctx)


sim.run_episode(2, 1, "W1_INSIDE", 0.54, arms, cfg, memory=mix, policy=spy)
bad = {"evaluation", "captured", "frac_original_T", "original", "ORIG"}
check(not (set(seen["ctx_keys"]) & bad), f"policy ctx has no evaluation or label fields: {seen['ctx_keys']}")
check("committed" in seen["attrs"] and "word" in seen["attrs"], "policy sees agent memory and word only (committed flag is used by step(), not exposed as a label)")

# 6. totality
def boom(batch, c, ctx):
    raise RuntimeError("provider down")


r = sim.run_episode(2, 1, "W1_INSIDE", 0.54, arms, cfg, memory=mix, policy=boom)
check(len(r) == len(arms) and all(not x["validity"]["ok"] for x in r), "a raising policy yields recorded invalid episodes for every arm")

# 7. plan
for st in SCRIPTED_STAGES:
    plist = runs_for_stage(d, st, "scripted")
    keys = [(p["world"], p["dose"], p["memory"], p["tasks"]) for p in plist]
    check(len(keys) == len(set(keys)) and plist, f"{st}: {len(plist)} runs, each cell once")
for s in ("1", "full", "mix:1/full@0.5", "mix:5/20@0.125"):
    check(memory_param(parse_memory(s)) == s, f"memory string round-trips: {s}")
check(stage_cfg(d, "M1")["takeover_max_rounds"] == 400, "M1 takeover cap 400 (full memory needs it)")

# 8. adapter
import os
os.environ.pop("SWARM_MODEL_CONFIG", None)
try:
    model.build("http"); check(False, "adapter refuses without config")
except model.ModelFailure:
    check(True, "adapter refuses without config")
os.environ["SWARM_MODEL_CONFIG"] = json.dumps({"model": "x/y", "max_cost_usd": 50, "ledger": "/tmp/cmm-selftest-ledger.json"})
try:
    pol, _ = model.build("http")
    check(pol.cap == model.HARD_CAP_USD and model.HARD_CAP_USD <= 20, f"cap clamps at HARD_CAP_USD = {model.HARD_CAP_USD}")
except model.ModelFailure as e:
    check(False, f"adapter builds with a cap ({e})")
words = {sim.ORIG: "zuli", sim.ATK: "mako"}
fake = {"choices": [{"message": {"content": "Zuli."}, "logprobs": {"content": [{"top_logprobs": [
    {"token": " Z", "logprob": -0.2}, {"token": "m", "logprob": -1.8}, {"token": "mak", "logprob": -3.0}, {"token": "\n", "logprob": -5.0}]}]}}]}
mass, content = model.HTTPPolicy._mass(fake, words)
check(abs(mass[sim.ORIG] - 2.718281828 ** -0.2) < 1e-6 and abs(mass[sim.ATK] - (2.718281828 ** -1.8 + 2.718281828 ** -3.0)) < 1e-6,
      "first-token mass parser handles space/case and partial tokens")

print("\nFAILED: " + "; ".join(fails) if fails else "\nall checks passed")
sys.exit(1 if fails else 0)
