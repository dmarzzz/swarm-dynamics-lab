---
id: cleghorn-2018-particle
type: paper
title: 'Particle swarm stability: a theoretical extension using the non-stagnate distribution assumption'
authors: [Christopher W. Cleghorn, Andries P. Engelbrecht]
year: 2018
venue: Swarm Intelligence
url: https://repository.up.ac.za/bitstreams/a2a0b38c-4afd-4232-b960-285d551d64d9/download
doi: 10.1007/s11721-017-0141-x
arxiv: null
cite: 'Cleghorn, C. W., & Engelbrecht, A. P. (2018). Particle swarm stability: A theoretical extension using the non-stagnate distribution assumption. Swarm Intelligence, 12(1), 1–22. https://doi.org/10.1007/s11721-017-0141-x'
topics: [swarm-intelligence]
added_by: dmarz/swarm-intelligence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: 94 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Almost all PSO stability theory assumes stagnation: personal and neighbourhood bests are frozen. This paper replaces
that with the weaker "non-stagnate distribution" assumption, in which the bests are random variables whose
distributions may change over time as long as their means and variances converge. Under it they derive order-1
(mean) and order-2 (variance) stability criteria for a general class of PSO update rules, show that convergent best
positions are a necessary condition, and recover the known canonical-PSO stability region.

## Contribution

Closes the gap between the stagnation-based regions of [[trelea-2003-particle]], [[poli-2007-particle]]-era work
(Poli 2009, Blackwell 2012) and real PSO runs, in which the bests keep moving. It is the reference result on PSO
parameter regions as of 2018 and sits between the deterministic analyses ([[clerc-2002-particle]],
[[kadirkamanathan-2006-stability]]) and the mean-field line ([[grassi-2021-particle]], [[huang-2023-global]],
[[borghi-2026-long]]).

## Key results

- Proved (Theorem 4.1): for position updates of the form x_{t+1} = alpha x_t + beta x_{t-1} + gamma_t (random alpha,
  beta, gamma), order-1 and order-2 stability follow from spectral-radius conditions on moment matrices when the
  informers' means and variances converge; convergence of the informers is also necessary.
- Derived (canonical PSO, w constant, theta_k = c_k r_k with r_k ~ U(0,1)): order-1 stability iff -1 < w < 1 and
  0 < c1 + c2 < 4(1 + w); order-2 stability iff -1 < w < 1 and 0 < c1 + c2 < 24(1 - w^2)/(7 - 5w). This is exactly
  Poli's 2009 region, now justified without stagnation.
- Derived for a general PSO with random w, theta_1, theta_2: closed-form necessary order-2 conditions (eqs. 43-44);
  sufficiency checked empirically, 100% of 10^12 random parameter combinations satisfying (43)-(44) had spectral
  radius < 1 (measured, not proved).

## Methods and models

Linear stochastic recurrence for one particle per dimension; first- and second-moment dynamics written as linear
systems with time-varying operators; convergence via spectral radius and norm arguments; symbolic eigenvalues in
Matlab. Applies to fully informed PSO ([[mendes-2004-fully]]), unified PSO and other variants. I read the
introduction, Section 3 (prior regions), Section 5 and the conclusions, and skimmed the proofs in Section 4. Read
from the authors' accepted manuscript in the University of Pretoria repository.

## Limitations and open questions

Still an assumption (convergent informer moments), not a theorem about PSO on a given objective; the authors
recommend empirical checks in an assumption-free setting. Single-particle, per-dimension analysis ignores coupling
through the shared neighbourhood best. Says nothing about whether the swarm converges to a good optimum, only that it
does not diverge.

## Relevance to us

Gives the exact parameter region where a PSO swarm neither explodes nor freezes: a phase boundary in (w, c1 + c2)
that a hackathon experiment can measure directly. Compare with the explosion threshold in the (m, sigma) phase
diagrams of [[huang-2023-global]].
