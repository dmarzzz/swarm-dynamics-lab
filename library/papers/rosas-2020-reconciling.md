---
id: rosas-2020-reconciling
type: paper
title: 'Reconciling emergences: An information-theoretic approach to identify causal emergence in multivariate data'
authors: ['Fernando E. Rosas', 'Pedro A. M. Mediano', 'Henrik J. Jensen', 'Anil K. Seth', 'Adam B. Barrett', 'Robin L. Carhart-Harris', 'Daniel Bor']
year: 2020
venue: 'PLOS Computational Biology'
url: https://arxiv.org/abs/2004.08220
doi: 10.1371/journal.pcbi.1008289
arxiv: '2004.08220'
cite: 'Rosas, F. E., Mediano, P. A. M., Jensen, H. J., Seth, A. K., Barrett, A. B., Carhart-Harris, R. L., & Bor, D. (2020). Reconciling emergences: An information-theoretic approach to identify causal emergence in multivariate data. PLOS Computational Biology, 16(12), e1008289.'
topics: [criticality-measurement, collective-motion]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: '158 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Proposes a formal, data-driven theory of causal emergence built on partial information
decomposition (PID) and its dynamical extension, integrated information decomposition (PhiID). A supervenient
macro feature V_t is causally emergent if it carries unique predictive information about the system's future
that no small set of parts carries. Emergence capacity equals the system's dynamical synergy, which splits
into downward causation (whole predicts parts) and causal decoupling (whole predicts whole). Because full PID
is intractable for large systems, they give sufficient criteria based only on pairwise mutual informations,
Psi = I(V_t; V_t') - sum_j I(X_t^j; V_t'), and test them on Conway's Game of Life, Reynolds boids and macaque
ECoG data.

## Contribution

Turns "emergence" into a measurable quantity on observational time series, with a practical
estimator (Psi) that scales linearly with system size. It is the most usable causal-emergence framework for
collective motion data, complementing the intervention-based effective-information approach of
[[hoel-2013-quantifying]].

## Key results

- Theorem: a system has a causally emergent feature of order k iff Syn^(k)(X_t; X_t') > 0; Syn = G (causal decoupling) + D (downward causation).
- Game of Life particle collider (15x15 grid, 1000 steps): Psi = 0.58 +/- 0.02 for particle type; Gamma = 0.009, orders of magnitude below I(V_t; V_t') = 0.99, suggesting causal decoupling.
- Boids (N = 10): sweeping avoidance strength a2, the centre of mass meets Psi > 0 only at intermediate a2, where flocks form and break up; at low a2 redundancy drives Psi negative, at high a2 the centre of mass has little self-predictability.
- Macaque ECoG (64 channels) decoded wrist position: Psi = 1.275 +/- 0.002 at 8 ms lag, Gamma = 0.049; criterion holds up to about 0.2 s.

## Methods and models

PID atoms I_partial^alpha; k-th order synergy and unique information; PhiID lattice for
downward-causation and decoupling indices; practical criteria Psi, Delta, Gamma (Eq. 10) with Bayesian or
Gaussian mutual information estimators; JIDT ([[lizier-2014-jidt]]) for ECoG. Boids follow Seth's
three-parameter Reynolds model (aggregation a1, avoidance a2, alignment a3).

## Limitations and open questions

Psi is a whole-minus-sum measure: sufficient but not necessary, and double-counts redundancy, so it
misses emergence in redundant (highly ordered) regimes and cannot rule emergence out. Requires a candidate
macro variable. Assumes fully observed Markovian systems. Results depend on the micro partition. Boids
example is tiny (10 agents) and illustrative.

## Relevance to us

Gives us an emergence score computable from swarm trajectories (e.g. centre of mass, polarisation
or milling order parameter as V_t). The boids result suggests emergence peaks at intermediate interaction
regimes, a hypothesis worth testing against order-disorder transitions in larger swarms. Read with
[[mediano-2022-greater]], [[varley-2022-emergence]], [[hoel-2013-quantifying]] and [[niizato-2023-functional]].


## Notes from dmarz/criticality-measurement-audit

Audit 2026-10-03: re-opened arXiv 2004.08220 (PDF) and Crossref (PLOS Comput Biol 16(12) e1008289, 7 authors). Verified Game of Life 15x15 arrays, 1000 update steps, Psi = 0.58 +/- 0.02, Gamma = 0.009, I(V;V') = 0.99; boids N = 10; ECoG 64 channels, Psi = 1.275 +/- 0.002 and Gamma = 0.049 at 8 ms, criterion up to about 0.2 s: all match. No corrections. Companion high-order measure: [[rosas-2019-quantifying]] (O-information).
