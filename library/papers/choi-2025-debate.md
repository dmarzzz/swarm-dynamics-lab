---
id: choi-2025-debate
type: paper
title: 'Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?'
authors:
- Hyeong Kyu Choi
- Xiaojin Zhu
- Sharon Li
year: 2025
venue: Advances in Neural Information Processing Systems (NeurIPS 2025)
url: https://arxiv.org/abs/2508.17536
doi: null
arxiv: '2508.17536'
cite: 'Choi, H. K., Zhu, X., & Li, S. (2025). Debate or vote: Which yields better decisions in multi-agent large language models? Advances in Neural Information Processing Systems (NeurIPS 2025). arXiv:2508.17536.'
topics:
- llm-agent-swarms
- sync-consensus
- collective-decision
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 91 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

Decomposes multi-agent debate into majority voting and inter-agent debate and tests each across seven NLP benchmarks. Majority voting alone accounts for most of the gains usually attributed to debate. A theoretical model treats debate as a stochastic process and proves it induces a martingale over agents' belief trajectories, so debate alone does not improve expected correctness. Interventions that bias belief updates toward correction do improve debate.

## Contribution

A clean negative result plus theory: interaction without a corrective bias is a martingale (pure drift), so gains come from aggregation. This is exactly the drift-vs-selection distinction in [[tanaka-2026-when]].

## Key results

- Voting accounts for most of MAD's improvement on seven benchmarks (abstract claim).
- Debate dynamics form a martingale over beliefs (proved in the paper; not checked here).

## Methods and models

Ablations separating voting from debate rounds; Bayesian/stochastic model of belief updates. Code: https://github.com/deeplearning-wisc/debate-or-vote

## Limitations and open questions

Homogeneous agents on QA-style benchmarks; the martingale result assumes unbiased updates, whereas [[el-2026-physics]] measures an asymmetric pull toward correct answers in some settings.

## Relevance to us

Provides the null hypothesis for "does communication help a swarm decide?", matching the wisdom-of-crowds vs social-influence debate in collective decision-making.
