---
id: guerraoui-2024-byzantine
type: paper
title: 'Byzantine Machine Learning: A Primer'
authors:
- Rachid Guerraoui
- Nirupam Gupta
- Rafael Pinot
year: 2024
venue: ACM Computing Surveys
url: https://api.crossref.org/works/10.1145/3616537
doi: 10.1145/3616537
arxiv: null
cite: 'Guerraoui, R., Gupta, N., & Pinot, R. (2024). Byzantine Machine Learning: A Primer. ACM Computing Surveys, 56(7), 1-39.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 36 (Crossref, 2026-10-03)
code: []
---

## Summary

Review article on Byzantine machine learning: training an accurate model in a distributed system where some nodes hold corrupt data or misbehave arbitrarily. The authors note that many solutions build on stochastic gradient descent but the field lacks a unifying structure, and they organise it around three pillars: breakdown point (the largest fraction of Byzantine nodes a method tolerates), robustness, and gradient complexity. They use this frame to compare the merits and limits of existing solutions and to suggest directions.

## Contribution

The standard review of the area, giving a vocabulary (breakdown point, robustness, gradient complexity) for comparing aggregation rules.

## Key results

- Framing (per abstract): breakdown point, robustness and gradient complexity as the three criteria for any Byzantine ML method.
- The specific breakdown points of rules discussed were not checked (body not opened; the ACM page returned 403 and the abstract was read from the Crossref record).

## Methods and models

Survey. Only the abstract was read.

## Limitations and open questions

Abstract-level reading. Covers gradient-based learning, not merging of discrete agent memories.

## Relevance to us

Q2. The review to read first for thresholds. "Breakdown point" is the precise name for dmarz's question: the fraction of returning sub-agents an attacker must corrupt before the merged parent can be moved arbitrarily far. In classical robust statistics the ceiling for location estimators such as the median is one half (the contamination model is in [[huber-1964-robust]]; the breakdown-point concept itself comes from later work by Hampel, not catalogued here); distributed protocols set lower ceilings (one third for oral-message agreement, [[lamport-1982-byzantine]]). Primary works: [[blanchard-2017-byzantine]], [[yin-2018-byzantine]], [[el-mhamdi-2018-hidden]], [[karimireddy-2020-learning]], [[alistarh-2018-byzantine]].
