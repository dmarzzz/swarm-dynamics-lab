---
id: liu-2026-phase
type: paper
title: Phase Transition for Budgeted Multi-Agent Synergy
authors: [Bang Liu, Linglong Kong, Jian Pei]
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2601.17311
doi: null
arxiv: '2601.17311'
cite: Liu, B., Kong, L., & Pei, J. (2026). Phase Transition for Budgeted Multi-Agent Synergy. arXiv:2601.17311.
topics: [llm-agent-swarms, criticality-measurement]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

A calibratable theory of when multi-agent systems help, saturate or collapse under a fixed inference budget. Leaf agents are summarised by a compute-performance exponent beta, communication by a message-length fidelity curve gamma(m), dependence by an effective shared-error correlation rho, and the context window W imposes fan-in limits that force hierarchy. For binary tasks with majority aggregation on deep b-ary trees with correlated inputs and lossy communication, the authors prove a sharp phase transition: one scalar alpha_rho (combining gamma(m), rho and b) decides whether a weak signal is amplified to a nontrivial fixed point or washed out to chance. In the amplifying regime, budgeted synergy (beating the best single agent at equal budget) occurs exactly when an organisation exponent s exceeds beta.

## Contribution

A theory that joins correlated errors, lossy communication and context limits into one phase boundary for multi-agent gain, a theoretical counterpart to the empirical ceiling results.

## Key results

- Sharp amplify-or-wash-out transition set by alpha_rho (proved).
- Validation in controlled synthetic simulations; explanatory mapping to published matched-budget LLM agent-scaling studies (reported).

## Methods and models

Analytical model of hierarchical majority aggregation with correlation and lossy channels. Abstract-level read.

## Limitations and open questions

Abstract only; no new LLM experiments as far as the abstract says.

## Relevance to us

Gives a phase-diagram framing for the logistic-versus-ceiling open problem: [[qian-2025-scaling]] style gains and [[bertalanic-2026-ringelmann]] style ceilings can be different sides of alpha_rho.
