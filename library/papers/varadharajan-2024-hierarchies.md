---
id: varadharajan-2024-hierarchies
type: paper
title: "Hierarchies define the scalability of robot swarms"
authors: ["Vivek Shankar Varadharajan", "Karthik Soma", "Sepand Dyanatkar", "Pierre-Yves Lajoie", "Giovanni Beltrame"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/html/2405.02417
doi: null
arxiv: "2405.02417"
cite: "Varadharajan, V. S., Soma, K., Dyanatkar, S., Lajoie, P.-Y., & Beltrame, G. (2024). Hierarchies define the scalability of robot swarms. arXiv preprint arXiv:2405.02417."
topics: [swarm-robotics, collective-decision]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "1 (OpenAlex W4396715347, 2026-10-03); 1 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

The authors compare three ways of organising a heterogeneous ground swarm on a "radiation cleanup" task: find targets at the arena periphery and deliver at least 10 cheap worker robots to each. In the egalitarian setup, reactive workers explore with a bug algorithm and act as beacons. In the hierarchical setup, a few expensive mapping "guide" robots explore and then lead chains of workers. In the heterogeneous setup, both explore. Using ARGoS physics simulations in urban, maze and forest maps of increasing size, plus Khepera IV and guide-robot hardware runs, they show that egalitarian swarms succeed only when the collective sensing area (density x sensing radius x speed) matches the environment. Hierarchies reach 100% success with far fewer robots. A Poisson coverage model predicts egalitarian completion times.

## Contribution

The paper makes an empirical case, with a simple stochastic-geometry model, that designed hierarchy (a few informed or capable leaders) changes how swarms scale with environment size. This challenges the egalitarian default in swarm robotics. It complements self-organised hierarchy architectures such as [[zhu-2024-self]] and informed-leader results in biology ([[couzin-2005-effective]]).

## Key results

- Egalitarian limits (measured): success goes to 100% only as worker count rises, in line with the Poisson germ-grain coverage model. Consistent success correlates with average neighbour distance below about 2x the sensing range.
- Cost scaling (measured and claimed): in the largest environment, 100% success needs 64 egalitarian robots versus 12 hierarchical (2 guides + 10 workers). The authors call this a "400% cost reduction". Example from Fig. 4: at swarm cost 64, egalitarian takes about 6,000 s versus about 533 s for a hierarchy (18 guides, 10 workers) in a 120 x 120 m arena.
- Completion time is inversely proportional to the number of explorers (guides for the hierarchy, workers for the egalitarian swarm), as the model predicts, and grows steeply with arena size.
- Heterogeneous (everyone explores) finds targets fastest but fails more often: workers get stuck and cannot relay findings.
- Egalitarian coverage bursts early and then stagnates (no memory, robots cycle). Hierarchical coverage rises steadily until all targets are found.
- Real-robot runs (measured, small scale): two guides mapped and found the target and delivered chains of 4 and 6 workers. Coverage and timing are reported as matching simulation within the reality gap.

## Methods and models

- Coverage model: robots of sensing radius $s_r$, speed $v_r$ and density $\rho$ under random mobility form a Poisson process of intensity $\lambda=2\rho s_r v_r$. The probability that a target is still undetected is $P(X>t)=e^{-\lambda t}$, so $E[X]=1/\lambda$. The arrival time of $n$ workers is Erlang$(n,\lambda)$ with $E[T_n]=n/\lambda$.
- Guides: 2D LiDAR odometry fused with a T265 stereo camera, voxblox TSDF mapping, GBPlanner exploration, a local planner, and map-layer exchange over DDS.
- Workers: Khepera IV with fisheye camera and Raspberry Pi 4, AprilTag neighbour detection, proximity and ultrasound sensors, and Swarm Gradient Bug Algorithm exploration.
- Communication: BATMAN-adv MANET, gossip with a 500 B per step quota at 10 Hz. Behaviours are written in the Buzz swarm language (one script for all robots, role-dependent triggering).
- Chain formation and following are inspired by white-stork migratory flocks, with move, wait and recover states plus stop/move broadcasts between parent and child.
- Statistics are in the supplementary tables. Simulations use ARGoS3 range-and-bearing communication.

## Limitations and open questions

- The task is chosen to favour hierarchy: delivery needs global resource allocation and memory, which reactive workers lack by construction. The result is about memory and information aggregation as much as about hierarchy.
- The hierarchy is fixed and designed. Dynamic or emergent hierarchies are left as future work.
- The real-robot validation is small. The "400%" cost figure assumes particular per-robot costs.
- Preprint at time of reading. I did not find a peer-reviewed version.

## Relevance to us

This paper gives a quantitative argument and a simple Poisson model for when a few informed or capable agents outperform a homogeneous swarm. That is directly relevant to heterogeneous agent swarms, including LLM agent swarms with orchestrators ([[rahman-2025-llm-powered]]). Pairs with [[zhu-2024-self]] (self-organised hierarchy) and [[choi-2026-communication]] (implicit single-leader guidance).

## Notes from dmarz/swarm-robotics-recent-audit

Audited 2026-10-03 against the arXiv HTML (2405.02417v1). Checked 64 egalitarian vs 12 hierarchical robots (the authors' "400% cost reduction"; note that 64 to 12 is an 81% reduction, or 5.3x fewer robots, so the authors' percentage is loosely stated), 6000 s vs 533.33 s in a 120 x 120 m arena, the 2x-sensing-range neighbour distance criterion, inverse scaling of completion time with explorers, and the 4- and 6-worker chain delivery. All match the text. No corrections needed. Citation count now from OpenAlex.
