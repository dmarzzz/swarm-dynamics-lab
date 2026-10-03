---
id: weng-2025-do
type: paper
title: 'Do as We Do, Not as You Think: the Conformity of Large Language Models'
authors:
- Zhiyuan Weng
- Guikun Chen
- Wenguan Wang
year: 2025
venue: International Conference on Learning Representations (ICLR 2025)
url: https://arxiv.org/abs/2501.13381
doi: null
arxiv: '2501.13381'
cite: 'Weng, Z., Chen, G., & Wang, W. (2025). Do as we do, not as you think: The conformity of large language models. International Conference on Learning Representations (ICLR 2025). arXiv:2501.13381.'
topics:
- llm-agent-swarms
- collective-decision
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "0 (OpenAlex W4406785434, arXiv record, 2026-10-03); Semantic Scholar 50 same day"
code: []
---

## Summary

Studies conformity (groupthink) in LLM multi-agent systems: whether it exists, what drives it and how to mitigate it. Introduces BenchForm, a conformity benchmark with reasoning-intensive tasks and five interaction protocols, and measures conformity and independence rates across LLMs. Factors include interaction time and majority size; mitigation via enhanced personas and a reflection mechanism.

## Contribution

A benchmark-level quantification of Asch-style conformity in LLMs, the micro-level mechanism behind majority-following collective dynamics.

## Key results

- Conformity is present and grows with majority size and interaction duration (abstract).
- Personas and reflection reduce conformity (abstract).

## Methods and models

BenchForm protocols placing a subject agent among simulated peers giving (often wrong) answers. Code: https://github.com/Zhiyuan-Weng/BenchForm

## Limitations and open questions

Subject-vs-confederates design, not free population dynamics. Abstract-level read.

## Relevance to us

Micro-level counterpart of the majority force beta in [[de-marzo-2024-ai]]; see also [[cho-2025-herd]].
