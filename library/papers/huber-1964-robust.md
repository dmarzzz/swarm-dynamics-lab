---
id: huber-1964-robust
type: paper
title: Robust Estimation of a Location Parameter
authors:
- Peter J. Huber
year: 1964
venue: The Annals of Mathematical Statistics
url: https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-1/Robust-Estimation-of-a-Location-Parameter/10.1214/aoms/1177703732.full
doi: 10.1214/aoms/1177703732
arxiv: null
cite: 'Huber, P. J. (1964). Robust Estimation of a Location Parameter. The Annals of Mathematical Statistics, 35(1), 73-101.'
topics:
- fork-merge-security
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 5654 (Crossref, 2026-10-03)
code: []
---

## Summary

Founding paper of robust statistics. Huber estimates a location parameter when the data come from a contaminated normal distribution, where a fraction of observations may be gross errors from an unknown distribution. He introduces M-estimators, which lie between the sample mean and the sample median, and finds the estimator that minimises the worst-case asymptotic variance over the contamination neighbourhood: its loss behaves quadratically (like the mean) for small residuals and linearly (like the median) for large ones, related to Winsorizing.

## Contribution

Introduces the epsilon-contamination model and minimax M-estimation, the statistical basis for the median, trimmed mean and related rules later used in Byzantine-robust aggregation.

## Key results

- Result (per the publisher page summary): the minimax-robust estimator under epsilon-contamination of the normal has the Huber loss form, quadratic in the centre and linear in the tails.
- Not in this paper: the breakdown point concept, which came later (Hampel); not catalogued here.

## Methods and models

Asymptotic variance of M-estimators under a contamination neighbourhood. Only the abstract and publisher page were read.

## Limitations and open questions

Abstract-level reading. The contamination model assumes outliers are a random fraction, not an adaptive adversary who sees the honest data; Byzantine ML relaxes that assumption ([[blanchard-2017-byzantine]], [[baruch-2019-little]]).

## Relevance to us

Q2, as background. The contamination fraction epsilon is the statistical counterpart of the fraction of corrupted sub-agents, and robust location estimators show that merging by a median-like rule caps the influence of each contribution while a mean does not. The jump from random contamination to adaptive adversaries is where guarantees weaken, see [[yin-2018-byzantine]] and [[guerraoui-2024-byzantine]].
