---
id: kota-2026-design
type: paper
title: 'Design and Evaluation of Multi-Agent AI Oracle Systems for Prediction Market Resolution'
authors: ['Tarun Kota']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2605.30802
doi: null
arxiv: '2605.30802'
cite: 'Kota, T. (2026). Design and Evaluation of Multi-Agent AI Oracle Systems for Prediction Market Resolution. arXiv:2605.30802.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Compares single-LLM oracles (GPT-5 Nano, DeepSeek V3, Llama-3.3-70B), independent aggregation and deliberative consensus on 1,189 resolved KalshiBench questions with a shared date-filtered Exa evidence layer. Confidence-weighted independent voting is best at 83.43%, 1.01 points above the best model; deliberation drops accuracy to about 76%, below every single model, as confidently wrong models flip correct ones. Cross-model error correlations of 0.529 to 0.689 explain the shortfall from the Condorcet ceiling. Auto-resolving only unanimous high-confidence questions gives 97.87% accuracy on 47% of the data.

## Contribution

A clean contrast of independent voting versus deliberation across three model families with measured error correlations.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Cross-family deliberation can be worse than independent voting: interaction re-correlates errors. Supports separating aggregation from interaction on a board ([[choi-2025-debate]], [[ren-2026-sepal]]).
