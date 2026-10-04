---
id: rodriguez-2026-emergent
type: paper
title: "Emergent Coordination in Multi-Agent Systems via Pressure Fields and Temporal Decay"
authors:
- "Roland Rodriguez"
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2601.08129
doi: null
arxiv: "2601.08129"
cite: "Rodriguez, R. (2026). Emergent Coordination in Multi-Agent Systems via Pressure Fields and Temporal Decay. arXiv preprint arXiv:2601.08129."
topics:
- llm-agent-swarms
- swarm-intelligence
added_by: dmarz/llm-agent-swarms-recent-audit
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "not retrieved (OpenAlex and Semantic Scholar both HTTP 429, 2026-10-03)"
code: []
---
## Summary

Proposes replacing planner/executor and manager/worker orchestration of LLM agents with a stigmergic scheme: agents act locally on a shared artifact, guided by "pressure" gradients computed from measurable quality signals, while temporal decay of pressure prevents premature convergence (analogous to pheromone evaporation). The paper formalises this as optimisation over a pressure landscape and proves convergence under mild conditions. On meeting-room scheduling (1,350 trials), pressure-field coordination solves 48.5% of problems vs 12.6% for conversation-based coordination, 1.5% for hierarchical control and 0.4% for sequential and random baselines (all pairwise p < 0.001); disabling decay costs 10 percentage points; easy problems reach 86.7%.

## Contribution

An explicit pheromone-like coordination mechanism for LLM agents with a convergence proof and a controlled comparison against orchestration patterns. Complements [[pal-2026-swarmworld]] (stigmergy in an open world) and the swarm-intelligence-inspired frameworks [[li-2025-swarmsys]] and [[feng-2024-model]].

## Key results

- Measured (abstract): solve rate 48.5% vs 12.6% (conversation), 1.5% (hierarchical), 0.4% (sequential, random).
- Measured: temporal decay ablation reduces solve rate by 10 pp.
- Measured: performance roughly constant from 1 to 4 agents.

## Methods and models

Shared-artifact optimisation with quality-derived pressure gradients and exponential decay; meeting-room scheduling benchmark; 1,350 trials. Code link given on the arXiv page (not opened).

## Limitations and open questions

- Abstract-level read. Only 1 to 4 agents, so this says little about swarm-scale behaviour.
- One task family with an easily computed quality signal; the approach needs such a signal.
- Baselines may be weak (1.5% for hierarchical control is surprisingly low).

## Relevance to us

A small, implementable stigmergy primitive for LLM swarms; the decay parameter is a natural control knob for an exploration/exploitation sweep at larger N. Related: [[zomer-2026-unraveling]] (premature consensus in llmASO), [[kim-2025-towards]].
