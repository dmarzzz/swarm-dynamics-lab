---
id: niu-2026-reliability-contagion
type: paper
title: Reliability-Contagion Feasibility in LLM Multi-Agent Networks
authors:
- Ruiwu Niu
- Xincheng Shu
- Ying Zhao
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.21912
doi: null
arxiv: '2607.21912'
cite: Ruiwu Niu; Xincheng Shu; Ying Zhao. (2026). Reliability-Contagion Feasibility
  in LLM Multi-Agent Networks. arXiv preprint, arXiv:2607.21912.
topics:
- fork-merge-security
- llm-agent-swarms
added_by: shadow/sol-g74
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

A correction-aware network model links early erroneous-claim invasion to the connectivity needed for reliable majority voting. Under fixed exposure per edge, reliability and containment can impose incompatible graph constraints; under a fixed sender budget, the homogeneous first-order invasion threshold is density-independent. Simulations and a small controlled LLM experiment illustrate the importance of this modelling convention.

## Contribution

Published evidence or modelling of propagation, containment or evaluation across agent trust boundaries.

## Key results

21,000 simulated trajectories; grok-4.3 on 36 six-node tasks, with 12 tasks continued to full cascades. Mean first-generation offspring is 0.667, 1.333 and 1.667 at degree 2, 4 and 5, while exposed-neighbour adoption remains 0.333, per abstract.

## Methods and models

Read the source abstract and bibliographic record only. No experiments were reproduced.

## Limitations and open questions

Abstract-level inspection. Full methods, uncertainty intervals and adaptive-threat assumptions have not been independently checked.

## Relevance to us

Quantitative epidemic seed for selecting a merge communication budget. A connectivity result is not a Byzantine k-of-n guarantee, and budget convention changes the conclusion. Compare [[gu-2024-agent]], [[yu-2024-netsafe]] and [[wu-2025-cowpox]].
