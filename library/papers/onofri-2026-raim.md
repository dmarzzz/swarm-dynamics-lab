---
id: onofri-2026-raim
type: paper
title: 'RAIM: Robust Aggregation of Inexpensive Models for Hallucination Detection'
authors: ['Elia Onofri', 'Roberto Di Pietro']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2609.39229
doi: null
arxiv: '2609.39229'
cite: 'Onofri, E., & Di Pietro, R. (2026). RAIM: Robust Aggregation of Inexpensive Models for Hallucination Detection. arXiv:2609.39229.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Aggregates ten cheap open-weight judges (4 to 9B, disjoint families) for faithfulness evaluation with a cross-fitted stacked logistic regression robust to correlated errors, plus an admissibility test that says from the members outputs when aggregation beats the best member. Against Claude Sonnet the panel keeps a median 93% of Cohen kappa and loses 2.9 points of balanced accuracy on average across eight benchmarks, at a sixty-fourth of the price, after 50 to 100 labelled calibration records.

## Contribution

Correlation-robust stacking with an explicit test for when aggregation pays.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Shows the ceiling can be partly worked around with calibrated stacking; context for [[kohli-2026-nine]].
