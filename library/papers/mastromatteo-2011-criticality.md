---
id: mastromatteo-2011-criticality
type: paper
title: 'On the criticality of inferred models'
authors: ['Iacopo Mastromatteo', 'Matteo Marsili']
year: 2011
venue: 'Journal of Statistical Mechanics: Theory and Experiment'
url: https://arxiv.org/abs/1102.1624
doi: 10.1088/1742-5468/2011/10/P10012
arxiv: '1102.1624'
cite: 'Mastromatteo, I., & Marsili, M. (2011). On the criticality of inferred models. Journal of Statistical Mechanics: Theory and Experiment, 2011(10), P10012.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '76 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Argues that statistical inference itself pushes fitted models toward critical points. The Fisher information
metric on the space of models equals the model susceptibility, so distinguishable models are densest near
critical points where susceptibility diverges, and parameter estimates are most stable there. Illustrated on
interacting point processes fitted to financial data, where sensible observation time scales yield
near-critical models.

## Contribution

An early and influential theoretical reason to distrust "the fitted maximum entropy model is near critical"
as evidence that the system itself is critical. It is the information-geometry counterpart to the latent-variable
critiques of [[schwab-2014-zipfs]] and [[morrell-2021-latent]].

## Key results

- Fisher information of the model family equals its susceptibility (analytic, claimed in abstract).
- Inference procedures preferentially return models close to phase transitions (argument plus example).
- Financial point-process example: reasonable time scales give near-critical inferred models (applied example).

## Methods and models

Exponential-family (Ising-type) models; Fisher information as the reparametrisation-invariant metric;
inference of interacting (Hawkes-type) point processes on financial transaction data.

## Limitations and open questions

Read at abstract level only. The argument is about which models inference returns, not a proof that any
particular biological claim is wrong; how much it explains the flock results of [[bialek-2012-statistical]] is not
quantified.

## Relevance to us

A required citation in any survey that uses fitted-model criticality as evidence. It also motivates Fisher
information as a measurement tool, used in [[chen-2025-why]] and [[du-2026-fisher]].
