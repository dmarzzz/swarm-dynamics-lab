---
id: okeeffe-2025-global
type: paper
title: Global synchronization theorem for coupled swarmalators
authors: [Kevin O'Keeffe]
year: 2025
venue: "Chaos: An Interdisciplinary Journal of Nonlinear Science"
url: https://arxiv.org/abs/2410.18011
doi: 10.1063/5.0245064
arxiv: '2410.18011'
cite: "O'Keeffe, K. (2025). Global synchronization theorem for coupled swarmalators. Chaos: An Interdisciplinary Journal of Nonlinear Science, 35(2), 023150."
topics: [sync-consensus, active-matter]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "11 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Proves that in the identical 1D swarmalator model (agents on a ring with position x_i and phase theta_i, couplings
J' and K'), the fully synchronised state, in which all agents share the same position and the same phase, is
globally attracting for almost every initial condition whenever J', K' > 0 and N > 2. The proof is by
elimination: (1) on this parameter region the model is a "transformed gradient system", which rules out limit
cycles and chaos; (2) every fixed point lies on the async, phase-wave or sync manifold or is a so-called pi_pq
state; (3) explicit Jacobian spectra show every fixed point other than sync is unstable there.

## Contribution

First global (rather than local) stability result for any swarmalator model, and an extension of the recent
global-sync results for Kuramoto oscillators on random graphs to oscillators on temporal graphs whose edges are
set by the agents' own motion. Also points out the gradient-plus-Hamiltonian (Helmholtz) structure of the model,
z' = -grad V + S grad H with V = -(K N^2/2)(r^2 + s^2) and H = (J N^2/2)(r^2 - s^2).

## Key results

- Theorem 1: the sync manifold is globally stable on D_sync = {J', K' > 0} (equivalently J - K < 0, J + K < 0
  in sum/difference couplings), for any finite N > 2; N = 2 is non-generic and excluded.
- Lemma 1: the model becomes a gradient flow after rescaling X = x/J', T = theta/K'; the metric is positive
  definite only when J', K' > 0, which is why the theorem is restricted to that region.
- Lemma 3: sync eigenvalues are 0 (multiplicity 2, from rotational symmetry), -(K + J) and -(K - J)
  (each multiplicity N - 1).
- Lemmas 4-6: pi_pq states (agents split into groups pi apart) are saddles for all J, K != 0; phase-wave fixed points
  are stable only on D_wave = {K > 0, J + K > 0, J - K < 0}; theoretical eigenvalues match numerically computed
  ones (Fig. 5, n = 6, 100 trials).
- Manifold dimensions: async 2N - 4, phase wave N - 1, sync 1, which the author connects informally to
  macrostate entropy.
- Open (stated): global stability of async and phase-wave states, where the gradient structure is lost and the
  phase wave destabilises through an apparently subcritical Hopf bifurcation; closed-form async spectrum.

## Methods and models

Model: dx_i/dt = (J'/N) sum_j sin(x_j - x_i) cos(theta_j - theta_i), dtheta_i/dt = (K'/N) sum_j sin(theta_j - theta_i) cos(x_j - x_i)
(identical units, natural frequencies set to zero by a frame change). Coordinates xi = x + theta, eta = x - theta give two
coupled Kuramoto models with "rainbow" order parameters r = |<exp(i xi)>|, s = |<exp(i eta)>|. Tools: transformed
gradient systems, Routh-Hurwitz criteria, block-matrix determinant identities, Mathematica notebooks (linked in
the paper, not opened).

## Limitations and open questions

- Identical agents, all-to-all coupling, 1D periodic domain: far from robots in the plane.
- The author's own discussion lists delays, local coupling and stochastic coupling (features Bettstetter's group
  found essential in hardware, [[barcis-2020-sandsbots]]) and 2D/3D motion as needed before the result is useful
  in the lab.
- Does not cover heterogeneous frequencies, where [[yoon-2022-sync]] gives existence results only.

## Relevance to us

If a hackathon demo needs a guarantee that a swarm will converge to "everyone together and in phase" from any
start, this is the only rigorous statement available for swarmalators, and it tells us which parameter sign
choices to avoid. It also shows how consensus-style Lyapunov and gradient arguments (as in
[[olfati-saber-2004-consensus]] and [[dorfler-2014-synchronization]]) carry over to mobile oscillators. Read
with [[okeeffe-2022-collective]] for the local-stability picture.
