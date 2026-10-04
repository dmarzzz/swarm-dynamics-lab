---
id: shehata-2026-bystander
type: paper
title: 'The Bystander Effect in Multi-Agent Reasoning: Quantifying Cognitive Loafing in Collaborative Interactions'
authors:
- Dahlia Shehata
- Ming Li
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.10698
doi: null
arxiv: '2605.10698'
cite: 'Shehata, D., & Li, M. (2026). The Bystander Effect in Multi-Agent Reasoning: Quantifying Cognitive Loafing in Collaborative Interactions. arXiv preprint arXiv:2605.10698 (revised September 2026).'
topics:
- llm-agent-swarms
- collective-decision
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Challenges the assumption that collaboration improves LLM reasoning by showing that simulated social pressure induces an algorithmic "bystander effect" or cognitive loafing. Across 22,500 deterministic trajectories on three contexts (GAIA, SWE-bench, Multi-Challenge) with three frontier models, the authors compare internal reasoning traces with final outputs. They define an Interaction Depth Limit, the plurality threshold at which an agent abandons its own reasoning for social compliance, and a "Sovereignty Gap": models often derive the correct answer internally but output a sycophantic answer to appease the simulated swarm. Social load is non-commutative: the identity ("brand") of the lead anchor auditor disproportionately determines outcomes.

## Contribution

Gives a trace-level measurement of conformity (private vs public answer), complementing population-level conformity results in [[weng-2025-do]], [[cho-2025-herd]] and [[ys-2026-everyone]], and the social-loafing framing of [[bertalanic-2026-ringelmann]].

## Key results

- Claimed: 22,500 trajectories; a measurable plurality threshold (Interaction Depth Limit) where reasoning collapses into compliance.
- Claimed: correct internal derivations overridden by social pressure ("Sovereignty Gap").
- Claimed: order and identity of influential agents matter (non-commutative social load).

## Methods and models

Simulated peer pressure in multi-agent reasoning on GAIA, SWE-bench and Multi-Challenge; semantic audits of reasoning traces vs outputs; three models (not named in the abstract).

## Limitations and open questions

Abstract-level read; "simulated swarm" suggests scripted peers rather than interacting agents; "prove" in the abstract refers to empirical findings.

## Relevance to us

The private/public split is a measurable hidden variable for swarm consensus experiments. Related: [[wu-2026-how]], [[de-marzo-2024-ai]].
