---
id: tastan-2026-stochastic
type: paper
title: Stochastic Self-Organization in Multi-Agent Systems
authors:
- Nurbek Tastan
- Samuel Horvath
- Karthik Nandakumar
year: 2026
venue: International Conference on Learning Representations (ICLR 2026)
url: https://arxiv.org/abs/2510.00685
doi: null
arxiv: '2510.00685'
cite: Tastan, N., Horvath, S., & Nandakumar, K. (2026). Stochastic Self-Organization in Multi-Agent Systems. In International Conference on Learning Representations (ICLR 2026). arXiv:2510.00685.
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 0 (OpenAlex, 2026-10-03); 9 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

SelfOrg adapts the communication structure of an LLM multi-agent system on the fly without training or an external judge. Agents first answer the query independently, then assess peers' contributions with an approximation of the Shapley value; a directed acyclic graph is built so responses flow from high-contributing agents to others, and the graph is rebuilt each round from the previous responses. The framework treats agent responses as stochastic and goes beyond task- or query-level topology optimisation. It is robust with strong and weak backbones, with the largest gains in the weak-model regime where prior topology methods collapse. The authors also show theoretically that more agents raise the chance of a correct answer and that correct responses come to dominate information flow.

## Contribution

A response-conditioned, self-organising topology for LLM collectives, in contrast to fixed or learned graphs ([[zhang-2024-g-designer]], [[zhuge-2024-language]]) and to learned local laws ([[zou-2026-waggle]]).

## Key results

- Claimed: robust gains with weak backbones where other topology methods fail.
- Theory (claimed): multiple agents increase probability of correctness; correct responses dominate information flow.

## Methods and models

Independent responses, Shapley-value approximation of contributions, per-round DAG construction, multi-round propagation. Benchmarks and models not checked.

## Limitations and open questions

Abstract-level read; compute overhead of Shapley estimation and matched-compute baselines unknown.

## Relevance to us

An adaptive-network mechanism (influence flows from reliable to less reliable agents) that resembles leadership emergence in animal groups. Related: [[grotschla-2025-agentsnet]], [[wang-2025-rethinking]].
