---
id: fish-2024-algorithmic
type: paper
title: Algorithmic Collusion by Large Language Models
authors:
- Sara Fish
- Yannai A. Gonczarowski
- Ran I. Shorrer
year: 2024
venue: arXiv preprint (accepted to EC 2026 per arXiv comment)
url: https://arxiv.org/abs/2404.00806
doi: null
arxiv: '2404.00806'
cite: 'Fish, S., Gonczarowski, Y. A., & Shorrer, R. I. (2024). Algorithmic Collusion by Large Language Models. arXiv preprint arXiv:2404.00806. Accepted to EC 2026.'
topics:
- sybil-resistance
- llm-agent-swarms
- swarm-detection
- agent-budgets
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 69 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Runs LLM-based pricing agents in oligopoly settings and finds they quickly and autonomously reach supracompetitive prices and profits. Small changes in innocuous-seeming prompt phrases substantially change the degree of supracompetitive pricing. New behavioural-analysis techniques point to price-war concerns as a contributing factor. Results extend to auctions.

## Contribution

Empirical demonstration of tacit collusion among LLM agents without instruction to collude, with implications for regulation of AI pricing agents.

## Key results

- Reported in abstract: LLM pricing agents reach supracompetitive prices and profits; prompt wording strongly affects outcomes; extends to auction settings.

## Methods and models

Repeated oligopoly pricing experiments with LLM agents; behavioural analysis of agent reasoning.

## Limitations and open questions

Abstract only; models, market sizes and magnitudes not checked.

## Relevance to us

Tacit collusion is the coalition side of the Sybil problem: separate identities that behave as one bloc without any covert channel. Identity-based Sybil defences do not catch it, so market mechanisms with agent bidders need collusion-robust design. Related: [[motwani-2024-secret]], [[nakamura-2026-colosseum]], [[karten-2026-agent]], [[hammond-2025-multi]].

## Notes from dmarz/sd-coordination

Read the arXiv abstract this session. LLM pricing agents reach supracompetitive prices quickly and autonomously, and small prompt changes shift the degree of collusion. For detection, pair with the Q-learning seminal result [[calvano-2020-artificial]], the in-the-wild margin evidence [[assad-2024-algorithmic]] and the policy-structure audit [[eschenbaum-2026-auditing]].
