---
id: huang-2024-collision
type: paper
title: "Collision Avoidance and Navigation for a Quadrotor Swarm Using End-to-end Deep Reinforcement Learning"
authors: ["Zhehui Huang", "Zhaojing Yang", "Rahul Krupani", "Baskın Şenbaşlar", "Sumeet Batra", "Gaurav S. Sukhatme"]
year: 2024
venue: "2024 IEEE International Conference on Robotics and Automation (ICRA)"
url: https://arxiv.org/html/2309.13285
doi: "10.1109/icra57147.2024.10611499"
arxiv: "2309.13285"
cite: "Huang, Z., Yang, Z., Krupani, R., Şenbaşlar, B., Batra, S., & Sukhatme, G. S. (2024). Collision Avoidance and Navigation for a Quadrotor Swarm Using End-to-end Deep Reinforcement Learning. In 2024 IEEE International Conference on Robotics and Automation (ICRA) (pp. 300-306). IEEE."
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "25 (Crossref, 2026-10-03); 35 (Semantic Scholar, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

The authors extend the end-to-end quadrotor-swarm RL of [[batra-2022-decentralized]] from obstacle-free space to rooms with dense random pillars. Each drone runs a decentralised policy that maps its own state, its K nearest neighbours' relative positions and velocities, and a 3x3 signed-distance-field patch of nearby obstacles directly to four rotor thrusts. Three changes make obstacle-rich training work: a replay buffer that restarts episodes just before past collisions, multi-head attention over neighbour and obstacle embeddings, and the permutation-invariant SDF obstacle encoding. The resulting policy scales in simulation and transfers zero-shot to Crazyflie 2.1 nano-quadrotors running the network on the 168 MHz microcontroller.

## Contribution

This is the first purely end-to-end DRL controller (observations to motor thrusts) for quadrotor swarms in obstacle-rich environments that transfers zero-shot to real hardware. It also shows that an attention policy small enough for a Crazyflie can be deployed. It sits between classical reactive methods (ORCA, safety barrier certificates) and imitation-learned GLAS, and it is the direct predecessor of later learned aerial-swarm work such as [[choi-2026-communication]].

## Key results

- Scale (measured, abstract): up to 32 robots at 80% obstacle density in simulation, and 8 robots at 20% obstacle density on real Crazyflies.
- Baselines (measured, Table I; 8 robots, base density): success 0.97 vs 0.99 (SBC) vs 0.75 (GLAS). Inference 5 ms vs 21 ms vs 15 ms. The method is comparable to safety barrier certificates at about 4x faster inference and beats GLAS by 22 points.
- Narrow gaps (measured): with 32 robots and obstacle size 0.8-0.85 m (gaps of 0.15-0.2 m for 0.1 m drones), the learned policy keeps working where SBC fails.
- Ablations (measured, Fig. 3; base setting 8 robots, 2 sensed neighbours, 20% density, 0.6 m obstacles in a 10 m cube): without the replay buffer the collision rate rises from 0.05 to 0.12. Removing attention as well drops success from 0.88 to 0.79 and raises collisions from 0.12 to 0.20. Replacing the SDF encoding with L-nearest obstacles drops success from 0.79 to 0.10 and training diverges. The collision replay beats prioritised level replay.
- Sensed neighbours (measured): 2 nearest neighbours is best. More neighbours lowers performance, which the authors attribute to harder learning with larger inputs. K-nearest beats range-based neighbour sets (success 0.95 vs 0.89).
- Generalisation (measured, 20 episodes, 8 robots, 20% density): success 0.83 in an unseen pursuit-evasion task and 0.85 in a goal-swap task.
- Hardware (measured, Table II): a model trained from scratch at hidden size 10 with single-head attention (1,820 parameters, 7 KB, 0.35 ms per on-board inference) beats policy distillation (success 0.88 vs 0.72, collision rate 0.04 vs 0.28) and runs on board the Crazyflie.

## Methods and models

- Robots: quadrotor dynamics simulator from [[batra-2022-decentralized]] (based on QuadSim/Sample Factory). The action is 4 normalised rotor thrusts.
- Observation: relative goal position, velocity, rotation matrix, angular velocity and altitude, plus K nearest neighbours' relative position and velocity, plus 9 SDF values (3x3 grid at 0.1 m resolution).
- Reward: distance-to-goal shaping, one-off penalties for robot-robot and robot-obstacle collisions and for proximity, and regularisers on floor contact, angular velocity, control effort and tilt.
- Learning: asynchronous decentralised IPPO (Sample Factory), with parameter sharing implied by the decentralised policy. Training uses 4 seeds and two goal modes (shared goal, random independent goals).
- Collision replay: the environment state just before each collision is saved and replayed with a set probability. States replayed too often are dropped as too hard.
- Architecture: 3 MLP encoders (self, neighbours, obstacles) with multi-head attention over neighbour and obstacle embeddings. Physical tests use Vicon at 100 Hz and a 1 kHz on-board controller, with obstacles supplied as a list for local SDF computation.
- Project page: https://sites.google.com/view/obst-avoid-swarm-rl (no code repository URL in the paper text I read).

## Limitations and open questions

- Localisation and obstacle maps are external (Vicon plus a known obstacle list). No on-board sensing.
- Static obstacles only. No safety guarantees.
- Agents are goal-reaching, not flocking: the collective behaviour is collision-free crowd navigation, and order parameters were not studied.
- The finding that 2 sensed neighbours beats more is a learning-difficulty artefact, not a statement about the information needed. This is worth contrasting with [[choi-2026-communication]], where 6 neighbours was optimal.

## Relevance to us

This paper is the reference point for model-free end-to-end swarm RL on real micro-drones, and the baseline any hackathon learned-swarm controller should beat or reproduce. It contrasts with differentiable-physics training ([[zhang-2025-learning]]) and with graph/attention policy structure ([[agarwal-2025-lpac]], [[zhang-2025-gcbf]]).
