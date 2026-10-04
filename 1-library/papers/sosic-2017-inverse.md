---
id: sosic-2017-inverse
type: paper
title: Inverse Reinforcement Learning in Swarm Systems
authors:
- Adrian Šošić
- Wasiur R. KhudaBukhsh
- Abdelhak M. Zoubir
- Heinz Koeppl
year: 2017
venue: Proceedings of the 16th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2017)
url: https://arxiv.org/abs/1602.05450
doi: null
arxiv: '1602.05450'
cite: Šošić, A., KhudaBukhsh, W. R., Zoubir, A. M., & Koeppl, H. (2017). Inverse reinforcement learning in swarm systems. In Proceedings of the 16th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2017). arXiv:1602.05450.
topics:
- marl-emergence
- collective-motion
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

The paper introduces the swarMDP, a homogeneous sub-class of Dec-POMDPs, and shows that because agents are identical their value functions coincide, which reduces multi-agent inverse RL to a single-agent problem. A heterogeneous learning scheme solves the control step. On two example systems it recovers local reward models from observed collective dynamics that reproduce the global behaviour.

## Contribution

Formal backbone (the swarm MDP) later used by [[huttenrauch-2019-deep]], and an early proposal to infer the objectives behind observed collective motion rather than its rules.

## Key results

- Local reward models that reproduce observed global dynamics on two example systems (claimed in abstract; systems include a Vicsek-type model according to later citations, not checked).

## Methods and models

swarMDP definition, value-function equivalence proof, IRL with a heterogeneous learning scheme. Abstract-level read.

## Limitations and open questions

Small examples; identifiability of rewards from collective data is not addressed in the abstract.

## Relevance to us

The "infer the reward that a real flock optimises" question is a natural hackathon project using tracking data (see dataset entries from the collective-motion scan). Related: [[durve-2020-learning]], [[huttenrauch-2019-deep]].
