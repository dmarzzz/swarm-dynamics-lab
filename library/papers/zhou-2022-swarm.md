---
id: zhou-2022-swarm
type: paper
title: "Swarm of micro flying robots in the wild"
authors: ["Xin Zhou", "Xiangyong Wen", "Zhepei Wang", "Yuman Gao", "Haojia Li", "Qianhao Wang", "Tiankai Yang", "Haojian Lu", "Yanjun Cao", "Chao Xu", "Fei Gao"]
year: 2022
venue: "Science Robotics"
url: https://doi.org/10.1126/scirobotics.abm5954
doi: "10.1126/scirobotics.abm5954"
arxiv: null
cite: "Zhou, X., Wen, X., Wang, Z., Gao, Y., Li, H., Wang, Q., Yang, T., Lu, H., Cao, Y., Xu, C., & Gao, F. (2022). Swarm of micro flying robots in the wild. Science Robotics, 7(66), eabm5954."
topics: [swarm-robotics]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "612 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Palm-sized, fully autonomous drones navigate as a swarm through cluttered, unknown outdoor environments such as
a dense bamboo forest, using only onboard perception, localisation and planning. The core is a decentralised
trajectory planner that jointly optimises trajectory shape and time allocation (spatial-temporal joint
optimisation) under flight efficiency, obstacle avoidance, inter-robot collision avoidance, dynamical
feasibility and swarm coordination objectives, producing a high-quality trajectory within a few milliseconds.
Field experiments include swarm flight through forest, mutual avoidance and following a human.

## Contribution

Represents the optimisation/planning approach to swarming, in contrast to the reactive rule-based flocking of
[[vasarhelyi-2018-optimized]]: coordination emerges from each drone planning against its neighbours' broadcast
trajectories. It is the most-cited recent aerial swarm paper.

## Key results

- Claimed: planner computes trajectories in milliseconds and beats benchmarks in trajectory quality and
  computing time; field demonstrations in the wild without external infrastructure.

## Methods and models

Decentralised spatial-temporal trajectory optimisation with onboard perception, localisation and control on a
palm-sized platform. Abstract read; implementation details (sensors, communication of trajectories, code
release) not checked.

## Limitations and open questions

Swarm sizes in the demonstrations are small (not checked exactly); planning-based coordination generally
requires sharing plans between robots, so this is not a communication-free swarm (inferred, not checked).

## Relevance to us

Benchmark for "how good can engineered aerial swarms get" and a contrast case to emergent flocking; compare
[[soria-2021-predictive]], [[mcguire-2019-minimal]].
