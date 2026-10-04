---
id: cui-2023-scalable
type: paper
title: Scalable Task-Driven Robotic Swarm Control via Collision Avoidance and Learning Mean-Field Control
authors:
- Kai Cui
- Mengguang Li
- Christian Fabian
- Heinz Koeppl
year: 2023
venue: IEEE International Conference on Robotics and Automation (ICRA 2023)
url: https://arxiv.org/abs/2209.07420
doi: null
arxiv: '2209.07420'
cite: Cui, K., Li, M., Fabian, C., & Koeppl, H. (2023). Scalable task-driven robotic swarm control via collision avoidance and learning mean-field control. In IEEE International Conference on Robotics and Automation (ICRA 2023). arXiv:2209.07420.
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

Mean-field control turns many-agent swarm control into single-agent control of the agent distribution, so single-agent RL can be used, at the cost of assuming weak interactions. Real robots collide, which breaks the mean-field model, so the authors combine collision avoidance with learned mean-field control in one framework, prove approximation guarantees in continuous spaces with collision avoidance, and report that the method outperforms MARL and runs decentralised and open-loop in simulation and on real UAV swarms.

## Contribution

A concrete, hardware-tested use of mean-field control learning for swarms, complementing mean-field MARL ([[yang-2018-mean]]) and the MFG survey [[lauriere-2022-learning]].

## Key results

- Outperforms MARL baselines on swarm tasks; decentralised open-loop execution with collision avoidance in simulation and real UAVs (claimed in abstract).

## Methods and models

Mean-field control of the swarm distribution learned with single-agent RL, plus a collision-avoidance layer; approximation theorems. Abstract-level read.

## Limitations and open questions

Weak-interaction assumption; open-loop execution limits reactivity.

## Relevance to us

A theory-backed alternative to per-agent MARL for target-distribution tasks. Related: [[cui-2022-survey]], [[borra-2021-optimal]].
