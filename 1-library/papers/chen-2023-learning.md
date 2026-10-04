---
id: chen-2023-learning
type: paper
title: Learning Decentralized Flocking Controllers with Spatio-Temporal Graph Neural Network
authors:
- Siji Chen
- Yanshen Sun
- Peihan Li
- Lifeng Zhou
- Chang-Tien Lu
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2309.17437
doi: null
arxiv: '2309.17437'
cite: Chen, S., Sun, Y., Li, P., Zhou, L., & Lu, C.-T. (2023). Learning decentralized flocking controllers with spatio-temporal graph neural network. arXiv preprint arXiv:2309.17437.
topics:
- marl-emergence
- swarm-robotics
- collective-motion
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

GNN controllers that use only immediate neighbours fail to imitate centralised flocking, and adding L-hop delayed states can leave distant flock members without consensus, forming small clusters. A spatio-temporal GNN combines spatial expansion (delayed states from distant neighbours) with temporal expansion (past states of immediate neighbours), is trained by imitation of an expert, and achieves cohesive flocking, leader following and obstacle avoidance in simulation and on Crazyflie drones.

## Contribution

Improves on [[tolstaya-2020-learning]] by adding temporal memory to graph controllers; still imitation rather than RL.

## Key results

- Better emulation of the global expert and cohesive flocking on real Crazyflies (claimed in abstract).

## Methods and models

Spatio-temporal GNN, imitation learning from a centralised expert. Abstract-level read.

## Limitations and open questions

Needs an expert controller; preprint.

## Relevance to us

Memory in learned flocking controllers; relevant to whether temporal information improves learned collective motion. Related: [[tolstaya-2020-learning]], [[batra-2022-decentralized]].
