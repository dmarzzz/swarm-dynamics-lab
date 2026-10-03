import time, numpy as np
from pogema import pogema_v0, GridConfig
for N, size in ((64,32),(256,64),(1024,128)):
    gc = GridConfig(num_agents=N, size=size, density=0.3, obs_radius=5, max_episode_steps=256, seed=1)
    env = pogema_v0(grid_config=gc)
    obs, info = env.reset()
    t=time.time(); steps=0
    while steps<256:
        obs, r, term, trunc, info = env.step([np.random.randint(5) for _ in range(N)])
        steps+=1
        if all(term) or all(trunc): break
    dt=time.time()-t
    print(f"N={N} size={size} steps={steps} env_steps/s={steps/dt:.1f} agent_steps/s={N*steps/dt:.0f} obs_shape={np.array(obs[0]).shape}")
# LBF
import gymnasium as gym, lbforaging
env = gym.make("Foraging-8x8-2p-1f-v3"); obs,_ = env.reset(seed=0)
t=time.time(); n=0
while time.time()-t<5:
    obs, r, term, trunc, info = env.step(env.action_space.sample()); n+=1
    if term or trunc: env.reset()
print(f"LBF 8x8-2p env_steps/s={n/(time.time()-t):.0f} agent_steps/s={2*n/(time.time()-t):.0f}")
