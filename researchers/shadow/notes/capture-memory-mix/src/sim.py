"""capture-memory-mix: heterogeneous memory lengths in a captured-then-purged convention swarm.

Extends researchers/shadow/notes/capture-memory (one memory length per population) to populations in which a
fraction f of the honest agents keep a SHORT window (L_short, default 1) and the rest keep a LONG window
(L_long in {20, full}). Everything else is the capture-memory protocol: binary convention, N agents, random
perfect matching each round, committed minority above the tipping dose, oracle purge, recovery.

Contract (templates/experiment-worker/README.md step 3):

    run_episode(task_id, seed, world, dose, arms, cfg, memory=..., policy=..., backend=...) -> one record per arm

`memory` is either a scalar (1, 5, 20, "full": homogeneous, identical to capture-memory) or a dict
{"short": 1, "long": 20, "f": 0.5}: exactly round(f * n_honest) of the honest agents get the short window, chosen
by a draw keyed on (task, seed) only, so the same agents are short at a given f across arms and worlds.

Pairing: the matching schedule and each agent's per-round uniform are keyed by (task, seed, round) only. The arms
of an episode share the whole pre-intervention prefix by construction (it is simulated once and forked), so
capture status is identical across arms and the arm contrast is paired per draw.

Policies are BATCHED: `policy(batch, cfg, ctx) -> list[float]` returns P(original) for every honest agent that
heard a word this round, so a model backend can issue the round's calls concurrently (decisions are simultaneous
by design). The word an agent says is ORIG iff its per-round uniform draw < P(original). The scripted policy is the
capture-memory tanh rule over the memory magnetisation; the model policy (model.py) reads the first-token
log-probabilities of the two allowed words. A scripted result is a property of the rule, not of LLM agents.
"""
from __future__ import annotations

import copy
import math
import random
import time

WORLDS = {
    "W0_CLEAN": "inside-spinodal pair, no committed minority ever; intrinsic drift",
    "W1_INSIDE": "inside-spinodal pair (h = cfg.h_inside); k = round(dose N) agents replaced by committed ones",
    "W2_OUTSIDE": "outside-spinodal pair (h = cfg.h_outside), regime control: the attack label is not metastable",
}

MEMORY_FULL = "full"
ORIG, ATK = 1, -1

# Twelve nonsense words with twelve distinct first letters, so a model's first-token log-probability identifies the
# word. Which of a task's two words is the original alternates with task parity (yang-2026-when label control).
WORDS = ["zuli", "mako", "teru", "vand", "pira", "sello", "quon", "brisk", "fenn", "olam", "ruvo", "kade"]
assert len({w[0] for w in WORDS}) == len(WORDS)


def task(task_id: int) -> dict:
    r = random.Random(f"task:{task_id}")
    w = r.sample(WORDS, 2)
    return {"task_id": task_id, "words": {ORIG: w[task_id % 2], ATK: w[1 - task_id % 2]}}


# ----------------------------------------------------------------- draws (shared by every arm and memory spec)

def round_draws(task_id: int, seed: int, rnd: int, n: int):
    r = random.Random(f"round:{task_id}:{seed}:{rnd}")
    ids = list(range(n))
    r.shuffle(ids)
    return [(ids[i], ids[i + 1]) for i in range(0, n - 1, 2)], [r.random() for _ in range(n)]


def replaced(task_id: int, seed: int, n: int, k: int) -> list:
    return sorted(random.Random(f"replace:{task_id}:{seed}").sample(range(n), k))


def short_set(task_id: int, seed: int, honest: list, f: float, replaced_ids: list = ()) -> set:
    """Which agents carry the short window: round(f * n_honest) of the honest agents, plus round(f * k) of the
    agents that will later be replaced (so the entrench-phase population has the same mix and f = 1 / f = 0
    reduce exactly to the homogeneous populations). Keyed on (task, seed) only."""
    r = random.Random(f"mix:{task_id}:{seed}")
    out = set(r.sample(sorted(honest), round(f * len(honest))))
    if replaced_ids:
        out |= set(r.sample(sorted(replaced_ids), round(f * len(replaced_ids))))
    return out


# ----------------------------------------------------------------- agents

class Honest:
    __slots__ = ("word", "L", "mem", "count", "committed", "kind")

    def __init__(self, word: int, L, kind: str = "long"):
        self.word = word
        self.L = None if L == MEMORY_FULL else int(L)
        self.mem = []
        self.count = 0
        self.committed = False
        self.kind = kind                      # "short" | "long" (homogeneous populations are all "long")

    def hear(self, w: int):
        self.mem.append(w)
        self.count += w
        if self.L is not None and len(self.mem) > self.L:
            self.count -= self.mem.pop(0)

    def magnetisation(self) -> float:
        return self.count / len(self.mem) if self.mem else 0.0

    def wipe(self):
        self.mem.clear()
        self.count = 0


class Committed:
    __slots__ = ("word", "committed", "kind")

    def __init__(self, word: int):
        self.word = word
        self.committed = True
        self.kind = "committed"


def scripted_policy(batch: list, cfg: dict, ctx: dict) -> list:
    """P(original) = [tanh(beta (m + h)) + 1] / 2 per agent, from its memory magnetisation only."""
    return [(math.tanh(cfg["beta"] * (ag.magnetisation() + ctx["h"])) + 1) / 2 for ag in batch]


def step(agents: dict, task_id: int, seed: int, rnd: int, cfg: dict, policy, ctx: dict) -> None:
    n = cfg["n_agents"]
    pairs, draws = round_draws(task_id, seed, rnd, n)
    heard = {}
    for a, b in pairs:
        if a in agents and b in agents:
            heard[a] = agents[b].word
            heard[b] = agents[a].word
    ids = [i for i, w in heard.items() if not agents[i].committed]
    for i in ids:
        agents[i].hear(heard[i])
    ctx["round"] = rnd
    probs = policy([agents[i] for i in ids], cfg, ctx)
    for i, p in zip(ids, probs):
        agents[i].word = ORIG if draws[i] < p else ATK


def frac_original(agents: dict, kind: str | None = None) -> float:
    hon = [ag for ag in agents.values() if not ag.committed and (kind is None or ag.kind == kind)]
    return sum(1 for ag in hon if ag.word == ORIG) / len(hon) if hon else float("nan")


def streak(series: list, thresh: float, k: int, above: bool = True) -> int | None:
    run = 0
    for i, x in enumerate(series):
        hit = x >= thresh if above else x <= thresh
        run = run + 1 if hit else 0
        if run >= k:
            return i - k + 1
    return None


def memory_spec(memory) -> dict:
    if isinstance(memory, dict):
        return {"short": memory.get("short", 1), "long": memory["long"], "f": float(memory["f"])}
    return {"short": memory, "long": memory, "f": 0.0}


def memory_label(memory) -> str:
    s = memory_spec(memory)
    if isinstance(memory, dict):
        return f"mix:{s['short']}/{s['long']}@{s['f']:g}"
    return str(memory)


# ----------------------------------------------------------------- one episode: shared prefix, forked arms

def _record(series, series_short, series_long, k, entrench_end, capture_round, removal_round, rnd):
    return {"k": k, "entrench_end": entrench_end, "capture_round": capture_round,
            "captured": capture_round is not None, "removal_round": removal_round, "rounds": rnd,
            "series_original": [round(x, 4) for x in series],
            "series_short": [None if x != x else round(x, 4) for x in series_short],
            "series_long": [None if x != x else round(x, 4) for x in series_long]}


def simulate_prefix(t: dict, seed: int, world: str, dose: float, memory, cfg: dict, policy, ctx: dict):
    n = cfg["n_agents"]
    k = 0 if world == "W0_CLEAN" else round(dose * n)
    ctx["h"] = cfg["h_outside"] if world == "W2_OUTSIDE" else cfg["h_inside"]
    spec = memory_spec(memory)
    rep = replaced(t["task_id"], seed, n, k) if k else []
    honest = [i for i in range(n) if i not in rep]
    shorts = short_set(t["task_id"], seed, honest, spec["f"], rep) if isinstance(memory, dict) else set()
    agents = {}
    for i in range(n):
        kind = "short" if i in shorts else "long"
        agents[i] = Honest(ORIG, spec["short"] if kind == "short" else spec["long"], kind)
        agents[i].hear(ORIG)
    series, s_short, s_long = [], [], []

    def log():
        series.append(frac_original(agents))
        s_short.append(frac_original(agents, "short"))
        s_long.append(frac_original(agents, "long"))

    rnd = 0
    for _ in range(cfg["entrench_rounds"]):
        step(agents, t["task_id"], seed, rnd, cfg, policy, ctx); rnd += 1
        log()
    entrench_end = rnd
    capture_round = None
    for i in rep:
        agents[i] = Committed(ATK)
    cap = cfg["takeover_max_rounds"] if k else cfg["clean_takeover_rounds"]
    for _ in range(cap):
        step(agents, t["task_id"], seed, rnd, cfg, policy, ctx); rnd += 1
        log()
        if k:
            s = streak(series[entrench_end:], 1 - cfg["capture_frac"], cfg["capture_streak"], above=False)
            if s is not None:
                capture_round = entrench_end + s
                break
    return {"agents": agents, "k": k, "entrench_end": entrench_end, "capture_round": capture_round,
            "removal_round": rnd, "series": series, "s_short": s_short, "s_long": s_long,
            "n_short": len(shorts & set(honest)), "n_honest": len(honest)}


def simulate_arm(prefix: dict, t: dict, seed: int, arm: str, cfg: dict, policy, ctx: dict) -> dict:
    agents = copy.deepcopy(prefix["agents"])
    k, rnd = prefix["k"], prefix["removal_round"]
    series, s_short, s_long = list(prefix["series"]), list(prefix["s_short"]), list(prefix["s_long"])
    if k and arm in ("A1_purge", "A2_purge_wipe"):
        agents = {i: ag for i, ag in agents.items() if not ag.committed}
    if k and arm == "A2_purge_wipe":
        for ag in agents.values():
            ag.wipe()
    for _ in range(cfg["recovery_rounds"]):
        step(agents, t["task_id"], seed, rnd, cfg, policy, ctx); rnd += 1
        series.append(frac_original(agents))
        s_short.append(frac_original(agents, "short"))
        s_long.append(frac_original(agents, "long"))
    rec = _record(series, s_short, s_long, k, prefix["entrench_end"], prefix["capture_round"],
                  prefix["removal_round"], rnd)
    rec["n_short"], rec["n_honest"] = prefix["n_short"], prefix["n_honest"]
    return rec


def evaluate(t: dict, run: dict, cfg: dict) -> dict:
    rem = run["removal_round"]
    T = cfg["eval_round"]
    post = run["series_original"][rem:]
    rec = streak(post[:T], cfg["recover_frac"], cfg["recover_streak"])

    def at(series, i):
        v = series[i] if len(series) > i else None
        return None if v is None else v

    ps, pl = run["series_short"][rem:], run["series_long"][rem:]
    out = {
        "captured": run["captured"],
        "capture_latency": None if run["capture_round"] is None else run["capture_round"] - run["entrench_end"] + 1,
        "entrench_frac_original": run["series_original"][run["entrench_end"] - 1],
        "frac_original_at_removal": run["series_original"][rem - 1],
        "frac_original_T": post[T - 1] if len(post) >= T else float("nan"),
        "frac_original_end": post[-1],
        "recovered": rec is not None,
        "recovery_round": None if rec is None else rec + 1,
        "half_time": next((i + 1 for i, x in enumerate(post) if x >= 0.5), None),
        "short_at_removal": at(run["series_short"], rem - 1), "short_T": at(ps, T - 1),
        "long_at_removal": at(run["series_long"], rem - 1), "long_T": at(pl, T - 1),
    }
    out["delta_original"] = out["frac_original_T"] - out["frac_original_at_removal"]
    out["delta_short"] = None if out["short_T"] is None else out["short_T"] - out["short_at_removal"]
    out["delta_long"] = None if out["long_T"] is None else out["long_T"] - out["long_at_removal"]
    return out


ARMS = {
    "A0_no_purge": "committed agents stay for the whole recovery phase (negative control)",
    "A1_purge": "committed agents removed perfectly at the end of takeover; honest memories untouched",
    "A2_purge_wipe": "as A1, plus every surviving honest agent's memory is emptied at removal (broad reset)",
}


def run_episode(task_id: int, seed: int, world: str, dose: float, arms: list, cfg: dict,
                memory=MEMORY_FULL, policy=scripted_policy, backend: str = "scripted") -> list:
    t = task(task_id)
    out = []
    t0 = time.perf_counter()
    ctx = {"task": t, "seed": seed, "memory": memory, "calls": 0, "cost_usd": 0.0, "low_mass": 0}
    try:
        prefix = simulate_prefix(t, seed, world, dose, memory, cfg, policy, ctx)
        pre_err = None
    except Exception as e:  # noqa: BLE001
        prefix, pre_err = None, f"{type(e).__name__}: {e}"
    prefix_wall = time.perf_counter() - t0
    for arm in arms:
        t1 = time.perf_counter()
        ctx["arm"] = arm
        if pre_err is None:
            try:
                run = simulate_arm(prefix, t, seed, arm, cfg, policy, ctx)
                ev = evaluate(t, run, cfg)
                ok, err = True, None
            except Exception as e:  # noqa: BLE001
                run, ev, ok, err = None, None, False, f"{type(e).__name__}: {e}"
        else:
            run, ev, ok, err = None, None, False, pre_err
        out.append({
            "task_id": task_id, "seed": seed, "world": world, "dose": dose,
            "memory": memory_label(memory), "memory_spec": memory_spec(memory), "arm": arm,
            "backend": backend, "cfg": cfg, "words": t["words"],
            "trajectory": run, "evaluation": ev,
            "validity": {"ok": ok, **({} if ok else {"error": err})},
            "cost_actual": {"wall_s": round(time.perf_counter() - t1 + prefix_wall / len(arms), 6),
                            "model_calls": ctx["calls"], "cost_usd": round(ctx["cost_usd"], 6),
                            "low_mass_calls": ctx["low_mass"]},
        })
    return out
