---
id: zou-2026-waggle
type: paper
title: 'Waggle: Learning One Anonymous Local Law for Self-Organizing LLM Swarms'
authors:
- Mingxi Zou
- Wei Zhu
- Zhuo Wang
- Langzhang Liang
- Zhiwen Tang
- Yinghui Xu
- Zenglin Xu
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.34136
doi: null
arxiv: '2609.34136'
cite: 'Zou, M., Zhu, W., Wang, Z., Liang, L., Tang, Z., Xu, Y., & Xu, Z. (2026). Waggle: Learning One Anonymous Local Law for Self-Organizing LLM Swarms. arXiv preprint arXiv:2609.34136.'
topics:
- llm-agent-swarms
- swarm-intelligence
- marl-emergence
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (Semantic Scholar, 2026-10-03); not in OpenAlex as of 2026-10-03
code: []
---

## Summary

Instead of learning roles, hierarchies, routing or communication topologies for LLM multi-agent systems, Waggle learns a single shared, anonymous local law: a policy over bounded local views that jointly selects task actions, semantic messages and local commitment updates, executed identically by interchangeable agents. Coordination forms, persists and reorganises through repeated execution of the same law, without explicit roles or global topology. Training uses Swarm-Consistent Distillation, combining anonymous-orbit consistency (permutation symmetry) with rollout-grounded prediction of the next local coordination field. The same learned law remains effective as populations and interaction budgets change, retains over 96% of substrate-specific oracle quality, transfers without retraining, and improves reorganisation after counterevidence.

## Contribution

The most explicitly "swarm-like" design in the 2026 LLM-MAS literature: identical anonymous agents with a learned local rule, the LLM analogue of a Boids or Vicsek update rule. Contrasts with topology-learning approaches such as [[zhang-2024-g-designer]] and [[tastan-2026-stochastic]].

## Key results

- Claimed: >96% of substrate-specific oracle quality retained; robust to changes in population size and interaction budget; zero-shot transfer.
- Claimed: better reorganisation after counterevidence with SCD.

## Methods and models

Shared policy over bounded local views; Swarm-Consistent Distillation (anonymous-orbit consistency plus next-local-field prediction). Tasks and base models not checked.

## Limitations and open questions

Abstract-level read; very recent; definition of "coordination field" and test tasks need the full text.

## Relevance to us

Conceptually central for a hackathon framed around swarm dynamics: it is a learned local rule we could analyse with collective-motion order parameters. Related: [[ruan-2025-benchmarking]], [[li-2025-swarmsys]].
