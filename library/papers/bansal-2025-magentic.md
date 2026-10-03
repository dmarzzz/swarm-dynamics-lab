---
id: bansal-2025-magentic
type: paper
title: 'Magentic Marketplace: An Open-Source Environment for Studying Agentic Markets'
authors:
- Gagan Bansal
- Wenyue Hua
- Zezhou Huang
- Adam Fourney
- Amanda Swearngin
- Will Epperson
- Tyler Payne
- Jake M. Hofman
- Brendan Lucier
- Chinmay Singh
- et al.
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2510.25779
doi: null
arxiv: '2510.25779'
cite: 'Bansal, G., Hua, W., Huang, Z., Fourney, A., Swearngin, A., Epperson, W., Payne, T., Hofman, J. M., Lucier, B., Singh, C., et al. (2025). Magentic Marketplace: An Open-Source Environment for Studying Agentic Markets. arXiv preprint arXiv:2510.25779.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 14 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

An open-source simulated two-sided market in which Assistant agents represent consumers and Service agents represent competing businesses, built to study welfare, behavioural biases, vulnerability to manipulation and the effect of search mechanisms. Frontier models approach optimal welfare only under ideal search conditions; performance degrades sharply with scale, and all models show a strong first-proposal bias that gives 10 to 30 times more advantage to response speed than to quality.

## Contribution

A shared, open-source environment for agent-to-agent markets that includes manipulation experiments.

## Key results

- Reported in abstract: near-optimal welfare only with ideal search; sharp degradation with scale; first-proposal bias yields 10 to 30x advantage for speed over quality.

## Methods and models

Simulated marketplace with LLM consumer and business agents; varied search mechanisms and scale.

## Limitations and open questions

Abstract only; whether Sybil sellers are part of the manipulation suite was not checked. 24 authors; list truncated to ten plus et al.

## Relevance to us

First-proposal bias means a principal who floods a market with many fast Service identities captures attention regardless of quality, a Sybil amplification channel. Pair with the explicit Sybil scenario in [[karten-2026-agent]] and the reputation attack in [[xia-2026-when]].
