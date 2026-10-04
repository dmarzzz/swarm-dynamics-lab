---
id: zhang-2025-swarmagentic
type: paper
title: 'SwarmAgentic: Towards Fully Automated Agentic System Generation via Swarm Intelligence'
authors:
- Yao Zhang
- Chenyang Lin
- Shijie Tang
- Haokun Chen
- Shijie Zhou
- Yunpu Ma
- Volker Tresp
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2506.15672
doi: null
arxiv: '2506.15672'
cite: 'Zhang, Y., Lin, C., Tang, S., Chen, H., Zhou, S., Ma, Y., & Tresp, V. (2025). SwarmAgentic: Towards fully automated agentic system generation via swarm intelligence. arXiv preprint arXiv:2506.15672. https://doi.org/10.48550/arXiv.2506.15672'
topics:
- swarm-intelligence
- llm-agent-swarms
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Generates LLM multi-agent systems from scratch by keeping a population of candidate systems and evolving them with
language-driven, feedback-guided updates inspired by PSO, jointly optimising agent functionality and collaboration.
Given only a task description and objective, it outperforms baselines on six
open-ended tasks, including a +261.8% relative improvement over ADAS on TravelPlanner.

## Contribution

Uses PSO as a search scaffold over discrete, text-defined system designs rather than over real vectors, analogous to
[[feng-2024-model]] (PSO over model weights).

## Key results

- Claimed (abstract): beats all baselines on six tasks; +261.8% relative over ADAS on TravelPlanner.

## Methods and models

PSO-inspired population search over candidate agentic systems with feedback-guided, language-driven updates (abstract only). Project page:
https://yaoz720.github.io/SwarmAgentic/

## Limitations and open questions

Abstract-level reading; preprint. The PSO analogy is loose (no metric space), so the dynamical properties of PSO do
not carry over.

## Relevance to us

Example of swarm-intelligence vocabulary migrating into LLM agent design; check whether the "swarm" adds anything over
simple population-based search (see [[camacho-villalon-2023-exposing]] for the same question in optimisation).
