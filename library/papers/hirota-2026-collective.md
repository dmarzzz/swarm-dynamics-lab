---
id: hirota-2026-collective
type: paper
title: Collective Regimes in Multi-Agent LLMs under Reasoning Effort and Communication Topology
authors:
- Machiko Hirota
- Akshara Nadayanur Sathis Kanna
- Ujwal Kumar
- Phan Xuan Tan
year: 2026
venue: arXiv preprint (under review at ICLR 2027)
url: https://arxiv.org/abs/2609.35885
doi: null
arxiv: '2609.35885'
cite: Hirota, M., Kanna, A. N. S., Kumar, U., & Tan, P. X. (2026). Collective Regimes in Multi-Agent LLMs under Reasoning Effort and Communication Topology. arXiv preprint arXiv:2609.35885.
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Panels of N = 50 stateless LLM agents repeatedly update a prediction after seeing only their locally visible peers on a ring-like communication graph. Measuring both global agreement and local (neighbour) agreement, the authors identify three collective regimes borrowed from coupled-oscillator theory: synchronised (global consensus), twisted (locally ordered but globally incoherent, like twisted states of Kuramoto rings) and chimera-like (coherent and incoherent subpopulations coexist). Raising gpt-5-mini's reasoning effort moves panels from fragmented outcomes to locally ordered twisted states, while increasing connectivity drives them toward global synchronisation; fragmentation collapses faster as the graph's algebraic connectivity grows. In 40% of trials with low spatial heterogeneity (Delta Z < 0.03) a twisted configuration persists through the final 20 turns.

## Contribution

Brings the order-parameter vocabulary of the Kuramoto/swarmalator literature (synchronised, twisted, chimera states; algebraic connectivity) into LLM deliberation panels, and shows that aggregate agreement alone mischaracterises collective LLM behaviour. Closest analogues: [[de-marzo-2024-ai]] (global coupling, Curie-Weiss) and [[riedl-2025-emergent]] (information-theoretic emergence).

## Key results

- Claimed (abstract): three regimes (synchronised, twisted, chimera-like) observed in N = 50 panels.
- Claimed: reasoning effort and topology control different aspects: effort promotes local order, connectivity promotes global synchronisation.
- Claimed: fragmentation decays faster with larger algebraic connectivity across rewired graphs; topology effect reproduces on a non-circular judging task and across models from three providers.
- Claimed: 40% of trials with Delta Z < 0.03 remain twisted for the last 20 turns.

## Methods and models

Stateless agents updating predictions from visible neighbours on rewired ring-type graphs; global and local agreement measures (including a spatial heterogeneity statistic Delta Z); gpt-5-mini at several reasoning-effort settings plus models from two other providers. Details beyond the abstract not checked.

## Limitations and open questions

Read at abstract level only. Unclear how predictions are scored, whether results depend on prompt framing, and how the "twisted" label is operationalised for non-phase variables. Very recent (Sept 2026) and not yet peer reviewed.

## Relevance to us

Very high: a direct bridge between LLM swarms and the sync-consensus physics we already catalogue (Kuramoto, chimeras). A hackathon replication on SwarmBench-like grids or simple rings is cheap. Read in full next. Related: [[de-marzo-2024-ai]], [[wang-2025-rethinking]], [[ricco-2026-consensus]].
