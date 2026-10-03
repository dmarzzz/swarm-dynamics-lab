---
id: jin-2026-physics
type: paper
title: "Physics-Informed Modeling and Control of Emergent Behaviors in Robot Swarms"
authors: ["Zixuan Jin", "Wenzhuo Zhang", "Shuxian Quan", "Zirui Dong", "Fangwen Ye", "Yuchen Shi", "Cheng Xu"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.01597
doi: null
arxiv: "2606.01597"
cite: "Jin, Z., Zhang, W., Quan, S., Dong, Z., Ye, F., Shi, Y., & Xu, C. (2026). Physics-Informed Modeling and Control of Emergent Behaviors in Robot Swarms. arXiv:2606.01597."
topics: [swarm-robotics, marl-emergence, active-matter]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---
## Summary

PhySwarm represents multi-stage swarm emergence as density-field evolution under a multi-phase
advection-diffusion-reaction model (Macro-ADR), realised at the robot level by an equivalent deterministic motion
model (potential-field advection, density-gradient compensation, gated phase switching). A neural-physics
controller maps local observations and memory to bounded physical parameters and is trained with a combined
reinforcement learning and physics-informed neural network (PINN) objective that penalises macro-scale density
residuals and micro-scale motion inconsistency. Proof-of-concept missions include trail-guided foraging,
formation-reconfigurable navigation and role-adaptive search and rescue.

## Contribution

A recent attempt to unify mean-field (density) modelling and learned control for swarms with interpretable
physical parameters.

## Key results

- Claimed: generates distinct multi-stage emergent behaviours in one framework; learned density fields are
  interpretable (simulation only, from abstract).

## Methods and models

ADR density model, micro motion model, RL plus PINN training. Abstract read on arXiv (June 2026 preprint, not
peer reviewed).

## Limitations and open questions

Preprint, simulation only; no comparison numbers checked.

## Relevance to us

Recent example of the micro-macro programme of [[elamvazhuthi-2019-mean]] meeting deep RL; worth watching, not
yet load-bearing.
