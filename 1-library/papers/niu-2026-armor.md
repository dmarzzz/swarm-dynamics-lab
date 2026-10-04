---
id: niu-2026-armor
type: paper
title: 'ARMOR-MAD: Adaptive Routing for Heterogeneous Multi-Agent Debate in Large Language Model Reasoning'
authors: ['Fuqiang Niu', 'Bowen Zhang']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2606.13197
doi: null
arxiv: '2606.13197'
cite: 'Niu, F., & Zhang, B. (2026). ARMOR-MAD: Adaptive Routing for Heterogeneous Multi-Agent Debate in Large Language Model Reasoning. arXiv:2606.13197.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 1
citations: null
code: []
---

## Summary

A training-free heterogeneous debate framework that treats debate as conditional computation: pre-debate agreement routing skips debate when independent round-0 answers agree, an early-stopping evaluator halts after convergence, and semantic outlier detection down-weights abnormal final answers. With the same model pool it beats fixed-round heterogeneous debate on MATH Level 5, GSM8K, MMLU and MMLU-Pro (65.5%, 96.5%, 90.0%, 81.5%). The authors motivate it by debate amplifying correlated errors among similar agents.

## Contribution

Agreement-gated heterogeneous debate.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Method background for the diversity lever; not a population measurement.
