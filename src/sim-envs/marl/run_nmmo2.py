import time, nmmo, sys
from nmmo.core.config import Default
for N in (128, 512):
    cfg = Default(); cfg.set("PLAYER_N", N) if hasattr(cfg,'set') else setattr(cfg,'PLAYER_N',N)
    env = nmmo.Env(cfg); obs,_ = env.reset(seed=2)
    n0=len(obs); steps=0; ag=0; t=time.time()
    while steps<150 and env.agents:
        obs, r, term, trunc, info = env.step({a: env.action_space(a).sample() for a in env.agents})
        steps+=1; ag+=len(env.agents)
    dt=time.time()-t
    print(f"N={N} start_agents={n0} steps={steps} agent_steps/s={ag/dt:.0f} env_steps/s={steps/dt:.1f} alive_end={len(env.agents)}")
