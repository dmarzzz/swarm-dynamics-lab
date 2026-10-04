---
id: chen-2025-online
type: paper
title: "Online Planning for Multi-UAV Pursuit-Evasion in Unknown Environments Using Deep Reinforcement Learning"
authors: ["Jiayu Chen", "Chao Yu", "Guosheng Li", "Wenhao Tang", "Shilong Ji", "Xinyi Yang", "Botian Xu", "Huazhong Yang", "Yu Wang"]
year: 2025
venue: "IEEE Robotics and Automation Letters"
url: https://arxiv.org/abs/2409.15866
doi: "10.1109/lra.2025.3583620"
arxiv: "2409.15866"
cite: "Chen, J., Yu, C., Li, G., Tang, W., Ji, S., Yang, X., Xu, B., Yang, H., & Wang, Y. (2025). Online Planning for Multi-UAV Pursuit-Evasion in Unknown Environments Using Deep Reinforcement Learning. IEEE Robotics and Automation Letters, 10(8), 8196-8203."
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "22 (OpenAlex W4411687934, 2026-10-03); 26 (Crossref, 2026-10-03)"
code: []
---

## Summary

A MARL approach to 3-D multi-UAV pursuit-evasion in unknown environments that respects quadrotor dynamics. An evader-prediction-enhanced network handles partial observability, and an adaptive environment generator improves exploration and generalisation during training. In simulation it beats all baselines in hard scenarios and generalises to unseen ones with a 100% capture rate. A two-stage reward refinement yields a policy that is deployed zero-shot on real quadrotors using collective-thrust and body-rate commands, which the authors call the first such RL deployment for multi-UAV pursuit-evasion.

## Contribution

Real-world, low-level-command MARL for an adversarial multi-drone task, from the Tsinghua group behind the OmniDrones simulator.

## Key results

- 100% capture rate in unseen simulated scenarios; outperforms all baselines in challenging ones (per the abstract).
- Zero-shot real-quadrotor deployment.

## Methods and models

MARL with an evader-prediction module, adaptive environment generation and two-stage reward refinement. Code and videos: https://sites.google.com/view/pursuit-evasion-rl (project page, per the abstract).

## Limitations and open questions

Abstract-depth entry. Small team sizes typical of pursuit-evasion. Task-specific.

## Relevance to us

An adversarial counterpart to cooperative learned swarms ([[huang-2024-collision]], [[wang-2025-local]]).
