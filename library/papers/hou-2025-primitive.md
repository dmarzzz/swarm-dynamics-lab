---
id: hou-2025-primitive
type: paper
title: "Primitive-Swarm: An Ultra-Lightweight and Scalable Planner for Large-Scale Aerial Swarms"
authors: ["Jialiang Hou", "Xin Zhou", "Neng Pan", "Ang Li", "Yuxiang Guan", "Chao Xu", "Zhongxue Gan", "Fei Gao"]
year: 2025
venue: "IEEE Transactions on Robotics"
url: https://arxiv.org/abs/2502.16887
doi: "10.1109/tro.2025.3573667"
arxiv: "2502.16887"
cite: "Hou, J., Zhou, X., Pan, N., Li, A., Guan, Y., Xu, C., Gan, Z., & Gao, F. (2025). Primitive-Swarm: An Ultra-Lightweight and Scalable Planner for Large-Scale Aerial Swarms. IEEE Transactions on Robotics, 41, 3629-3648. (arXiv:2502.16887)"
topics: [swarm-robotics]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "19 (OpenAlex W4410737470, 2026-10-03); 19 (Crossref, 2026-10-03); 22 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Primitive-Swarm is a decentralised, asynchronous replanner for very large quadrotor swarms. Each robot picks the cheapest collision-free trajectory from an offline library of time-optimal, dynamically feasible motion primitives (generated with a TOPP-RA-based parameterisation). Collision checking is a precomputed lookup that maps primitives to the discretised space they occupy and handles robot-obstacle and robot-robot spatio-temporal conflicts together. This turns online optimisation into a linear-complexity selection. The abstract reports under 1 ms planning in dense clutter, the shortest flight times and distances in benchmarks, real-time simulation with up to 1,000 robots, and real-world flights.

## Contribution

It pushes classical (non-learned) aerial swarm planning, from the Zhejiang FAST Lab line behind [[zhou-2022-swarm]], to the 1,000-agent scale by moving almost all computation offline. It is a strong non-learning baseline for learned controllers.

## Key results

- Planning time under 1 ms in dense environments (claimed in abstract, benchmarked in paper).
- Shortest flight time and travelled distance among compared planners (claimed in abstract).
- Real-time simulation of up to 1,000 robots and real-world flights (claimed in abstract; scale of real flights not stated there).

## Methods and models

Motion-primitive library from time-optimal path parameterisation by reachability analysis, an offline occupancy association between primitives and discretised space for fast conflict checks, and decentralised asynchronous replanning that shares trajectories. The abstract says code will be released; no repository URL was on the arXiv abstract page I read.

## Limitations and open questions

Read at abstract depth only. It relies on trajectory sharing between robots (communication), unlike the communication-free learned approaches. Primitive-library expressiveness bounds agility. Swarm-level dynamics (order, density waves) are not the object of study.

## Relevance to us

A classical, scalable baseline to compare learned swarm navigation against ([[zhang-2025-learning]], [[huang-2024-collision]]) and a sibling of [[toumieh-2024-high]].
