---
id: ricco-2026-consensus
type: paper
title: Consensus and Factual Dynamics in Large Populations of Interacting Language Models
authors:
- Emanuele Ricco
- Elia Onofri
- Vincenzo Sammartino
- Roberto Di Pietro
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.39211
doi: null
arxiv: '2609.39211'
cite: Ricco, E., Onofri, E., Sammartino, V., & Di Pietro, R. (2026). Consensus and Factual Dynamics in Large Populations of Interacting Language Models. arXiv preprint arXiv:2609.39211.
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

RHEON is a physics-inspired framework that treats a population of agents drawn from one frozen LLM as an evolving O(n) spin system on interaction geometries of increasing effective dimension, from a 1D ring to the fully coupled mean-field graph, with sampling temperature T as thermal disorder and Glauber-like asynchronous updates. Sweeping 432 configurations of prompt, population size, topology and temperature yields Eraclitus-4.7M, a corpus of 4.7 million tagged responses. Agents gain most consensus within the first few update sweeps; more neighbours per agent speeds convergence on average. Whether a configuration settles on a correct or a hallucinated consensus is not predictable from its initial state; the hallucination-minimising temperature depends on the coupling geometry, so near-greedy decoding is not automatically safest. Semantic agreement correlates with factual convergence and interaction strengthens the association, but never enough for unanimity to certify correctness.

## Contribution

The largest systematic sweep of LLM consensus over topology dimension and temperature, framed explicitly as a spin model, and with ground-truth factuality. Extends the binary-opinion analyses of [[de-marzo-2024-ai]] to factual questions and to graphs from 1D to mean-field.

## Key results

- Claimed: strongest consensus gain within first few sweeps; more neighbours accelerate convergence.
- Claimed: correct vs hallucinated consensus not predictable from initial state.
- Claimed: optimal (hallucination-minimising) temperature depends on coupling geometry.
- Claimed: agreement correlates with factual convergence but unanimity does not certify correctness.
- Dataset: Eraclitus-4.7M (4.7M responses, 432 configurations).

## Methods and models

O(n) spin analogy; ring to complete-graph ladder; Glauber-like asynchronous dynamics; temperature sweep; single frozen model per population. Model and dataset access details not checked.

## Limitations and open questions

Abstract-level read; whether the spin mapping is quantitative (fitted couplings) or metaphorical is not clear from the abstract.

## Relevance to us

High: a released corpus could be mined for order parameters and finite-size effects without new LLM calls. Related: [[fukushima-2026-message]], [[hirota-2026-collective]], [[tanaka-2026-when]].
