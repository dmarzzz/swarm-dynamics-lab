---
id: yang-2026-understanding
type: paper
title: Understanding Agent Scaling in LLM-Based Multi-Agent Systems via Diversity
authors:
- Yingxuan Yang
- Chengrui Qu
- Muning Wen
- Laixi Shi
- Ying Wen
- Weinan Zhang
- Adam Wierman
- Shangding Gu
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2602.03794
doi: null
arxiv: '2602.03794'
cite: Yang, Y., Qu, C., Wen, M., Shi, L., Wen, Y., Zhang, W., Wierman, A., & Gu, S. (2026). Understanding agent scaling in LLM-based multi-agent systems via diversity. arXiv preprint arXiv:2602.03794.
topics:
- llm-agent-swarms
- criticality-measurement
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 30 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

Scaling the number of homogeneous agents shows strong diminishing returns, while adding heterogeneity (different models, prompts or tools) keeps helping. An information-theoretic framework bounds MAS performance by intrinsic task uncertainty rather than agent count; gains depend on the number of effective independent channels. The paper introduces K*, a label-free estimate of effective channel count. Empirically, 2 diverse agents can match or exceed 16 homogeneous agents.

## Contribution

An information-theoretic explanation of saturation in agent scaling: correlated agents add redundant, not new, information. Connects to diversity-prediction results in collective intelligence.

## Key results

- Homogeneous scaling saturates early; heterogeneous configurations consistently outperform it (abstract claim).
- 2 diverse agents >= 16 homogeneous agents (abstract claim).

## Methods and models

Architecture-agnostic bounds via mutual information between agent outputs and the answer; K* effective channel count. Code: https://github.com/SafeRL-Lab/Agent-Scaling

## Limitations and open questions

Bounds are on information, not on coordination costs; tasks are mostly reasoning benchmarks.

## Relevance to us

Gives a measurable quantity (effective channels) that parallels redundancy/synergy decompositions in [[riedl-2025-emergent]]; complements [[kim-2025-towards]] and [[li-2024-more]].
