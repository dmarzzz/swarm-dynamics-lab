# Toy: one-vote-per-identity governance; attacker mints Sybils at a cost per step.
import time, random
from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend

initial_state = {"honest": 100, "sybils": 0, "attacker_budget": 50.0, "captured": False}
params = {"identity_cost": [0.5, 1.0, 2.0], "detect_rate": [0.0, 0.1]}

def p_mint(params, substep, history, state):
    n = int(state["attacker_budget"] // params["identity_cost"]) if state["attacker_budget"] > 0 else 0
    n = min(n, 10)
    return {"mint": n}

def s_sybils(params, substep, history, state, inp):
    survivors = sum(1 for _ in range(state["sybils"]) if random.random() > params["detect_rate"])
    return "sybils", survivors + inp["mint"]

def s_budget(params, substep, history, state, inp):
    return "attacker_budget", state["attacker_budget"] - inp["mint"] * params["identity_cost"]

def s_captured(params, substep, history, state, inp):
    return "captured", (state["sybils"] + inp["mint"]) > state["honest"] * 0.5

psubs = [{"policies": {"mint": p_mint}, "variables": {"sybils": s_sybils, "attacker_budget": s_budget, "captured": s_captured}}]
model = Model(initial_state=initial_state, state_update_blocks=psubs, params=params)
sim = Simulation(model=model, timesteps=20, runs=20)
t = time.time()
exp = Experiment([sim]); exp.engine = Engine(backend=Backend.SINGLE_PROCESS)
res = exp.run()
print("rows", len(res), "secs", round(time.time() - t, 2))
import pandas as pd
df = pd.DataFrame(res)
last = df[df.timestep == 20]
print(last.groupby(["subset"]).agg(sybils=("sybils", "mean"), captured=("captured", "mean")))
print(df[["subset","run"]].drop_duplicates().shape)
