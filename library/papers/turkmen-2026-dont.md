---
id: turkmen-2026-dont
type: paper
title: 'Don''t Always Pick the Highest-Performing Model: An Information Theoretic View of LLM Ensemble Selection'
authors: ['Yigit Turkmen', 'Baturalp Buyukates', 'Melih Bastopcu']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2602.08003
doi: null
arxiv: '2602.08003'
cite: 'Turkmen, Y., Buyukates, B., & Bastopcu, M. (2026). Don''t Always Pick the Highest-Performing Model: An Information Theoretic View of LLM Ensemble Selection. arXiv:2602.08003.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Formulates budgeted LLM ensemble selection as maximising mutual information between the label and member predictions, models correlated errors with a Gaussian copula, and derives an information-theoretic error floor that explains why ensemble accuracy saturates as members are added. A greedy mutual-information selector is tested on two QA datasets and one binary sentiment task.

## Contribution

A copula-based error floor for ensembles of correlated LLMs.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search round run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Theoretical companion to the floor in [[li-2026-state]] and the ceiling in [[chen-2026-when]].
