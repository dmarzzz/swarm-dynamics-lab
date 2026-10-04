"""capture-memory: binary convention, committed minority, perfect removal, recovery vs memory length.

Deterministic given (task_id, seed). Contract (templates/experiment-worker/README.md step 3):

    run_episode(task_id, seed, world, dose, arms, cfg, memory=...) -> one record per arm

Every arm and every memory length run on the SAME draws: the pairing schedule and each agent's per-round
uniform draw are keyed by (task, seed, round) and the agent index, never by arm or memory. Contrasts
across arms and across memory lengths are paired per task x seed. The three arms are identical until the
removal round, so capture status is shared by all arms of an episode.

What the policy sees: only the words its partners said to it (its memory window) and the fixed pull h
toward the established convention. The purge uses the committed flag, an oracle identity: this experiment
assumes PERFECT removal and asks only what happens afterwards. Detection, quarantine and selective repair
are vishesh's lane (researchers/vishesh/notes/swarm-immune-response); A2 is the narrow bridge to it.

Scripted policy (backend "scripted"): P(original) = [tanh(beta (m + h)) + 1] / 2, the form fitted to nine
LLMs by de-marzo-2026-conformity, applied to the magnetisation m of the agent's memory window (FIFO of
partner utterances, as in magistrali-2026-aligned; +1 = original, -1 = attack label). m = 0 for an empty
memory, so a wiped memory exposes the pull h alone. The population always starts on the label favoured by h,
so the attack pushes toward the DISFAVOURED label, which is metastable inside the spinodal
(beta > 1, |h| < h_s): that is the de-marzo stubborn-agent setting, with memory and locality added.
Committed agents always say the attack label and never update. A scripted result is a property of this
rule, not a finding about LLM agents; model.py holds the (unrun) HTTP adapter for a later paid pass.
"""
from __future__ import annotations

import math
import random
import time

WORLDS = {
    "W0_CLEAN": "inside-spinodal pair, no committed minority ever; intrinsic drift per memory length",
    "W1_INSIDE": "inside-spinodal pair (h = cfg.h_inside); k = round(dose N) agents replaced by committed ones",
    "W2_OUTSIDE": "outside-spinodal pair (h = cfg.h_outside), regime control: the attack label is not metastable",
}

MEMORY_FULL = "full"            # unbounded memory; design.yaml lists memories as [1, 5, 20, "full"]
ORIG, ATK = 1, -1               # internal label codes; the model adapter maps them onto per-task words

# Two nonsense words per task for the model backend; the scripted policy never reads them. Which word is
# the original alternates with task parity so a model's string prior is balanced (yang-2026-when).
WORDS = ["zuli", "mako", "teru", "vand", "pira", "sello", "quon", "brisk", "fenn", "olam", "ruvo", "kade"]


def task(task_id: int) -> dict:
    """The task is the cluster unit: nothing here depends on the seed."""
    r = random.Random(f"task:{task_id}")
    w = r.sample(WORDS, 2)
    return {"task_id": task_id, "words": {ORIG: w[task_id % 2], ATK: w[1 - task_id % 2]}}


# ----------------------------------------------------------------- draws (shared by every arm and memory)

def round_draws(task_id: int, seed: int, rnd: int, n: int):
    """One matching and n uniforms per round, keyed by (task, seed, round) only."""
    r = random.Random(f"round:{task_id}:{seed}:{rnd}")
    ids = list(range(n))
    r.shuffle(ids)
    return [(ids[i], ids[i + 1]) for i in range(0, n - 1, 2)], [r.random() for _ in range(n)]


def replaced(task_id: int, seed: int, n: int, k: int) -> list:
    return sorted(random.Random(f"replace:{task_id}:{seed}").sample(range(n), k))


# ----------------------------------------------------------------- agents

class Honest:
    __slots__ = ("word", "L", "mem", "count", "committed")

    def __init__(self, word: int, L):
        self.word = word
        self.L = None if L == MEMORY_FULL else int(L)
        self.mem = []
        self.count = 0                       # running sum of memory entries (+1 / -1)
        self.committed = False

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
    __slots__ = ("word", "committed")

    def __init__(self, word: int):
        self.word = word
        self.committed = True


COST_KEYS = ("calls", "retries", "prompt_tokens", "completion_tokens", "cost_usd", "parse_failures", "fuzzy_parses", "parse_retries")


def scripted_policy(m: float, cfg: dict, draw: float, ctx: dict) -> int:
    """P(original) = [tanh(beta (m + h)) + 1] / 2. Sees the memory magnetisation and the pull h only."""
    p = (math.tanh(cfg["beta"] * (m + ctx["h"])) + 1) / 2
    return ORIG if draw < p else ATK


def step(agents: dict, task_id: int, seed: int, rnd: int, cfg: dict, policy, ctx: dict) -> None:
    """One round: a random perfect matching over the agents present, both partners hear each other,
    then every honest agent decides simultaneously. The decisions are independent given the round's state, so
    a policy that sets `concurrent = True` (the HTTP adapter) has them issued in parallel threads; the scripted
    policy runs them in order. Either way the order of application is by agent index, so the result is the same."""
    n = cfg["n_agents"]
    pairs, draws = round_draws(task_id, seed, rnd, n)
    heard = {}
    for a, b in pairs:
        if a in agents and b in agents:          # after a purge some indices are gone; their partner idles
            heard[a] = agents[b].word
            heard[b] = agents[a].word
    deciders = []
    for i, w in sorted(heard.items()):
        ag = agents[i]
        if ag.committed:
            continue
        ag.hear(w)
        deciders.append(i)
    new = {}
    if getattr(policy, "concurrent", False) and len(deciders) > 1:
        import concurrent.futures as cf
        subs = {i: {**ctx, "mem": agents[i].mem, **{k: 0 for k in COST_KEYS}} for i in deciders}
        with cf.ThreadPoolExecutor(max_workers=len(deciders)) as ex:
            futs = {i: ex.submit(policy, agents[i].magnetisation(), cfg, draws[i], subs[i]) for i in deciders}
            errs = []
            for i in deciders:
                try:
                    new[i] = futs[i].result()
                except Exception as e:  # noqa: BLE001
                    errs.append(e)
        for i in deciders:                       # merge the per-call ledgers back, failures included
            for k in COST_KEYS:
                ctx[k] = ctx.get(k, 0) + subs[i][k]
        if errs:
            raise errs[0]
    else:
        for i in deciders:
            ctx["mem"] = agents[i].mem           # the model adapter reads the words; the scripted policy does not
            new[i] = policy(agents[i].magnetisation(), cfg, draws[i], ctx)
    for i, w in new.items():
        agents[i].word = w


def frac_original(agents: dict) -> float:
    hon = [ag for ag in agents.values() if not ag.committed]
    return sum(1 for ag in hon if ag.word == ORIG) / len(hon) if hon else float("nan")


def streak(series: list, thresh: float, k: int, above: bool = True) -> int | None:
    """First index at which `series` has been >= thresh (or <= thresh) for k consecutive entries."""
    run = 0
    for i, x in enumerate(series):
        hit = x >= thresh if above else x <= thresh
        run = run + 1 if hit else 0
        if run >= k:
            return i - k + 1
    return None


# ----------------------------------------------------------------- one episode: shared prefix, then one fork per arm

def clone_agents(agents: dict) -> dict:
    """Deep copy of the population at the fork point (memories are short lists)."""
    out = {}
    for i, ag in agents.items():
        if ag.committed:
            out[i] = Committed(ag.word)
        else:
            c = Honest(ag.word, MEMORY_FULL if ag.L is None else ag.L)
            c.mem, c.count = list(ag.mem), ag.count
            out[i] = c
    return out


def simulate_prefix(t: dict, seed: int, world: str, dose: float, memory, cfg: dict, policy, ctx: dict) -> dict:
    """Phases 1 and 2 (entrench, takeover until capture or the cap). Shared by every arm of an episode: the arms
    differ only at the intervention, so running the prefix once keeps them paired under ANY policy, including a
    sampled model whose draws are not keyed by round. For the scripted policy this is bit-identical to running
    the prefix inside each arm (draws depend on (task, seed, round) only); selftest checks it."""
    n = cfg["n_agents"]
    k = 0 if world == "W0_CLEAN" else round(dose * n)
    ctx["h"] = cfg["h_outside"] if world == "W2_OUTSIDE" else cfg["h_inside"]
    agents = {i: Honest(ORIG, memory) for i in range(n)}
    for ag in agents.values():
        ag.hear(ORIG)                                  # each agent has heard the convention once
    series = []                                        # honest fraction on the ORIGINAL, per round
    rnd = 0
    for _ in range(cfg["entrench_rounds"]):            # phase 1: entrench
        step(agents, t["task_id"], seed, rnd, cfg, policy, ctx); rnd += 1
        series.append(frac_original(agents))
    entrench_end = rnd
    capture_round = None                               # phase 2: takeover until capture or the cap
    if k:
        for i in replaced(t["task_id"], seed, n, k):
            agents[i] = Committed(ATK)
    cap = cfg["takeover_max_rounds"] if k else cfg["clean_takeover_rounds"]
    for _ in range(cap):
        step(agents, t["task_id"], seed, rnd, cfg, policy, ctx); rnd += 1
        series.append(frac_original(agents))
        if k:
            s = streak(series[entrench_end:], 1 - cfg["capture_frac"], cfg["capture_streak"], above=False)
            if s is not None:
                capture_round = entrench_end + s
                break
    return {"k": k, "h": ctx["h"], "agents": agents, "series": series, "rnd": rnd,
            "entrench_end": entrench_end, "capture_round": capture_round}


def simulate_arm(pre: dict, t: dict, seed: int, arm: str, cfg: dict, policy, ctx: dict) -> dict:
    """Phase 3 (intervention) and recovery for one arm, from a copy of the shared prefix state."""
    k, rnd = pre["k"], pre["rnd"]
    ctx["h"] = pre["h"]
    agents = clone_agents(pre["agents"])
    series = list(pre["series"])
    removal_round = rnd
    if k and arm in ("A1_purge", "A2_purge_wipe"):     # phase 3: intervention (oracle, perfect)
        agents = {i: ag for i, ag in agents.items() if not ag.committed}
    if k and arm == "A2_purge_wipe":
        for ag in agents.values():
            ag.wipe()
    for _ in range(cfg["recovery_rounds"]):            # then recovery
        step(agents, t["task_id"], seed, rnd, cfg, policy, ctx); rnd += 1
        series.append(frac_original(agents))
    return {"k": k, "entrench_end": pre["entrench_end"], "capture_round": pre["capture_round"],
            "captured": pre["capture_round"] is not None, "removal_round": removal_round, "rounds": rnd,
            "series_original": [round(x, 4) for x in series]}


def simulate(t: dict, seed: int, world: str, dose: float, arm: str, memory, cfg: dict, policy, ctx: dict) -> dict:
    """One arm end to end (kept for callers that want a single arm); run_episode forks the prefix instead."""
    pre = simulate_prefix(t, seed, world, dose, memory, cfg, policy, ctx)
    return simulate_arm(pre, t, seed, arm, cfg, policy, ctx)


def evaluate(t: dict, run: dict, cfg: dict) -> dict:
    """Outcome metrics. Rates are over honest agents; everything after removal is indexed from the
    removal round (round 1 = first round after the intervention)."""
    rem = run["removal_round"]
    post = run["series_original"][rem:]
    T = cfg["eval_round"]
    rec = streak(post[:T], cfg["recover_frac"], cfg["recover_streak"])
    return {
        "captured": run["captured"],
        "capture_latency": None if run["capture_round"] is None else run["capture_round"] - run["entrench_end"] + 1,
        "entrench_frac_original": run["series_original"][run["entrench_end"] - 1],
        "frac_original_at_removal": run["series_original"][rem - 1],
        "frac_original_T": post[T - 1] if len(post) >= T else float("nan"),
        "delta_original": (post[T - 1] - run["series_original"][rem - 1]) if len(post) >= T else float("nan"),
        "frac_original_end": post[-1],
        "recovered": rec is not None,
        "recovery_round": None if rec is None else rec + 1,
        "half_time": next((i + 1 for i, x in enumerate(post) if x >= 0.5), None),
    }


ARMS = {
    "A0_no_purge": "committed agents stay for the whole recovery phase (negative control)",
    "A1_purge": "committed agents removed perfectly at the end of takeover; honest memories untouched",
    "A2_purge_wipe": "as A1, plus every surviving honest agent's memory is emptied at removal (broad reset)",
}


def _fresh_ctx(t, seed, arm, memory):
    return {"task": t, "seed": seed, "arm": arm, "memory": memory, **{k: 0 for k in COST_KEYS}}


def run_episode(task_id: int, seed: int, world: str, dose: float, arms: list, cfg: dict,
                memory=MEMORY_FULL, policy=scripted_policy, backend: str = "scripted") -> list:
    """The prefix (entrench + takeover) runs once per episode and every arm forks from its end state, so
    capture status and the pre-removal trajectory are shared by all arms under any policy. Model calls and
    tokens spent on the prefix are reported once under `cost_actual.prefix`; each arm's own recovery spend is
    under `cost_actual` directly. A prefix failure invalidates every arm of the episode with the same error."""
    t = task(task_id)
    t0 = time.perf_counter()
    pctx = _fresh_ctx(t, seed, "prefix", memory)
    try:
        pre = simulate_prefix(t, seed, world, dose, memory, cfg, policy, pctx)
        perr = None
    except Exception as e:  # noqa: BLE001 - a failed episode is a recorded outcome, never retried
        pre, perr = None, f"{type(e).__name__}: {e}"
    prefix_cost = {"wall_s": round(time.perf_counter() - t0, 6), **{k: pctx[k] for k in COST_KEYS}}
    out = []
    for arm in arms:
        t1 = time.perf_counter()
        ctx = _fresh_ctx(t, seed, arm, memory)
        if perr is not None:
            run, ev, ok, err = None, None, False, perr
        else:
            try:
                run = simulate_arm(pre, t, seed, arm, cfg, policy, ctx)
                ev = evaluate(t, run, cfg)
                ok, err = True, None
            except Exception as e:  # noqa: BLE001
                run, ev, ok, err = None, None, False, f"{type(e).__name__}: {e}"
        out.append({
            "task_id": task_id, "seed": seed, "world": world, "dose": dose, "memory": memory, "arm": arm,
            "backend": backend, "cfg": cfg, "words": t["words"],
            "trajectory": run, "evaluation": ev,
            "validity": {"ok": ok, **({} if ok else {"error": err})},
            "cost_actual": {"wall_s": round(time.perf_counter() - t1, 6), "model_calls": ctx["calls"],
                            **{k: ctx[k] for k in COST_KEYS if k != "calls"}, "prefix": prefix_cost},
        })
    return out
