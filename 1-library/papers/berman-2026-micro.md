---
id: berman-2026-micro
type: paper
title: Micro-Swarm Locomotion Optimization in Dynamic Flow using Multi-Objective Multi-Agent Reinforcement Learning
authors:
- Josef Berman
- Oren Gal
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.25025
doi: null
arxiv: '2605.25025'
cite: Berman, J., & Gal, O. (2026). Micro-swarm locomotion optimization in dynamic flow using multi-objective multi-agent reinforcement learning. arXiv preprint arXiv:2605.25025.
topics:
- marl-emergence
- swarm-robotics
- active-matter
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Sixteen simulated magnetically actuated micro-robots navigate a pulsatile arterial flow in a 2 mm channel, with an incompressible Navier-Stokes solver coupled to decentralised PPO and rewards for upstream progress, energy efficiency and smoothness. Conflicting objectives are reconciled with PCGrad gradient surgery, without which energy and smoothness rewards collapse. The trained swarm shows three behaviours not encoded in the reward: hydrodynamic throttling formations, a ratchet synchronised with flow reversals, and individualised final approaches.

## Contribution

A 2026 example extending the CFD-plus-RL programme of [[verma-2018-efficient]] to a 16-agent decentralised swarm with multi-objective rewards.

## Key results

- Progress reward 6.5-7.0, energy efficiency 0.63-0.65, smoothness 0.97-0.99; more than 8 reward units above brute-force baselines on progress (claimed in abstract).

## Methods and models

CFD coupled with decentralised multi-objective PPO and PCGrad. Abstract-level read.

## Limitations and open questions

Preprint; single geometry; small swarm.

## Relevance to us

Evidence that physically coupled swarms yield unrewarded emergent formations; fluid-mediated coordination. Related: [[verma-2018-efficient]], [[gazzola-2016-learning]].
