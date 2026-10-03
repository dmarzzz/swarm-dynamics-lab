---
id: zeng-2025-decentralized
type: paper
title: "Decentralized Aerial Manipulation of a Cable-Suspended Load using Multi-Agent Reinforcement Learning"
authors: ["Jack Zeng", "Andreu Matoses Gimenez", "Eugene Vinitsky", "Javier Alonso-Mora", "Sihao Sun"]
year: 2025
venue: "Proceedings of the 9th Conference on Robot Learning (CoRL 2025), PMLR 305"
url: https://arxiv.org/abs/2508.01522
doi: null
arxiv: "2508.01522"
cite: "Zeng, J., Gimenez, A. M., Vinitsky, E., Alonso-Mora, J., & Sun, S. (2025). Decentralized Aerial Manipulation of a Cable-Suspended Load using Multi-Agent Reinforcement Learning. In Proceedings of the 9th Conference on Robot Learning, PMLR 305, 3850-3868."
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "not retrieved (no DOI; Semantic Scholar rate-limited). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

The first decentralised method for real-world 6-DoF manipulation of a cable-suspended load by a team of micro-aerial vehicles. Each MAV runs a MARL-trained outer-loop policy that needs no global state, no inter-MAV communication and no neighbour information. Agents coordinate implicitly through their observations of the shared load's pose, a stigmergy-like coupling through the payload. A new action space (linear acceleration plus body rates) with a robust low-level controller gives reliable sim-to-real transfer. Real experiments show setpoint tracking comparable to a state-of-the-art centralised controller, cooperation between heterogeneous policies, and robustness to losing one MAV in flight.

## Contribution

It shows physically mediated, communication-free coordination learned by MARL, where the object itself is the communication channel.

## Key results

- Full-pose load control with tracking comparable to the centralised state of the art (real-world, per the abstract).
- Robust to complete in-flight loss of one MAV; works with heterogeneous policies.

## Methods and models

MARL outer-loop policies per MAV; observation of load pose only; acceleration and body-rate action space; real MAV experiments.

## Limitations and open questions

Abstract-depth entry. Small teams (cable-load setups typically 3-4 MAVs).

## Relevance to us

Implicit coordination through a shared physical object links to [[arbel-2024-mechanical]] (mechanically mediated transport) and to stigmergy ideas in swarm intelligence.
