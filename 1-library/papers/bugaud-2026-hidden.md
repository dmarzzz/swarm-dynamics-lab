---
id: bugaud-2026-hidden
type: paper
title: 'Hidden Clones: Exposing and Fixing Family Bias in Vision-Language Model Ensembles'
authors: ['Zacharie Bugaud']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2603.17111
doi: null
arxiv: '2603.17111'
cite: 'Bugaud, Z. (2026). Hidden Clones: Exposing and Fixing Family Bias in Vision-Language Model Ensembles. arXiv:2603.17111.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Across 17 vision-language models from 8 families on VQAv2, TextVQA and GQA, family-correlated errors reduce effective ensemble dimensionality to 2.5 to 3.6 independent voters and create a misleading tier (1.5 to 6.5% of questions) where correlated majorities drive accuracy to 0% even when the best model is right. Hierarchical family voting recovers 18 to 26 points on that tier.

## Contribution

Family-level error correlation in multimodal ensembles, and family-aware voting.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search round run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Effective-N ceiling outside text LLMs; supports aggregating within family before across families.
