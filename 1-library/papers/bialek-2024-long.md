---
id: bialek-2024-long
type: paper
title: "Long Timescales, Individual Differences, and Scale Invariance in Animal Behavior"
authors: [William Bialek, Joshua W. Shaevitz]
year: 2024
venue: "Physical Review Letters"
url: https://arxiv.org/abs/2304.09608
doi: 10.1103/PhysRevLett.132.048401
arxiv: "2304.09608"
cite: "Bialek, W., & Shaevitz, J. W. (2024). Long Timescales, Individual Differences, and Scale Invariance in Animal Behavior. Physical Review Letters, 132(4), 048401. https://doi.org/10.1103/PhysRevLett.132.048401"
topics: [criticality-measurement]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "19 (Crossref, 2026-10-03)"
code: []
---

## Summary

A short methods-plus-result letter on how to measure long-range temporal correlations in behaviour without being fooled by individual differences. With finite recordings, pooling animals makes individual differences look like long memory, and long memory makes noise look like individual differences. Their fix: estimate each animal's state-occupancy probabilities over windows of length T, compute the across-individual variance Phi_n(T) (summed over states), and fit Phi_n(T) = A_n (dt/T)^(n Delta) + B_n, where the plateau B_n is the true individual-difference variance and the power law is the connected correlation. Applied to 59 inbred fruit flies walking for 1 h each (10 ms frames, 2.1 x 10^7 frames, 122 discrete behavioural states from earlier unsupervised mapping), they find clean power-law scaling from about 1 s to 1 h with a single scaling dimension Delta = 0.180 +/- 0.004 (second moment), 0.181 +/- 0.005 (third moment) and 0.179 +/- 0.004 (redefined 2-frame states, about 1200 observed). Individual differences contribute under 1% of variance; naive hour-long averages overstate them about 5x.

## Contribution

A practical estimator that separates genuine scale-invariant temporal correlations from heterogeneity across individuals, plus the test that real scale invariance predicts consistent exponents across several moments and under coarse redefinition of states, not just one power law.

## Key results

- Phi_2(T) decays far slower than 1/T beyond about 7 s; the T > 7 s data fit the scaling form across three decades (Fig. 1, 2).
- Delta agrees across Phi_2, Phi_3 and 2-frame states to the third decimal (Table I).
- Individual differences under 1% of total variance; a naive 1 h estimate inflates them about 5x because long correlations mean 1 h is not enough independent samples.
- Authors' interpretation: a single underlying scale-invariant process; they note this is harder to explain by a simple mixture of independent time scales, but do not identify a mechanism.

## Methods and models

Data from earlier fly-behaviour mapping work (Berman et al. 2014, 2016). Window resampling, variance over 1000 random halves of the individuals for error bars, posterior sampling for fit parameters.

## Limitations and open questions

Single species, single condition, 1 h recordings; the 1 s lower cutoff is set by the state definition. Data about ten years old; authors point to week-long recordings as the next test. Scale invariance here is temporal, within individuals, not across a collective.

## Relevance to us

Directly reusable for measuring LLM agent swarms: if we log discrete agent "states" (action types, tools, topics) over long runs, this estimator tells us whether long-memory structure is real or an artefact of pooling heterogeneous agents (different prompts, seeds, models). The multi-moment consistency check is a cheap guard against claiming criticality from one power law. Context: the field's criticality claims and caveats [[mora-2011-biological]], [[munoz-2018-colloquium]]; spatial analogue in flocks [[cavagna-2010-scale]], [[bialek-2014-social]]; RG coarse-graining of neurons [[meshulam-2019-coarse]]. Bialek presented this work as "Finding evidence for scale invariance in animal behavior" (BPPB seminar, 14 July 2023, https://www.youtube.com/watch?v=cfeRxcnRVIw) and at ICTP-SAIFR 2024; recordings not transcribed.
