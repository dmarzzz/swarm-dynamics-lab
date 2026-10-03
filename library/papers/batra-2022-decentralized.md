---
id: batra-2022-decentralized
type: paper
title: Decentralized Control of Quadrotor Swarms with End-to-end Deep Reinforcement Learning
authors:
- Sumeet Batra
- Zhehui Huang
- Aleksei Petrenko
- Tushar Kumar
- Artem Molchanov
- Gaurav S. Sukhatme
year: 2022
venue: Proceedings of the 5th Conference on Robot Learning (CoRL 2021), PMLR 164
url: https://arxiv.org/abs/2109.07735
doi: null
arxiv: '2109.07735'
cite: Batra, S., Huang, Z., Petrenko, A., Kumar, T., Molchanov, A., & Sukhatme, G. S. (2022). Decentralized control of quadrotor swarms with end-to-end deep reinforcement learning. In Proceedings of the 5th Conference on Robot Learning, PMLR 164, 576–586.
topics:
- marl-emergence
- swarm-robotics
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Fully decentralised neural policies for individual quadrotors, trained with large-scale multi-agent end-to-end RL in simulation with realistic quadrotor physics, transfer zero-shot to real drones. In simulation the policies show flocking, aggressive manoeuvres in tight formation with collision avoidance, breaking and re-forming formations around moving obstacles, and pursuit-evasion coordination. Real-robot deployment shows station keeping and goal swapping on resource-constrained quadrotors.

## Contribution

Demonstrates that MARL swarm policies can go sim-to-real on aerial robots from raw thrust-level control, beyond the kinematic agents of [[huttenrauch-2019-deep]].

## Key results

- Zero-shot sim-to-real transfer for station keeping and goal swapping (claimed in abstract).
- Architecture and training-regime ablations in simulation (not read).

## Methods and models

End-to-end deep RL with neighbour-encoding networks on simulated quadrotor dynamics; project site https://sites.google.com/view/swarm-rl. Abstract-level read; code repository not opened.

## Limitations and open questions

Real-world experiments cover simpler behaviours than simulation; swarm sizes small in hardware.

## Relevance to us

Best reference if a team wants learned swarm behaviour on drones. Related: [[tolstaya-2020-learning]], [[de-souza-2021-decentralized]], [[orr-2023-multi]].
