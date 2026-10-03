---
id: zhang-2025-gcbf
type: paper
title: "GCBF+: A Neural Graph Control Barrier Function Framework for Distributed Safe Multiagent Control"
authors: ["Songyuan Zhang", "Oswin So", "Kunal Garg", "Chuchu Fan"]
year: 2025
venue: "IEEE Transactions on Robotics"
url: https://arxiv.org/abs/2401.14554
doi: "10.1109/tro.2025.3530348"
arxiv: null
cite: "Zhang, S., So, O., Garg, K., & Fan, C. (2025). GCBF+: A Neural Graph Control Barrier Function Framework for Distributed Safe Multiagent Control. IEEE Transactions on Robotics, 41, 1533-1552. (arXiv:2401.14554)"
topics: [swarm-robotics, sync-consensus, marl-emergence]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "50 (Crossref, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

GCBF+ introduces graph control barrier functions (GCBF), safety certificates defined on the local interaction graph, with a theory showing that a single GCBF certifies safety for an arbitrary number of agents. A GNN parameterises both the candidate GCBF and a distributed policy, and the framework can take LiDAR point clouds instead of states. On Crazyflie-like nonlinear dynamics it beats the best hand-crafted CBF method by up to 20% for up to 256 agents and leading MARL methods by up to 40% at 1,024 agents, without trading off goal reaching. Hardware tests with a drone swarm include position exchange and docking on a moving target.

## Contribution

It brings certified-style safety (control barrier functions) to learned, GNN-based swarm controllers. It is the main 'safe learned swarm' alternative to pure RL ([[huang-2024-collision]]) and a control-theory bridge to the networked-control community.

## Key results

- Up to 20% better than the best hand-crafted CBF method for up to 256 agents; up to 40% better than leading RL methods at 1,024 agents (simulation, per the abstract).
- Hardware experiments on a drone swarm: position exchange and docking on a moving target.

## Methods and models

A GNN-parameterised barrier function on the local graph, jointly trained with a distributed policy using a loss that enforces CBF conditions under input limits (per the abstract and title). The arXiv id 2401.14554 is the preprint ('GCBF+: A Neural Graph Control Barrier Function Framework for Distributed Safe Multi-Agent Control'). I keep it out of the arxiv field because the published title differs slightly.

## Limitations and open questions

Abstract-depth entry. Learned barrier functions only certify where training data cover the state space. The guarantees are empirical at scale.

## Relevance to us

Relevant if the hackathon needs safe learned swarm control or a safety layer on top of an emergent controller. Compare [[agarwal-2025-lpac]] (GNN perception-action) and [[sebastian-2025-physics]] (physics-structured MARL).
