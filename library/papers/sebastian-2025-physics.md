---
id: sebastian-2025-physics
type: paper
title: "Physics-Informed Multiagent Reinforcement Learning for Distributed Multirobot Problems"
authors: ["Eduardo Sebastián", "Thai Duong", "Nikolay Atanasov", "Eduardo Montijano", "Carlos Sagüés"]
year: 2025
venue: "IEEE Transactions on Robotics"
url: https://arxiv.org/abs/2401.00212
doi: "10.1109/tro.2025.3582836"
arxiv: null
cite: "Sebastián, E., Duong, T., Atanasov, N., Montijano, E., & Sagüés, C. (2025). Physics-Informed Multiagent Reinforcement Learning for Distributed Multirobot Problems. IEEE Transactions on Robotics, 41, 4499-4517. (arXiv:2401.00212)"
topics: [swarm-robotics, marl-emergence, sync-consensus]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "33 (Crossref, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

The authors learn distributed multi-robot policies whose structure is port-Hamiltonian, respecting energy conservation and the networked nature of robot interactions. Self-attention gives a sparse policy that handles time-varying neighbourhoods, and a soft actor-critic variant trains it while accounting for inter-robot correlations without value-function factorisation. Simulations across multi-robot scenarios show better scalability than prior MARL with similar or better cumulative reward.

## Contribution

It injects physical structure (port-Hamiltonian dynamics) into MARL policies, a control-theoretic route to scalable, interpretable swarm policies.

## Key results

- Better scalability than previous MARL solutions with similar or superior performance (claimed in abstract; numbers truncated on the arXiv page I read).

## Methods and models

Self-attention port-Hamiltonian policy plus SAC-based MARL training.

## Limitations and open questions

Abstract-depth entry. Simulation scenarios (VMAS-style) only per the abstract.

## Relevance to us

An architecture alternative to [[wang-2025-local]] and [[zhang-2025-gcbf]] for learned swarm control.
