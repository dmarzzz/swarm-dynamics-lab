---
id: mednikov-2026-calibrate
type: paper
title: "Calibrate Once, Fly Any Team: Residual-Grounded Low-Fidelity Training for Cooperative Drone Swarms"
authors: ["Maxim Mednikov", "Oren Gal"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.17265
doi: null
arxiv: "2609.17265"
cite: "Mednikov, M., & Gal, O. (2026). Calibrate Once, Fly Any Team: Residual-Grounded Low-Fidelity Training for Cooperative Drone Swarms. arXiv preprint arXiv:2609.17265."
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (Semantic Scholar, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

Instead of RL in a high-fidelity (HF) rigid-body simulator, whose cost and crash rate grow with team size, the authors train one shared decentralised policy in a differentiable JAX point-mass simulator. That simulator is corrected by a small per-agent residual ensemble fitted once from single-drone HF calibration flights. Across four cooperative tasks and 3 to 18 drones, the residual-corrected policy beats an uncorrected low-fidelity baseline in all combinations and a from-scratch HF policy in 22 of 24. It trails an HF-finetuned policy by a gap that narrows with team size.

## Contribution

It shows that single-agent calibration can ground multi-agent low-fidelity training, so the data budget does not compound with N. This is complementary to [[zhang-2025-learning]].

## Key results

- Beats the uncorrected low-fidelity baseline in all task x team-size combinations and the from-scratch HF policy in 22/24 (measured in simulation, per the abstract).
- The gap to the HF-finetuned policy narrows as team size grows to 18.

## Methods and models

JAX differentiable point-mass simulator, bagged residual dynamics ensemble, HF tracking by a zero-training PD controller.

## Limitations and open questions

Abstract-depth entry. Simulation only (HF simulator as 'reality'); no physical flights mentioned.

## Relevance to us

A practical recipe for cheap swarm-policy training at the hackathon; see [[zhang-2025-learning]] and [[zhang-2026-asymmetric]].
