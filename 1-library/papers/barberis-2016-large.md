---
id: barberis-2016-large
type: paper
title: 'Large-Scale Patterns in a Minimal Cognitive Flocking Model: Incidental Leaders, Nematic Patterns, and Aggregates'
authors: [Lucas Barberis, Fernando Peruani]
year: 2016
venue: Physical Review Letters
url: https://arxiv.org/pdf/1912.07929
doi: 10.1103/PhysRevLett.117.248001
arxiv: '1912.07929'
cite: 'Barberis, L., & Peruani, F. (2016). Large-scale patterns in a minimal cognitive flocking model: Incidental leaders, nematic patterns, and aggregates. Physical Review Letters, 117(24), 248001.'
topics: [collective-motion, active-matter]
added_by: dmarz/collective-motion-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "183 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A minimal "cognitive" flocking model in which memoryless self-propelled particles steer only toward the
positions of neighbours inside a vision cone of half-angle beta and range R0, with no velocity alignment.
Because the vision cone breaks action-reaction symmetry (non-reciprocal interactions for beta < pi), the
model produces aggregates and milling-like patterns, moving polar "worms" in which the front particle
acts as an incidental leader, and nematic bands with long-range nematic order, depending on beta and noise.
Simulations plus nonlinear field equations argue this position-based class differs fundamentally from
velocity-alignment flocking. Read: abstract, full main text and figure captions of the arXiv posting
(arXiv title spells "Large-scales patterns"; content matches the PRL abstract); supplement not read.

## Contribution

An early and much-cited demonstration that flocking-like order can arise from perception-limited
attraction alone, without explicit alignment, through non-reciprocity. It sits between
[[vicsek-1995-novel]] (explicit alignment) and later vision-based and nonreciprocal work
([[bastien-2020-model]], [[fruchart-2021-non]], [[bandini-2025-xy]]), and anticipates the empirical
challenge to explicit alignment in [[sayin-2025-behavioral]].

## Key results

- Phase diagram in (beta, D_theta) at N = 10^4, L = 100, rho0 = 1: gas, worms (small beta, e.g.
  beta = 0.8), aggregates or milling (beta near pi), and nematic bands at higher noise
  (e.g. sqrt(2 D_theta) = 0.84, beta = 1.9).
- Worms coagulate much faster than aggregates; particles in a worm copy the front particle, an
  "incidental leader".
- Nematic order parameter S2 is plotted against beta and, in an inset, against N (error bars from 50
  realizations) to support the claim of long-range nematic order; I did not check the finite-size trend.
- Field equations derived from the model reproduce the instabilities (claimed in main text; derivation in
  supplement, not read).

## Methods and models

dx_i/dt = v0 V(theta_i); dtheta_i/dt = (gamma/n_i) sum_{j in Omega_i} sin(alpha_ij - theta_i)
+ sqrt(2 D_theta) xi_i(t), where Omega_i holds neighbours with |x_j - x_i| <= R0 inside the cone
(angle with heading below beta) and alpha_ij is the bearing to j. Parameters v0 = 1, R0 = 1, gamma = 5,
rho0 = 1, periodic boundaries.

## Limitations and open questions

- 2D point particles, no repulsion; the 3D version is only in the supplement.
- The PRL predates the arXiv posting (2019), so the arXiv text may differ slightly from the published one.
- No direct comparison with animal data.

## Relevance to us

A very cheap agent rule (steer toward visible neighbours in a cone) that yields leaders, lanes and
clusters without any velocity sharing, which suits agents that can only observe positions. Good baseline
for testing whether alignment needs to be communicated at all. Related: [[caprini-2023-flocking]],
[[romanczuk-2009-collective]], [[lavergne-2019-group]].
