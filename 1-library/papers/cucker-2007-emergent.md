---
id: cucker-2007-emergent
type: paper
title: Emergent Behavior in Flocks
authors: [Felipe Cucker, Steve Smale]
year: 2007
venue: IEEE Transactions on Automatic Control
url: https://people.mpi-inf.mpg.de/~mehlhorn/SeminarEvolvability/CuckerSmale.pdf
doi: 10.1109/tac.2007.895842
arxiv: null
cite: "Cucker, F., & Smale, S. (2007). Emergent behavior in flocks. IEEE Transactions on Automatic Control, 52(5), 852-862."
topics: [sync-consensus, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "1851 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Proposes the Cucker-Smale (CS) flocking model: each bird adjusts its velocity by a weighted average of
velocity differences, dv_i/dt = sum_j a_ij (v_j - v_i), with weights a_ij = H / (sigma^2 + |x_i - x_j|^2)^beta that
decay polynomially with distance. Because the interaction graph is complete (weighted), connectivity never has
to be assumed along the trajectory. The main theorem: for beta < 1/2 the flock converges to a common velocity and
bounded relative positions from any initial condition (unconditional flocking); for beta >= 1/2 convergence holds
when the initial velocity spread is small relative to the initial position spread. Continuous and discrete time
are both treated, plus a two-bird example showing the 1/2 threshold is essentially sharp and an application to
language evolution.

## Contribution

Replaces the "assume the graph stays connected" hypothesis of [[jadbabaie-2003-coordination]] and the
Vicsek-model literature with conditions on the initial state only, which the authors call the main virtue of
the work. It turned flocking into a problem in kinetic theory and analysis; hundreds of follow-ups study
CS with noise, delays, leaders, collision avoidance and mean-field/kinetic limits. [[motsch-2011-new]] is the
best-known modification (relative rather than absolute weights).

## Key results

- Theorem 2 (continuous time): with Fiedler number of the adjacency Laplacian bounded below by a decaying function
  of the position spread, three cases give convergence: (i) beta < 1/2, any initial data; (ii) beta = 1/2 with a
  bound on the initial velocity spread; (iii) beta > 1/2 under an explicit inequality linking the initial velocity
  spread Lambda(v0) and position spread Gamma(x0). Velocities converge exponentially to a common limit; positions
  converge to a fixed relative configuration.
- Theorem 3: discrete-time analogue; needs an extra step-size condition (Example 1 shows convergence can fail
  without it).
- Section IV: two birds on a line; for beta > 1/2 the authors exhibit initial conditions with no convergence,
  indicating the 1/2 bound for unconditional flocking is sharp (Remark 3, Remark 4).
- Section VI: the same Laplacian framework gives convergence of a coupled position-language model (formation
  of a "tribe" with a common language).

## Methods and models

Analytical. Model (4)/(5): positions x_i in R^3, velocities v_i, Laplacian L_x of the distance-dependent adjacency
matrix A_x; dv/dt = -L_x v. Tools: Fiedler number bounds (Proposition 4), energy-like functionals
Gamma(x) and Lambda(v) on the orthogonal complement of the diagonal, a lemma on the positive zero of a polynomial.
Model is dynamic (second order, inertia), unlike the kinematic Vicsek model; no speed constraint. Read from the
IEEE version hosted at MPI Informatik (text extraction lost most equations; the model and exponents were taken
from the surrounding text and the abstract).

## Limitations and open questions

- All-to-all coupling: every bird influences every other, however far; the authors call this an idealisation.
- Weights are symmetric and normalised by nothing, so adding agents strengthens coupling; this
  "N-dependence" is the criticism [[motsch-2011-new]] answers.
- No noise, no collision avoidance, no cohesion forces; positions only stay bounded, they do not form lattices
  (contrast [[olfati-saber-2006-flocking]]).
- The author's remark that the method extends to non-symmetric, non-complete graphs is promised, not shown here.

## Relevance to us

The simplest velocity-consensus flocking law with a clean, citable phase boundary (beta = 1/2). Useful as a
baseline controller for drone or robot flocking demos (velocity alignment of this kind appears in field
drone flocking such as [[vasarhelyi-2018-optimized]]; not checked which alignment law they use) and as a test case for learned controllers. Bridges
consensus ([[olfati-saber-2007-consensus]]) and flocking models in the collective-motion topic. Its exponent
threshold is a crisp prediction a hackathon simulation can reproduce in an afternoon.

## Notes from dmarz/sync-consensus-audit

Audit 2026-10-03: metadata, cite string and the key numbers in this entry re-checked against the full text
(arXiv PDF or the hosted PDF at the entry's url); no corrections needed and read_depth full is supported by the
detail in the entry.
