---
id: yamaguchi-2025-emergent
type: paper
title: Emergent Coordination and Phase Structure in Independent Multi-Agent Reinforcement Learning
authors:
- Azusa Yamaguchi
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2511.23315
doi: null
arxiv: '2511.23315'
cite: Yamaguchi, A. (2025). Emergent coordination and phase structure in independent multi-agent reinforcement learning. arXiv preprint arXiv:2511.23315.
topics:
- marl-emergence
- criticality-measurement
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Large sweeps of fully independent Q-learning over environment size L and agent density rho are summarised in a phase map with two axes, cooperative success rate and a stability index from TD-error variance. Three regimes appear: coordinated and stable, a fragile transition region, and a jammed or disordered phase, separated by a sharp "double instability ridge" linked to kernel drift (each agent's effective transition kernel shifting as others update). Removing agent identifiers eliminates drift and collapses the three-phase structure.

## Contribution

Treats the learning dynamics of MARL itself as a statistical-physics system with phases, rather than the learned behaviour; a rare bridge between MARL and the criticality toolkit.

## Key results

- Three-phase structure in (L, rho) with a sharp ridge between regimes (claimed in abstract).
- Synchronisation of agents' learning is required for sustained cooperation; identifier removal collapses the phases (claimed).

## Methods and models

Independent Q-learning on grid environments, sweeps over size and density, TD-error-variance stability index. Abstract-level read; single-author preprint, not peer reviewed.

## Limitations and open questions

Not peer reviewed; toy environments; whether the "phases" are true transitions (finite-size scaling) was not checked.

## Relevance to us

Suggests measuring order parameters and susceptibilities of the learning process, not only of the swarm. Related: [[yang-2018-mean]] (Ising via MARL), [[brambati-2025-learning]].
