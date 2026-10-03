---
id: ha-2008-particle
type: paper
title: From particle to kinetic and hydrodynamic descriptions of flocking
authors: [Seung-Yeal Ha, Eitan Tadmor]
year: 2008
venue: Kinetic and Related Models
url: https://arxiv.org/pdf/0806.2182
doi: 10.3934/krm.2008.1.415
arxiv: '0806.2182'
cite: 'Ha, S.-Y., & Tadmor, E. (2008). From particle to kinetic and hydrodynamic descriptions of flocking. Kinetic and Related Models, 1(3), 415–435.'
topics: [collective-motion, sync-consensus]
added_by: dmarz/collective-motion-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "608 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Takes the Cucker-Smale particle model of flocking ([[cucker-2007-emergent]]), in which each agent relaxes
its velocity toward others' with a distance-decaying weight, and proves flocking (bounded diameter and
convergence to a common velocity) via the dynamics of fluctuations about the centre of mass, improving the
original conditions for slowly decaying kernels r(|x-y|) ~ |x-y|^(-2 beta) with 2 beta <= 1. It then
derives the mean-field Vlasov-type kinetic equation, proves global existence and time-asymptotic flocking
for compactly supported initial data, and takes moments to obtain a hydrodynamic (Euler-type) description
for which flocking is proved without closing the moment hierarchy. Read: abstract, introduction, section
structure and main theorem statements of the arXiv version; proofs not checked.

## Contribution

The standard reference for the particle-to-kinetic-to-hydrodynamic hierarchy in the applied-mathematics
literature on flocking, distinct from the physics route of [[toner-1998-flocks]]. It launched a large
literature on kinetic Cucker-Smale models and hydrodynamic limits (e.g. Karper et al., "Hydrodynamic limit of the kinetic Cucker-Smale
flocking model", M3AS, DOI 10.1142/s0218202515500050, seen in Crossref search, not opened).

## Key results

- Particle level (Theorem 2.1): unconditional flocking for kernels decaying like |x - y|^(-2 beta) with
  2 beta <= 1, extending the original Cucker-Smale result (which needed 2 beta < 1) to the borderline case
  beta = 1/2; the proof gives exponential convergence of velocity fluctuations for 2 beta < 1 (rates for
  the borderline case not checked by me).
- Kinetic level: Vlasov-type mean-field equation for f(t,x,v); global classical solutions and
  time-asymptotic flocking for arbitrary compactly supported initial data.
- Hydrodynamic level: flocking behaviour proved for the moment equations without a closure assumption.
- Results are proofs, not simulations; no noise is included.

## Methods and models

Cucker-Smale dynamics dv_i/dt = (lambda/N) sum_j r(x_i, x_j)(v_j - v_i), dx_i/dt = v_i, with
r(|x - y|) = 1/(1 + |x - y|^2)^beta; Lyapunov-type estimates on position and velocity fluctuations; BBGKY-style
mean-field derivation; a priori estimates for the kinetic equation; moment hierarchy for density and
momentum.

## Limitations and open questions

- Deterministic and noise-free: none of the order-disorder transitions or band instabilities of noisy
  Vicsek-type models ([[gregoire-2004-onset]], [[solon-2015-pattern]]) appear.
- All-to-all (metric, decaying) coupling, not topological; no repulsion or cohesion.
- Hydrodynamic flocking is proved for solutions that are assumed to exist and be smooth.

## Relevance to us

The rigorous baseline for consensus-style velocity alignment: if we use Cucker-Smale controllers for
agents, these conditions say when flocking is guaranteed. Connects collective motion to the consensus
literature ([[jadbabaie-2003-coordination]]) and to the kinetic-theory view in [[vicsek-2012-collective]].
