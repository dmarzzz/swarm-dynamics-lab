---
id: panerati-2021-learning
type: paper
title: "Learning to Fly—a Gym Environment with PyBullet Physics for Reinforcement Learning of Multi-agent Quadcopter Control"
authors: ["Jacopo Panerati", "Hehui Zheng", "SiQi Zhou", "James Xu", "Amanda Prorok", "Angela P. Schoellig"]
year: 2021
venue: "2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)"
url: https://arxiv.org/abs/2103.02142
doi: 10.1109/IROS51168.2021.9635857
arxiv: "2103.02142"
cite: "Panerati, J., Zheng, H., Zhou, S., Xu, J., Prorok, A., & Schoellig, A. P. (2021). Learning to Fly—a Gym Environment with PyBullet Physics for Reinforcement Learning of Multi-agent Quadcopter Control. 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 7512-7519."
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "182 (Crossref, 2026-10-03)"
code: [gh-learnsyslab-gym-pybullet-drones]
---

## Summary

Introduces gym-pybullet-drones, an OpenAI Gym-style environment for one or more Crazyflie quadcopters on the Bullet physics engine, with realistic collisions, ground effect, drag and downwash, kinematic and vision observations (RGB, depth, segmentation), single-agent RL via Stable Baselines3, multi-agent RL via RLlib, and a ROS2 wrapper, aiming to let control theory and RL be compared on one platform.

## Contribution

Claimed by the authors as the first open multi-quadcopter Gym environment combining multi-agent and vision-based RL interfaces with realistic aerodynamic effects.

## Key results

- Table II speed-ups versus wall clock: 1 drone, 1 environment, no vision: 16.8x (TinyRenderer, 2020 MacBook Pro CPU) and 15.5x (OpenGL3, Lenovo P52 GPU); 80 drones across 4 environments: 0.95x and 0.8x; vision-based observations cut the factor sharply (e.g. 1.3x and 10.8x for one vision drone).
- Examples include PID trajectory tracking, multi-robot flight with downwash, and single- and two-agent RL stabilisation tasks.

## Methods and models

PyBullet rigid-body physics at 240 Hz with control at 48 Hz in the examples; Crazyflie 2.x models identified from literature; Gym API with dictionaries per drone for multi-agent tasks.

## Limitations and open questions

Skimmed (abstract, intro, features, performance table). CPU-bound; scale to 80 drones is around real time. No communication-channel model; neighbourhood is a distance-thresholded adjacency matrix.

## Relevance to us

My own run of the current code ([[gh-learnsyslab-gym-pybullet-drones]]) got about 4,900 drone-control-steps/s, i.e. 50 drones at 2x real time on an M1 Max, consistent with this table. For larger swarms the same lab's JAX simulator [[gh-learnsyslab-crazyflow]] is the follow-up.
