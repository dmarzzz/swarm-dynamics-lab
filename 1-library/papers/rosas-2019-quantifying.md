---
id: rosas-2019-quantifying
type: paper
title: 'Quantifying high-order interdependencies via multivariate extensions of the mutual information'
authors: ['Fernando E. Rosas', 'Pedro A. M. Mediano', 'Michael Gastpar', 'Henrik J. Jensen']
year: 2019
venue: 'Physical Review E'
url: https://arxiv.org/abs/1902.11239
doi: 10.1103/PhysRevE.100.032305
arxiv: '1902.11239'
cite: 'Rosas, F. E., Mediano, P. A. M., Gastpar, M., & Jensen, H. J. (2019). Quantifying high-order interdependencies via multivariate extensions of the mutual information. Physical Review E, 100(3), 032305.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '239 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Introduces the O-information, a model-agnostic scalar built from multivariate extensions of mutual information
(total correlation and dual total correlation), that says whether a set of variables is dominated by redundancy
(positive) or synergy (negative). The paper derives its analytical properties, relates it to other high-order
measures from statistical mechanics and neuroscience, and demonstrates it on Baroque music scores.

## Contribution

The standard cheap measure of higher-order (beyond pairwise) statistical structure. Unlike full partial
information decomposition it scales gracefully with system size (a point the paper stresses), which makes it
usable on flocks of realistic size; related emergence work by the same authors includes [[rosas-2020-reconciling]]
and [[sas-2026-improved]], and see [[varley-2022-emergence]].

## Key results

- O-information Omega = TC - DTC = (n-2)H(X) + sum_j [H(X_j) - H(X_-j)] (Eq. 5); Omega > 0 means redundancy-dominated, Omega < 0 synergy-dominated (definition and properties).
- Relations to existing high-order measures (analytic, claimed in abstract).
- Proof of concept: synergy in Baroque music scores (application).

## Methods and models

Entropy-based functionals: total correlation, dual total correlation, O-information and S-information; Gaussian
and discrete estimators.

## Limitations and open questions

Abstract-level read. Omega is a net balance, so equal redundancy and synergy can cancel; estimation in
continuous high-dimensional data needs Gaussian or k-NN assumptions.

## Relevance to us

A ready measure of whether swarm velocity or heading fluctuations carry synergistic group-level information.
Pairs with [[rosas-2020-reconciling]], [[mediano-2022-greater]] and the JIDT toolkit [[lizier-2014-jidt]].
