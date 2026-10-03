---
id: damera-2026-stability
type: paper
title: 'Stability Buys Time: A Re-Keying Game for Encrypted Multi-Agent Control'
authors:
- Sai Sandeep Damera
- John S. Baras
year: 2026
venue: arXiv preprint; to appear in GameSec 2026
url: https://arxiv.org/abs/2607.12742
doi: null
arxiv: '2607.12742'
cite: 'Damera, S. S., & Baras, J. S. (2026). Stability Buys Time: A Re-Keying Game for Encrypted Multi-Agent Control. arXiv:2607.12742. To appear in GameSec 2026.'
topics:
- fork-merge-security
- swarm-robotics
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Models encrypted control of an agent fleet under a persistent threat as a two-phase game: passive reconnaissance that accumulates key leakage, then stealthy manipulation. The defender's move is re-keying, which resets accumulated leakage. At the Stackelberg equilibrium the defender re-keys at the slowest cadence that still denies the attacker, and that cadence is set by how fragile the control graph is: a marginally stable graph must re-key far more often than a well-connected one. Abstract only.

## Contribution

Connects FlipIt-style timing games to multi-agent control topology.

## Key results

- Re-key cadence depends on graph fragility (abstract).
- A window between a securability floor and a static-suffices ceiling (abstract).

## Methods and models

Two-phase Stackelberg timing game, CKKS homomorphic encryption.

## Limitations and open questions

Abstract only; control setting, not LLM agents.

## Relevance to us

- Q1 and Q2 (weak link): suggests that how often a parent should re-fork or reset children could depend on the topology of the swarm, by analogy; not tested for LLM agents.
Related: [[van-dijk-2013-flipit]], [[leslie-2015-threshold]].
