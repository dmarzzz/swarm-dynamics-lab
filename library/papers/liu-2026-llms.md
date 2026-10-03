---
id: liu-2026-llms
type: paper
title: 'LLMs as a Jury: Cross-Model Consensus Can Outperform Process Reward Models for LLM Reasoning'
authors: ['Ning Liu']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2607.10139
doi: null
arxiv: '2607.10139'
cite: 'Liu, N. (2026). LLMs as a Jury: Cross-Model Consensus Can Outperform Process Reward Models for LLM Reasoning. arXiv:2607.10139.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Uses cross-model consensus (independently trained models each solving once and agreeing on a final answer) as an answer selector. Across seven benchmarks it selects correct answers better than self-consistency and far better than self-scoring; on competition maths it closes the whole gap to an oracle selector. The stated mechanism is error decorrelation: different models scatter their wrong answers while the right one accumulates agreement, formalised as a parameter-free closed-form law.

## Contribution

Positive evidence that heterogeneous panels add evidence where homogeneous resampling does not.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

The flip side of the homogeneity ceiling: cross-model agreement carries signal because errors decorrelate. Compare [[kohli-2026-nine]], where frontier judges stay correlated on NLI.
