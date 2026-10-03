---
id: tadevosyan-2025-attentionswarm
type: paper
title: "AttentionSwarm: Reinforcement Learning with Attention Control Barrier Function for Crazyflie Drones in Dynamic Environments"
authors: ["Grik Tadevosyan", "Valerii Serpiva", "Aleksey Fedoseev", "Roohan Ahmed Khan", "Demetros Aschu", "Faryal Batool", "Nickolay Efanov", "Artem Mikhaylov", "Dzmitry Tsetserukou"]
year: 2025
venue: "2025 IEEE International Conference on Robotics and Biomimetics (ROBIO)"
url: https://arxiv.org/abs/2503.07376
doi: "10.1109/robio66223.2025.11377435"
arxiv: null
cite: "Tadevosyan, G., Serpiva, V., Fedoseev, A., Khan, R. A., Aschu, D., Batool, F., Efanov, N., Mikhaylov, A., & Tsetserukou, D. (2025). AttentionSwarm: Reinforcement Learning with Attention Control Barrier Function for Crazyflie Drones in Dynamic Environments. In 2025 IEEE International Conference on Robotics and Biomimetics (ROBIO) (pp. 764-769). IEEE. (arXiv:2503.07376)"
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "1 (Crossref, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

AttentionSwarm is a benchmark and controller for safe swarm flight in a dynamic multi-drone racing scenario. An attention model weights nearby obstacles and agents, and control barrier functions enforce collision-free constraints in real time, combined with RL. Tested indoors on Crazyflie 2.1 quadrotors with Vicon localisation, it reports a 95-100% collision-free navigation rate.

## Contribution

A small-scale example of attention plus CBF safety layering on learned drone-swarm control.

## Key results

- 95-100% collision-free navigation in a dynamic multi-agent drone racing environment (measured, per the abstract).

## Methods and models

Attention-weighted CBF safety filter with RL, Crazyflie 2.1 plus Vicon. The arXiv title misspells 'Barrier' as 'Barier'; I use the corrected ROBIO title.

## Limitations and open questions

Abstract-depth entry. Motion capture, small swarm, racing-specific.

## Relevance to us

Minor; a safety-layer example alongside [[zhang-2025-gcbf]].
