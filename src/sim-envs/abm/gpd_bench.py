# Headless multi-drone PID hover-in-circle benchmark on gym-pybullet-drones (CtrlAviary + DSLPIDControl).
import sys, time, numpy as np
from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl
from gym_pybullet_drones.utils.enums import DroneModel, Physics
N = int(sys.argv[1]); SEC = float(sys.argv[2]); phys = Physics(sys.argv[3]) if len(sys.argv) > 3 else Physics.PYB
side = int(np.ceil(np.sqrt(N)))
xyz = np.array([[ (i % side) * 0.5, (i // side) * 0.5, 0.1] for i in range(N)])
env = CtrlAviary(drone_model=DroneModel.CF2X, num_drones=N, initial_xyzs=xyz, physics=phys,
                 neighbourhood_radius=10, pyb_freq=240, ctrl_freq=48, gui=False, record=False, obstacles=False)
ctrl = [DSLPIDControl(drone_model=DroneModel.CF2X) for _ in range(N)]
act = np.zeros((N, 4)); target = xyz + np.array([0, 0, 1.0])
steps = int(SEC * env.CTRL_FREQ); t0 = time.time()
for i in range(steps):
    obs, *_ = env.step(act)
    for j in range(N):
        act[j], _, _ = ctrl[j].computeControlFromState(control_timestep=env.CTRL_TIMESTEP, state=obs[j], target_pos=target[j])
dt = time.time() - t0
err = np.abs(np.array([obs[j][0:3] for j in range(N)]) - target).max()
adj = env._getAdjacencyMatrix().sum()
print(f"physics={phys.value} N={N} ctrl_steps={steps} sim_sec={SEC} wall={dt:.2f}s realtime_x={SEC/dt:.1f} drone-ctrl-steps/s={N*steps/dt:,.0f} max_pos_err={err:.3f}m adjacency_links={int(adj)}")
env.close()
