---
id: meshulam-2019-coarse
type: paper
title: 'Coarse graining, fixed points, and scaling in a large population of neurons'
authors: ['Leenoy Meshulam', 'Jeffrey L. Gauthier', 'Carlos D. Brody', 'David W. Tank', 'William Bialek']
year: 2019
venue: 'Physical Review Letters'
url: https://arxiv.org/abs/1809.08461
doi: 10.1103/PhysRevLett.123.178103
arxiv: '1809.08461'
cite: 'Meshulam, L., Gauthier, J. L., Brody, C. D., Tank, D. W., & Bialek, W. (2019). Coarse graining, fixed points, and scaling in a large population of neurons. Physical Review Letters, 123(17), 178103.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: '145 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Develops a phenomenological renormalization group (PRG) for systems without a spatial lattice: repeatedly merge
the most correlated pairs of variables, and track how distributions and moments of the coarse-grained variables
change. Applied to calcium imaging of 1485 CA1 neurons in mice running in virtual reality, the coarse-grained
distributions approach a non-Gaussian fixed form, and several static and dynamic quantities scale as power laws
of cluster size, suggesting a non-trivial fixed point.

## Contribution

Replaces "is the fitted model at a critical temperature" with an RG-style test that works directly on data and
needs no model fit. It is now the main template for scaling analysis in neural data and has been suggested for
flocks and swarms (the paper cites them as candidate applications).

## Key results

- Probability of silence in clusters of size K: P0(K) = exp(-a K^beta) with beta = 0.87 +/- 0.03 (independent units would give 1) (measured).
- Covariance eigenvalues within clusters scale with fractional rank, exponent mu = 0.71 +/- 0.15 (measured).
- Dynamic scaling of autocorrelation time with cluster size, z-tilde = 0.11 +/- 0.01 (measured).
- An independent place-cell surrogate built from each cell's place field does not reproduce the scaling (control).

## Methods and models

Two-photon calcium imaging, 0.5 x 0.5 mm field, 30 Hz, 1485 cells, three mice. PRG: compute correlation
matrix, greedily pair maximally correlated variables, sum and renormalise, iterate to K = 2, 4, ... 256. In a
second scheme, project onto top eigenvectors of the covariance within clusters (momentum-space analogue).

## Limitations and open questions

Exponents are measured over about two decades of K in a single brain area; whether the fixed point reflects
criticality or latent drives is not settled ([[morrell-2021-latent]] shows latent variables can produce similar
scaling). Calcium signals are slow and thresholded.

## Relevance to us

A measurement recipe we can run on simulated swarm velocities or agent activity without assuming a model: if
coarse-grained variables approach a fixed non-Gaussian form with power-law scaling, that is stronger evidence than
a heat-capacity peak. Related: [[morales-2023-quasiuniversal]], [[mora-2011-biological]], [[sooter-2025-defining]].
