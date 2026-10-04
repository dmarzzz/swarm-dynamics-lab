#!/usr/bin/env python3
"""Offline checks, standard library only, a few seconds, no network, no hub, no model.

    python3 src/selftest.py

1. Determinism: the same (task, seed, memory) gives identical records.
2. Pairing: all arms of an episode share the trajectory up to the removal round, and the same capture status.
3. Pairing across memory: the matching and uniforms per round do not depend on arm or memory.
4. Blindness: the policy receives (magnetisation, cfg, draw, ctx) and no field of ctx names the original label;
   evaluation fields are absent from anything the policy can read; the oracle flag is only used at removal.
5. Clean world: in W0_CLEAN every memory length keeps the convention (frac_original_T > 0.8).
6. Capture: in W1_INSIDE at the S1 doses the committed minority captures most populations for bounded memory.
7. Regime control: W2_OUTSIDE A1_purge recovers more often than W1_INSIDE A1_purge at the same memory.
8. Totality: a policy that raises yields validity.ok = false and the episode is recorded.
9. Splits and plan: dev and holdout do not overlap; every stage has a fixed seed list; the primary contrast
   names an existing arm, memory pair, world, dose and stage; runs_for_stage covers each cell once.
10. Model adapter: refuses to build without a dollar cap or call cap; the Budget refuses the request that would
    pass either cap, counts retries, and settles actual usage from provider `usage` fields (no network: a fake
    transport is injected).
11. S1b and the dose rule: the stage only lengthens the takeover cap, its grid covers the rule's grid, the rule's
    horizon fits inside the cap, the plan covers each cell once.
12. Model stages (Q0, S2_pilot): dev split only, declared backend http, S2_pilot queues each memory at its own
    dose_rule dose, per-memory doses match dose_rule.scripted_result, the arms exist, and a scripted plan for them
    is refused. Prefix fork: run_episode's forked arms equal the per-arm simulate() end to end (scripted policy).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model  # noqa: E402
import sim  # noqa: E402
from common import ALL_STAGES, MODEL_STAGES, SCRIPTED_STAGES, load, runs_for_stage, stage_cfg  # noqa: E402

d = load("design.yaml")
cfg, arms, mems = d["cfg"], d["arms"], d["memories"]
fails = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


def strip(recs):
    return [{k: v for k, v in r.items() if k != "cost_actual"} for r in recs]


# 1 determinism
a = sim.run_episode(3, 1, "W1_INSIDE", 0.42, arms, cfg, memory=5)
b = sim.run_episode(3, 1, "W1_INSIDE", 0.42, arms, cfg, memory=5)
check(json.dumps(strip(a)) == json.dumps(strip(b)), "determinism: same task+seed+memory gives identical records")

# 2 pairing across arms
rem = a[0]["trajectory"]["removal_round"]
check(all(r["trajectory"]["removal_round"] == rem for r in a), "pairing: all arms share the removal round")
check(all(r["trajectory"]["series_original"][:rem] == a[0]["trajectory"]["series_original"][:rem] for r in a),
      "pairing: all arms share the trajectory up to removal")
check(len({r["evaluation"]["captured"] for r in a}) == 1, "pairing: capture status is shared by all arms")

# 3 pairing across memory: draws keyed by (task, seed, round) only
p1, u1 = sim.round_draws(3, 1, 7, cfg["n_agents"])
p2, u2 = sim.round_draws(3, 1, 7, cfg["n_agents"])
check(p1 == p2 and u1 == u2, "pairing: round draws depend only on (task, seed, round)")
check(sim.round_draws(3, 2, 7, cfg["n_agents"]) != (p1, u1), "draws: a different seed gives different draws")
check(sim.task(3) == sim.task(3), "task: words are deterministic per task")
check(all(sim.task(t)["words"][sim.ORIG] == sim.task(t)["words"][sim.ORIG] for t in range(10)), "task: cluster truth is seed-free")

# 4 blindness
seen = {}


def spy(m, c, draw, ctx):
    seen.update({k: ctx[k] for k in ctx})
    return sim.scripted_policy(m, c, draw, ctx)


sim.run_episode(3, 1, "W1_INSIDE", 0.42, ["A1_purge"], cfg, memory=5, policy=spy)
leak = {k for k in seen if k in ("original", "evaluation", "captured", "series_original")}
check(not leak, f"blindness: policy ctx carries no outcome fields {sorted(seen)}")
check("mem" in seen and "task" in seen and "h" in seen, "policy sees only memory words, task words and the pull h")
check(all(k in ("task_id", "words") for k in seen["task"]), "blindness: task dict exposes only id and words")

# 5 clean world
def rate(world, dose, arm, memory, metric, n=30, seed=1, captured_only=False):
    recs = [r for t in range(n) for r in sim.run_episode(t, seed, world, dose, [arm], cfg, memory=memory)]
    ev = [r["evaluation"] for r in recs if r["validity"]["ok"]]
    if captured_only:
        ev = [e for e in ev if e["captured"]]
    return sum(float(e[metric]) for e in ev) / len(ev) if ev else float("nan")


for m in mems:
    check(rate("W0_CLEAN", 0.0, "A1_purge", m, "frac_original_T") > 0.8, f"clean world: memory {m} keeps the convention")

# 6 capture at the S1 doses for bounded memory
for dose in d["stages"]["S1"]["doses"]:
    for m in [x for x in mems if x != "full"]:
        c = rate("W1_INSIDE", dose, "A1_purge", m, "captured")
        check(c >= 0.7, f"capture: W1_INSIDE dose {dose} memory {m} captured {c:.2f} >= 0.70")

# 7 regime control
for m in (1, 5):
    ri = rate("W1_INSIDE", 0.42, "A1_purge", m, "recovered", captured_only=True)
    ro = rate("W2_OUTSIDE", 0.42, "A1_purge", m, "recovered", captured_only=True)
    check(ro > ri, f"regime: outside-spinodal recovers more than inside at memory {m} ({ro:.2f} > {ri:.2f})")

# 8 totality
def boom(m, c, draw, ctx):
    raise RuntimeError("policy exploded")


bad = sim.run_episode(1, 1, "W1_INSIDE", 0.42, arms, cfg, memory=5, policy=boom)
check(len(bad) == len(arms) and all(not r["validity"]["ok"] and "RuntimeError" in r["validity"]["error"] for r in bad),
      "totality: a raising policy is recorded as validity.ok = false, one record per arm")

# 9 splits and plan
dev, hold = d["splits"]["dev"], d["splits"]["holdout"]
check(dev[1] < hold[0] or hold[1] < dev[0], "splits: dev and holdout task ids do not overlap")
check(all(isinstance(st["seeds"], list) and st["seeds"] for st in d["stages"].values()), "seeds: every stage has a fixed list")
check("S2" not in d["stages"], "stages: no holdout S2 before hypothesis acceptance (S2_pilot is dev-only)")
pc = d["primary_contrast"]
check(pc["arm"] in arms and pc["world"] in sim.WORLDS and pc["stage"] in d["stages"]
      and pc["dose"] in d["stages"][pc["stage"]]["doses"] and all(m in mems for m in pc["compare_memory"]),
      "primary contrast: names an existing stage, world, dose, arm and memory pair")
for stage in ALL_STAGES:
    st = d["stages"][stage]
    plan = runs_for_stage(d, stage, st.get("backend", "scripted"))
    cells_planned = {(p["world"], p["dose"], p["memory"], p["tasks"]) for p in plan}
    check(len(cells_planned) == len(plan), f"plan: each {stage} cell block is queued once")
    n_mem_dose = (len({(m, dd) for m, dd in st["doses_by_memory"].items()}) if st.get("doses_by_memory")
                  else len(st["doses"]) * len(st.get("memories", mems)))
    want = len(st["worlds"]) * n_mem_dose * -(-st["tasks"] // st.get("block", d["block"]))
    check(len(plan) == want, f"plan: {stage} has {len(plan)} runs = worlds x (memory, dose) x blocks")
check(set(d["stages"]) == set(ALL_STAGES), f"stages: design stages {sorted(d['stages'])} are exactly the known ones")
check(set(arms) <= set(sim.ARMS), f"arms in design.yaml exist in sim.ARMS {sorted(sim.ARMS)}")

# 10 model adapter: caps and the ledger, offline (fake transport)
os.environ["SWARM_MODEL_CONFIG"] = json.dumps({"model": "x", "max_calls": 1})
os.environ["SWARM_MODEL_BASE_URL"] = "https://example.invalid"
try:
    model.build("http")
    check(False, "model adapter: refuses to build without a dollar cap")
except model.ModelFailure:
    check(True, "model adapter: refuses to build without a dollar cap")
os.environ["SWARM_MODEL_CONFIG"] = json.dumps({"model": "x", "max_cost_usd": 1, "input_usd_per_million": 1, "output_usd_per_million": 1})
try:
    model.build("http")
    check(False, "model adapter: refuses to build without a call cap")
except (model.ModelFailure, TypeError):
    check(True, "model adapter: refuses to build without a call cap")


class FakeTransport:
    """Stands in for HTTPPolicy._complete: returns a scripted reply and a usage block, no network."""

    def __init__(self, reply, usage):
        self.reply, self.usage = reply, usage

    def __call__(self, user):
        return self.reply, self.usage, 0


os.environ["SWARM_MODEL_CONFIG"] = json.dumps({"model": "x", "max_calls": 3, "max_cost_usd": 0.001,
                                               "input_usd_per_million": 1000.0, "output_usd_per_million": 1000.0})
pol, name = model.build("http")
tw = sim.task(0)["words"]
pol._complete = FakeTransport(tw[sim.ORIG], {"prompt_tokens": 80, "completion_tokens": 3, "cost": 0.0002})
ctx = {"task": sim.task(0), "mem": [sim.ORIG, sim.ATK], "calls": 0}
check(pol(0.0, cfg, 0.5, ctx) == sim.ORIG and ctx["calls"] == 1 and ctx["cost_usd"] == 0.0002,
      "model adapter: parses the reply and books usage/cost from the provider fields")
# the fake transport bypasses reserve(); drive the Budget directly for the cap checks
b = model.Budget(max_calls=2, max_cost_usd=10.0, in_rate=1000.0, out_rate=1000.0)
b.reserve(300, 8); b.reserve(300, 8)
try:
    b.reserve(300, 8)
    check(False, "budget: the call past max_calls is refused")
except model.ModelFailure:
    check(True, "budget: the call past max_calls is refused")
b = model.Budget(max_calls=100, max_cost_usd=0.0005, in_rate=0.1, out_rate=0.1)
n_ok = 0
try:
    for _ in range(100):
        b.reserve(300, 8); n_ok += 1
except model.ModelFailure:
    pass
check(0 < n_ok < 100 and b.reserved_usd <= 0.0005, f"budget: reservation stops at the dollar cap ({n_ok} calls reserved, {b.reserved_usd:.6f} USD)")
b = model.Budget(max_calls=100, max_cost_usd=0.001, in_rate=0.0, out_rate=0.0)
b.reserve(10, 8); b.settle({"prompt_tokens": 1, "completion_tokens": 1, "cost": 0.002})
try:
    b.reserve(10, 8)
    check(False, "budget: actual usage past the cap refuses the next call even at zero reservation price")
except model.ModelFailure:
    check(True, "budget: actual usage past the cap refuses the next call even at zero reservation price")
pol._complete = FakeTransport(tw[sim.ATK][:-1] + ("x" if tw[sim.ATK][-1] != "x" else "y"), {"prompt_tokens": 80, "completion_tokens": 3})
fz = {"task": sim.task(0), "mem": [sim.ORIG], "calls": 0}
check(pol(0.0, cfg, 0.5, fz) == sim.ATK and fz.get("fuzzy_parses") == 1, "model adapter: an edit-distance-1 reply is accepted and counted as fuzzy")
pol._complete = FakeTransport("something else", {"prompt_tokens": 80, "completion_tokens": 3})
try:
    pol(0.0, cfg, 0.5, {"task": sim.task(0), "mem": [sim.ORIG], "calls": 0})
    check(False, "model adapter: an unparseable reply raises (recorded invalid, never retried)")
except model.ModelFailure:
    check(pol.budget.parse_failures == 1 and pol.budget.parse_retries == 1, "model adapter: an unparseable reply is re-asked once, then raises and is counted")
bad = sim.run_episode(1, 1, "W1_INSIDE", 0.42, arms, cfg, memory=5, policy=pol)
check(all(not r["validity"]["ok"] for r in bad) and all(r["cost_actual"]["prefix"]["parse_failures"] >= 1 for r in bad),
      "totality under the model adapter: a prefix failure invalidates every arm with the prefix ledger attached")

# 11 S1b and the dose rule
s1b, rule = d["stages"]["S1b"], d["dose_rule"]
check(set(s1b["cfg_overrides"]) == {"takeover_max_rounds"}, "S1b: overrides the takeover cap and nothing else")
cfg_b = stage_cfg(d, "S1b")
check(cfg_b["takeover_max_rounds"] >= 2 * rule["horizon"] and cfg_b["takeover_max_rounds"] >= 100,
      f"S1b: takeover cap {cfg_b['takeover_max_rounds']} >= 2 x rule horizon {rule['horizon']}")
check({k: v for k, v in cfg_b.items() if k != "takeover_max_rounds"} == {k: v for k, v in cfg.items() if k != "takeover_max_rounds"},
      "S1b: every other constant equals the frozen S1 cfg")
check(set(rule["grid"]) <= set(s1b["doses"]) and set(d["stages"]["S1"]["doses"]) <= set(s1b["doses"]),
      "S1b: dose grid covers the rule grid and the S1 doses")
check(0 < rule["capture_target"] <= 1 and all(0 < x <= 1 for x in rule["grid"]) and rule["grid"] == sorted(rule["grid"]),
      "dose rule: target in (0, 1], grid sorted and in (0, 1]")
check(all(round(x * cfg["n_agents"]) < cfg["n_agents"] for x in s1b["doses"]), "S1b: every dose leaves at least one honest agent")
check("s2_pilot_draft" not in d["stages"], "S2 draft block is a costing record, not a stage")
r400 = sim.run_episode(0, 1, "W1_INSIDE", 0.42, ["A1_purge"], cfg_b, memory=5)[0]
r100 = sim.run_episode(0, 1, "W1_INSIDE", 0.42, ["A1_purge"], cfg, memory=5)[0]
check(r400["trajectory"]["capture_round"] == r100["trajectory"]["capture_round"]
      and r400["evaluation"]["frac_original_T"] == r100["evaluation"]["frac_original_T"],
      "S1b: a longer cap changes nothing for an episode that captures inside the old cap")

# 12 model stages and the prefix fork
for stage in MODEL_STAGES:
    st = d["stages"][stage]
    check(st["split"] == "dev" and st.get("backend") == "http", f"{stage}: dev split, backend http")
    check(set(st.get("arms", arms)) <= set(sim.ARMS), f"{stage}: arms exist")
    try:
        runs_for_stage(d, stage, "scripted")
        check(False, f"{stage}: a scripted plan is refused")
    except ValueError:
        check(True, f"{stage}: a scripted plan is refused")
s2 = d["stages"]["S2_pilot"]
rule_res = d["dose_rule"]["scripted_result"]["W1_INSIDE"]
check(all(s2["doses_by_memory"][str(m)] == rule_res[str(m)] for m in s2["memories"]),
      "S2_pilot: per-memory doses equal dose_rule.scripted_result (W1_INSIDE)")
plan2 = runs_for_stage(d, "S2_pilot", "http")
check(all(p["dose"] == s2["doses_by_memory"][p["memory"]] for p in plan2), "S2_pilot: every queued run pairs a memory with its own dose")
check(max(int(p["tasks"].split("-")[1]) for p in plan2) < d["splits"]["holdout"][0], "S2_pilot: never touches holdout tasks")
cfg2 = stage_cfg(d, "S2_pilot")
check(cfg2["n_agents"] == 12 and cfg2["eval_round"] <= cfg2["recovery_rounds"], "S2_pilot: N = 12 and eval_round fits in recovery")
for m in (1, "full"):
    t0 = sim.task(4)
    forked = {r["arm"]: r["trajectory"] for r in sim.run_episode(4, 1, "W1_INSIDE", 0.42, arms, cfg, memory=m)}
    direct = {arm: sim.simulate(t0, 1, "W1_INSIDE", 0.42, arm, m, cfg, sim.scripted_policy, {"task": t0}) for arm in arms}
    check(forked == direct, f"prefix fork: forked arms equal per-arm simulate() end to end (memory {m})")
ev = sim.run_episode(4, 1, "W1_INSIDE", 0.42, ["A1_purge"], cfg, memory=1)[0]["evaluation"]
check(abs(ev["delta_original"] - (ev["frac_original_T"] - ev["frac_original_at_removal"])) < 1e-9, "delta_original = frac_original_T - frac_original_at_removal")

print("\nselftest", "FAILED" if fails else "passed")
sys.exit(1 if fails else 0)
