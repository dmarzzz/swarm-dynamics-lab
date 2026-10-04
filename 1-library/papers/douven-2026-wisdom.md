---
id: douven-2026-wisdom
type: paper
title: 'Wisdom of LLM Crowds: Aggregation and Contamination in Language Model Ensembles'
authors: ['Igor Douven']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2607.18269
doi: null
arxiv: '2607.18269'
cite: 'Douven, I. (2026). Wisdom of LLM Crowds: Aggregation and Contamination in Language Model Ensembles. arXiv:2607.18269.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Fifteen LLMs give probability estimates on 254 binary prediction-market questions. Learned linear aggregators (logistic regression matching an MLP) beat every individual model and every classical aggregator; symbolic regression recovers a pure model-disagreement signal as the simplest useful formula. Training-cutoff contamination is pervasive: the frontier-versus-local gap shrinks from 35.8% to 8.9% on questions resolving after all cutoffs, and LLM crowds stay well below the market even when evaluated at their cutoffs.

## Contribution

Wisdom-of-crowds effect for heterogeneous LLMs with contamination controls.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Heterogeneous LLM crowds can beat their best member with learned weights; contamination is a confound any forecasting-style board must control. Compare [[begin-2026-preference]] (same-model markets fail).
