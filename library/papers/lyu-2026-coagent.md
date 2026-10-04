---
id: lyu-2026-coagent
type: paper
title: 'CoAgent: Concurrency Control for Multi-Agent Systems'
authors:
- Hongtao Lyu
- Dingyan Zhang
- Mingyu Wu
- Xingda Wei
- Haibo Chen
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2606.15376v1
doi: null
arxiv: '2606.15376'
cite: 'Hongtao Lyu, Dingyan Zhang, Mingyu Wu, Xingda Wei, Haibo Chen (2026). CoAgent:
  Concurrency Control for Multi-Agent Systems. arXiv:2606.15376.'
topics:
- llm-agent-swarms
- agent-budgets
added_by: vishesh/codex-idea-scores
accessed: '2026-10-04'
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

The authors address concurrent agents modifying shared state. Their protocol combines ordered execution semantics, notifications and selective repair, rather than simply increasing team size. This supplies a strong competing explanation and baseline for a proposed team-contraction experiment.

## Contribution

Concurrency-control middleware with explicit tool effects and compensation.

## Key results

Ten contended workloads are evaluated; no result is reproduced here.

## Methods and models

Selected sections inspected; see the scope below.

## Limitations and open questions

Read abstract and selected introduction, protocol and tool sections; not a full proof audit. Serializability relies on stated protocol and relevance-judgment assumptions.

## Relevance to us

Closest-work check for the Optimal Swarm Size design refresh; compare [[kim-2025-towards]].
