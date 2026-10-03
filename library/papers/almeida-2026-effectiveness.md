---
id: almeida-2026-effectiveness
type: paper
title: Effectiveness of LLM-based Software Diversity for Reliability Improvement -- an Empirical Study
authors:
- Gabriel Almeida
- Ilir Gashi
- Vladimir Stankovic
- Joao R. Campos
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.03174
doi: null
arxiv: '2607.03174'
cite: 'Almeida, G., Gashi, I., Stankovic, V., & Campos, J. R. (2026). Effectiveness of LLM-based Software Diversity for Reliability Improvement -- an Empirical Study. arXiv preprint arXiv:2607.03174.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Extends classical software-diversity studies to LLM-generated programs. Using historical human-written programs and large pools of LLM-generated ones under a common compile, sandbox and exhaustive test setup, the authors vary model family, sampling temperature and programming language, and measure reliability gain in a 1-out-of-2 configuration for homogeneous and heterogeneous pairs (within one LLM, across languages, across LLM and human code). Combining LLM-generated programs gives reliability gains, especially in heterogeneous pairs, but the gain depends on language and generation setting.

## Contribution

Positions LLMs as a cheap source of design diversity and measures how much of the classical diversity benefit they deliver.

## Key results

- Reported in abstract: heterogeneous LLM-generated pairs give reliability gains; within-LLM pairs give less; the effect depends on language and generation settings. No numbers in the abstract.

## Methods and models

1-out-of-2 reliability analysis over program pools; exhaustive test suites. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; no adversary.

## Relevance to us

Q2. Supports the design rule that emerges from [[knight-1986-experimental]], [[ron-2026-n-version]] and [[nogueira-2026-systematic]]: if sub-agents are to count as independent parts in a k-of-n merge, they should differ in model family and in how they work, not only in random seed or temperature. Same-model forks give the smallest gains.
