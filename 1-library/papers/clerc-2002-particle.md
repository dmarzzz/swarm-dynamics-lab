---
id: clerc-2002-particle
type: paper
title: The particle swarm - explosion, stability, and convergence in a multidimensional complex space
authors:
- Maurice Clerc
- James Kennedy
year: 2002
venue: IEEE Transactions on Evolutionary Computation
url: https://doi.org/10.1109/4235.985692
doi: 10.1109/4235.985692
arxiv: null
cite: Clerc, M., & Kennedy, J. (2002). The particle swarm - explosion, stability, and convergence in a multidimensional complex space. IEEE Transactions on Evolutionary Computation, 6(1), 58–73. https://doi.org/10.1109/4235.985692
topics:
- swarm-intelligence
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 9051 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Analyses a single particle's trajectory first in discrete time (algebraic view) and then in continuous time
(analytical view), developing a five-dimensional depiction that describes the system completely. The analysis yields
a generalised model with coefficients that control convergence tendencies (the constriction coefficients), and
modified optimisers derived from it remove problems of the original algorithm (velocity explosion) and improve
results on standard test functions.

## Contribution

The first dynamical-systems theory of PSO; introduced constriction, which with [[shi-1998-modified]]'s inertia defines
standard PSO. Prior to the mean-field work ([[grassi-2021-particle]], [[huang-2023-global]]) this was the main
theoretical anchor.

## Key results

- Claimed in abstract: a complete low-dimensional description of particle dynamics and a family of coefficient
  settings that guarantee convergence; empirical improvements on test functions (numbers not read).

## Methods and models

Deterministic single-particle model (random coefficients replaced by constants), eigenvalue analysis of the linear
recurrence, continuous-time analogue; benchmark experiments (abstract only).

## Limitations and open questions

Abstract-level reading. Deterministic, stagnation (fixed attractor) assumptions; stochasticity and swarm interaction
are not captured, which [[kadirkamanathan-2006-stability]] and later order-2 stability analyses address.

## Relevance to us

Defines the explosion/convergence boundary in PSO parameter space, the algorithmic counterpart of a stability phase
diagram. Compare with the empirical (m, sigma) phase diagram in [[huang-2023-global]].
