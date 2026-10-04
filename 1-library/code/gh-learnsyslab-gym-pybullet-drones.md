---
id: gh-learnsyslab-gym-pybullet-drones
type: code
title: "gym-pybullet-drones: PyBullet Gymnasium environments for single- and multi-quadcopter control and RL (Crazyflie models)"
repo: learnsyslab/gym-pybullet-drones
url: https://github.com/learnsyslab/gym-pybullet-drones
authors: ["Jacopo Panerati", "Hehui Zheng", "SiQi Zhou", "James Xu", "Amanda Prorok", "Angela P. Schoellig"]
year: 2020
language: Python
license: "MIT"
stars: 2150
last_commit: 2026-09-06
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: [panerati-2021-learning]
---

## Summary

One line: rigid-body quadcopter physics (PyBullet, Crazyflie CF2X/CF2P models, optional ground effect, drag and downwash) for N drones, each observing its own state with a distance-thresholded adjacency matrix, controlled by PID or RL policies; measured here about 4,900 drone-control-steps/s at 48 Hz control (5 physics substeps each), so 10 drones run 10x faster than real time and 50 drones 2x on one M1 Max core; no LLM integration; no adversarial hooks (but any drone's action can be overridden in the step loop); light to run (pip, but pybullet must compile from source on Python 3.12, about 70 s).

Maintained by the Learning Systems Lab (Panerati); the README says it is tested on Apple Silicon/macOS 26 and Ubuntu 24.04, works with Stable-Baselines3 2.0 and Betaflight SITL (Ubuntu only). The original IROS 2021 code is on the paper/master branches. The lab now points to [[gh-learnsyslab-crazyflow]] for GPU/JAX and to safe-control-gym for constrained control.

## What it can do for us

A credible physics layer for a small drone swarm (tens of agents) where a policy, a scripted adversary or an LLM planner sends set-points. Downwash and collisions make physical interference attacks (a faulty drone pushing others) testable, which point-mass sims cannot show.

## Run notes

git clone https://github.com/learnsyslab/gym-pybullet-drones.git gpd && cd gpd && uv venv -p 3.12 .venv && uv pip install -p .venv/bin/python -e . (Python 3.11 is rejected: the package requires >=3.12; pybullet built from source, 68 s). Benchmark script (mine): CtrlAviary(drone_model=CF2X, num_drones=N, physics=PYB, pyb_freq=240, ctrl_freq=48, gui=False, obstacles=False) with one DSLPIDControl per drone holding a grid of drones 1 m above their start, stepped for 5 simulated seconds with no real-time sync. 2026-10-03, M1 Max: N=1, 0.06 s wall (82x real time, 3,921 drone-ctrl-steps/s); N=10, 0.48 s (10.3x, 4,954/s); N=50, 2.46 s (2.0x, 4,875/s); N=10 with pyb_gnd_drag_dw physics, 1.07 s (4.7x, 2,241/s). Max position error at the end 0.005 m in all PYB runs; adjacency matrix with neighbourhood_radius 10 was fully connected (N^2 links).

## Limitations

CPU-bound, about linear in N, so hundreds of drones are slow; no GPU batching. Python 3.12+ only, and pybullet has no prebuilt wheel there. The neighbourhood is a distance threshold only (no communication model, latency or packet loss).
