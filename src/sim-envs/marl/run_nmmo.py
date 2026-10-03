import time, nmmo, numpy as np
from nmmo.core.config import Default
cfg = Default()
print("PLAYER_N", cfg.PLAYER_N, "MAP_SIZE", cfg.MAP_SIZE, "HORIZON", cfg.HORIZON)
env = nmmo.Env(cfg)
t=time.time(); obs, info = env.reset(seed=1); print("reset s", round(time.time()-t,2), "agents", len(obs))
a0 = list(obs.keys())[0]
print("obs keys", list(obs[a0].keys()))
print("action space keys", list(env.action_space(a0).keys()) if hasattr(env.action_space(a0),'keys') else env.action_space(a0))
steps=0; agent_steps=0; t=time.time()
while time.time()-t < 60 and env.agents:
    acts = {a: env.action_space(a).sample() for a in env.agents}
    obs, r, term, trunc, info = env.step(acts)
    steps+=1; agent_steps+=len(acts)
dt=time.time()-t
print(f"steps {steps} agent_steps {agent_steps} env_steps/s {steps/dt:.1f} agent_steps/s {agent_steps/dt:.1f} alive {len(env.agents)}")
