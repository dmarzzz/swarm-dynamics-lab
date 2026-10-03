---
id: borghi-2026-long
type: paper
title: Long-time Stability and Convergence of Particle Swarm Optimization
authors:
- Giacomo Borghi
- Hui Huang
- Dohyeon Kim
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.24696
doi: null
arxiv: '2607.24696'
cite: Borghi, G., Huang, H., & Kim, D. (2026). Long-time stability and convergence of particle swarm optimization. arXiv preprint arXiv:2607.24696. https://doi.org/10.48550/arXiv.2607.24696
topics:
- swarm-intelligence
- sync-consensus
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Connects classical stagnation-based PSO stability analysis with mean-field methods to obtain quantitative estimates
for the time-discrete algorithm. Studies a regularised, memoryless PSO with a noise floor (non-degenerate noise),
proves Schur stability conditions for the linearised dynamics, convergence of the nonlinear mean-field system to a
neighbourhood of a global minimiser via a Laplace principle, and an N^{-1/2} error bound for the mean-field
approximation.

## Contribution

Bridges the two theory traditions in this library: discrete-time stability ([[clerc-2002-particle]],
[[trelea-2003-particle]]) and continuous mean-field convergence ([[huang-2023-global]]); applies to the discrete-time
algorithm people actually run.

## Key results

- Claimed (abstract): explicit stability conditions; convergence near a global minimiser; mean-field error O(N^{-1/2})
  for the discrete algorithm (constants not read).

## Methods and models

Schur stability of linearised recurrences, mean-field analysis, Laplace principle (abstract only).

## Limitations and open questions

Abstract-level reading; very recent preprint. Requires an added noise floor and no memory, so not the canonical PSO.

## Relevance to us

Most recent theory for discrete PSO; useful if experiments check stability boundaries numerically.
