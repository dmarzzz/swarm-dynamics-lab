---
id: choi-2026-communication
type: paper
title: "Communication-Free Collective Navigation for a Swarm of UAVs via LiDAR-Based Deep Reinforcement Learning"
authors: ["Myong-Yol Choi", "Hankyoul Ko", "Hanse Cho", "Changseung Kim", "Seunghwan Kim", "Jaemin Seo", "Hyondong Oh"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/html/2601.13657v1
doi: null
arxiv: "2601.13657"
cite: "Choi, M.-Y., Ko, H., Cho, H., Kim, C., Kim, S., Seo, J., & Oh, H. (2026). Communication-Free Collective Navigation for a Swarm of UAVs via LiDAR-Based Deep Reinforcement Learning. arXiv preprint arXiv:2601.13657."
topics: [swarm-robotics, collective-motion, marl-emergence, collective-decision]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "2 (Semantic Scholar, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

A five-quadrotor swarm navigates cluttered indoor and outdoor scenes with no inter-agent communication and no external positioning. Only one leader knows the goal. The followers do not know which robot is the leader. Each follower runs a PPO policy, trained in Isaac Sim/OmniDrones, that maps its own velocity and attitude, the relative states of up to six LiDAR-tracked neighbours, and a 2-channel LiDAR occupancy grid to a velocity command. Because the policy learns cohesion and separation (alignment is deliberately left out), the group follows the leader implicitly. This is the Couzin et al. (2005) informed-minority mechanism realised with a learned controller. In simulation the policy beats two bio-inspired baselines and an imitation expert, most clearly in forests.

## Contribution

The paper claims the first real-world, communication-free, LiDAR-only collective navigation by DRL. It moves the informed-leader result from fish and model agents onto physical UAVs with a learned rather than hand-tuned interaction rule, and benchmarks it against hand-designed vision-based flocking (VPF, PACNav) under identical perception.

## Key results

- Simulation, 5 UAVs, 100 trials per condition (measured, Table III), success rate for proposed vs PACNav vs VPF vs DAgger-expert: dense pillars (5 m gaps) 97 / 82 / 27 / 69%; simplified forest 97 / 38 / 6 / 34%; realistic forest 72 / 31 / 5 / 22%. The proposed policy also gives the tightest flock (radius 1.39-1.61 m) and the highest alignment (0.88-0.94), although alignment is not rewarded.
- Scaling with one 5-agent-trained model (measured, Table IV): obstacle-free success 100% for 2-6 followers, 98% for 8, 93% for 10. With 5 m gaps it drops to 56% (8 followers) and 46% (10). Flock radius grows from 1.04 m to 2.33 m and alignment falls from 0.97 to 0.83 as followers go from 2 to 10. The authors attribute the failures to geometry: a horizontally spread flock of diameter about 4.6 m meets 5 m gaps.
- Topological neighbour count (measured, 11 UAVs): success saturates at 94% with 4 neighbours without obstacles. In dense obstacles, going from 5 to 6 neighbours raises success from 26% to 46%, and going from 6 to 10 adds only 4 points. The chosen value of 6 echoes the topological interaction range of starlings.
- Reward ablation (measured): without the flocking reward success is 0% (followers hover). Without the stable-flight (altitude) term it is 3-11%, because neighbours leave the LiDAR's limited vertical field of view.
- Real world (measured, one trial per scene, 5 UAVs): collision-free in 2 indoor and 3 outdoor scenes. Mean minimum separation is 1.34-1.55 m. Alignment is 0.48-0.52 indoors and 0.72-0.81 outdoors. LiDAR neighbour detection rate is 100% and precision 99.2% within the field of view.

## Methods and models

- Perception: Livox Mid-360 LiDAR on 250 mm quadrotors with Jetson Orin NX and Pixhawk 6C. Neighbours wear retro-reflective tape. Intensity-gated points are clustered with DBSCAN, tracked with a constant-velocity EKF and validated by intensity ratio. Ego-state comes from FAST-LIO2. Detection is reliable out to about 10 m.
- POMDP, PPO with GAE. Observation is a 7-d ego state (velocity, quaternion), 6 neighbours x 7 (relative position, relative velocity, mask) and a 2-channel occupancy grid. Action is a 3-d velocity command. Position is deliberately excluded so the policy cannot learn map-specific correlations.
- Reward: 1.5 x flocking (separation penalty below 1.6 m, cohesion penalty beyond 2.0 m from the local centre of mass) + 2.0 x obstacle (proximity and approach direction within 3 m) + 1.0 x stable flight (match the leader's altitude, stay upright) + 1.0 x neighbour perception (keep neighbours in the field of view, descend to reacquire when all are lost) + a terminal collision penalty.
- Training: 512 parallel environments, 500 M steps, randomly placed pillars, goal sampled on a 30 m circle. Simulated perception noise, field-of-view limits, occlusion and 0.1-0.2 s latency. The leader uses RRT plus an artificial potential field.
- Baselines re-implemented on the same LiDAR perception: PACNav (path persistence and similarity), VPF (visual projection field) and the expert of a DAgger visuomotor method.
- No code link is given in the paper.

## Limitations and open questions

- Real-world validation is a single trial per environment with 5 UAVs, so there are no real-world success-rate statistics.
- Scalability is limited by a 2-D (horizontal) formation imposed by the LiDAR's narrow vertical field of view. Directional consensus degrades with N. The authors flag this as the main open problem.
- Excluding alignment is a design choice for leader-following. Its effect on collective order (for example a polarisation transition) was not explored.
- Leader identity is implicit but there is only ever one leader. Multiple informed individuals with conflicting goals (Couzin-style consensus) were not tested.

## Relevance to us

This is direct evidence that a learned local rule can reproduce informed-minority leadership on physical drones. It is a natural bridge between the collective-decision literature ([[couzin-2005-effective]]) and learned swarm control ([[huang-2024-collision]], [[zhang-2025-learning]]). The neighbour-count ablation gives a robot-side counterpart to topological-interaction findings in birds ([[ballerini-2008-interaction]]). Hackathon idea: add a second informed leader with a conflicting goal and measure whether the learned followers show the consensus/split bifurcation predicted by the Couzin model.
