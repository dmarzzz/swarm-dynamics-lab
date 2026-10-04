"""The environment: a quorum of agents deciding among K options, some of whom copy one shared source.

Deterministic given (task_id, seed). This file is the only one that knows the toy; replace it with your
simulator and keep the contract:

    run_episode(task_id, seed, world, dose, arms, cfg) -> list of episode records, one per arm

Every arm in `arms` is scored on the SAME draws (common random numbers), so arm contrasts are paired.
The aggregation rules see only the agents' reports (vote, evidence root). Ground truth enters only in
`evaluate()`, after the decision is locked.
"""
from __future__ import annotations

import random
import time

WORLDS = {
    "W0_CLEAN": "no shared source: every agent observes independently",
    "W1_TRUE": "the shared source points at the correct option",
    "W2_FALSE": "the shared source points at a wrong option (injected)",
}


def task(task_id: int, k: int) -> dict:
    """A task is the clustering unit: its truth does not depend on the seed."""
    r = random.Random(f"task:{task_id}")
    return {"task_id": task_id, "a_star": r.randrange(k)}


def draw_reports(t: dict, seed: int, world: str, dose: float, cfg: dict) -> list:
    """What the agents report. Shared by every arm in the episode."""
    r = random.Random(f"episode:{t['task_id']}:{seed}")
    k, n, q = cfg["k"], cfg["n_agents"], cfg["reliability"]
    wrong = [o for o in range(k) if o != t["a_star"]]
    shared_vote = t["a_star"] if world == "W1_TRUE" else r.choice(wrong)
    n_copy = 0 if world == "W0_CLEAN" else round(dose * n)
    reports = []
    for i in range(n):
        if i < n_copy:
            reports.append({"agent": i, "vote": shared_vote, "root": "shared"})
        else:
            vote = t["a_star"] if r.random() < q else r.choice(wrong)
            reports.append({"agent": i, "vote": vote, "root": f"own-{i}"})
    r.shuffle(reports)                     # arrival order, also shared by every arm
    return reports


# ----------------------------------------------------------------- arms (aggregation rules)

def quorum(reports: list, theta: float, n: int, provenance: bool):
    """Commit to the first option whose support reaches theta * n as reports arrive.
    provenance=False counts votes; provenance=True counts distinct evidence roots."""
    support: dict = {}
    for arrived, rep in enumerate(reports, start=1):
        key = rep["root"] if provenance else rep["agent"]
        support.setdefault(rep["vote"], set()).add(key)
        if len(support[rep["vote"]]) >= theta * n:
            return rep["vote"], arrived
    return None, len(reports)              # no commitment by the deadline: abstain


ARMS = {
    "A0_plurality": lambda reps, cfg: quorum(reps, cfg["theta"], cfg["n_agents"], provenance=False),
    "A1_provenance": lambda reps, cfg: quorum(reps, cfg["theta"], cfg["n_agents"], provenance=True),
}


def evaluate(t: dict, choice, cfg: dict) -> dict:
    committed = choice is not None
    correct = committed and choice == t["a_star"]
    return {
        "a_star": t["a_star"],
        "committed": committed,
        "correct": correct,
        "false_commit": committed and not correct,
        "regret": 0.0 if correct else (cfg["abstain_cost"] if not committed else 1.0),
    }


def run_episode(task_id: int, seed: int, world: str, dose: float, arms: list, cfg: dict) -> list:
    t = task(task_id, cfg["k"])
    reports = draw_reports(t, seed, world, dose, cfg)
    out = []
    for arm in arms:
        t0 = time.perf_counter()
        try:
            choice, delay = ARMS[arm](reports, cfg)
            ok = True
        except Exception as e:  # noqa: BLE001 - a failed episode is a recorded outcome, never retried
            choice, delay, ok = None, None, False
            err = f"{type(e).__name__}: {e}"
        rec = {
            "task_id": task_id, "seed": seed, "world": world, "dose": dose, "arm": arm,
            "cfg": cfg,
            "reports": [{"vote": r["vote"], "root": r["root"]} for r in reports],
            "decision": {"choice": choice, "delay": delay},
            "evaluation": evaluate(t, choice, cfg) if ok else None,
            "validity": {"ok": ok, **({} if ok else {"error": err})},
            "cost_actual": {"wall_s": round(time.perf_counter() - t0, 6)},
        }
        out.append(rec)
    return out
