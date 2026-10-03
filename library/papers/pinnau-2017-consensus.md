---
id: pinnau-2017-consensus
type: paper
title: A consensus-based model for global optimization and its mean-field limit
authors:
- René Pinnau
- Claudia Totzeck
- Oliver Tse
- Stephan Martin
year: 2017
venue: Mathematical Models and Methods in Applied Sciences
url: https://arxiv.org/abs/1604.05648
doi: 10.1142/S0218202517400061
arxiv: '1604.05648'
cite: Pinnau, R., Totzeck, C., Tse, O., & Martin, S. (2017). A consensus-based model for global optimization and its mean-field limit. Mathematical Models and Methods in Applied Sciences, 27(01), 183–204. https://doi.org/10.1142/S0218202517400061
topics:
- swarm-intelligence
- sync-consensus
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 146 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Introduces consensus-based optimization (CBO): N agents in R^d follow a first-order SDE that pulls each agent toward a
Gibbs-weighted average v_f of the swarm, v_f = sum_i X_i exp(-alpha f(X_i)) / sum_i exp(-alpha f(X_i)), with
multiplicative Brownian noise whose amplitude scales with the agent's distance to v_f. Replacing PSO's arg-min global
best by this smooth weighted average is what lets the authors pass formally to a mean-field (McKean-Vlasov) limit and
analyse the swarm through a nonlocal, degenerate Fokker-Planck PDE. They prove concentration results for the
deterministic mean-field case and show numerically that the particle system tracks the PDE and finds global minima of
Ackley and Rastrigin in d = 1 and d = 20.

## Contribution

The founding paper of the CBO line: it recasts a swarm-intelligence optimiser as an interacting-particle / opinion
consensus model (DeGroot, Hegselmann-Krause, Cucker-Smale, Vicsek are cited as ancestors) so that kinetic-theory and
PDE tools apply. Everything later in this family ([[carrillo-2018-analytical]], [[grassi-2021-particle]],
[[huang-2023-global]], [[fornasier-2024-consensus]]) builds on this construction.

## Key results

- Model (measured/defined): dX_i = -lambda (X_i - v_f) H_eps(f(X_i) - f(v_f)) dt + sqrt(2) sigma |X_i - v_f| dW_i, with
  H_eps a smoothed Heaviside and weight omega = exp(-alpha f).
- Proved: by the Laplace principle, -(1/alpha) log int exp(-alpha f) d rho -> inf f as alpha -> infinity, so the
  weighted measure concentrates on the global minimiser (Proposition 2.1).
- Proved (sigma = 0, H = 1): the mean-field variance decays exactly as V(t) = V(0) exp(-2 lambda t), so the law
  concentrates to a Dirac at some x_hat (Lemma 2.2); for f = strongly convex + small Lipschitz perturbation,
  f(v_f) ends within eps of f(x*) for large enough alpha (Lemma 2.3).
- Proved: without noise any configuration on a level set of f is stationary (non-uniform consensus); noise removes
  these spurious states (Lemma 2.1). Shown numerically on f(x) = 0.2x^4 - 2x^2 + 0.5x + 10.
- Measured (d = 20, 1000 runs, sigma = 5, dt = 0.01, T = 10, success = v_f within 0.25 of x* in sup-norm):
  Ackley success 100% for N = 50, 100, 200; Rastrigin success 34-63% at alpha = 30, rising with alpha to 99.3-99.7%
  at alpha = 50 (N = 100). Alpha matters more than N.
- Measured (d = 1): the W1 distance of the empirical measure to delta_{x*} decays exponentially; its variance shrinks
  as N grows (N = 100 vs 1000), consistent with mean-field behaviour.
- Claimed, not proved: the number of particles needed to mimic mean-field dynamics should scale like O(N^{d/2}), yet
  good results arrive with far fewer particles.

## Methods and models

Interacting SDE system (2a-2b), Euler-Maruyama particle scheme (numpy Mersenne Twister), mean-field Fokker-Planck
equation d_t rho = Laplacian(kappa[rho] rho) + div(mu[rho] rho) with kappa = sigma^2 |x - v_f|^2, solved by
discontinuous Galerkin in space with Strang splitting (local Lax-Friedrichs flux). Benchmarks: shifted Ackley and
Rastrigin. Parameters in d = 1: N = 50, dt = 0.1, alpha = 40, sigma = 0.7, M = 500 runs, T = 80. No code repository
is given in the paper; the later CBX packages ([[bailo-2024-cbx]]) implement this method.

## Limitations and open questions

Analysis is only for the deterministic case (sigma = 0) with H = 1; the stochastic case is deferred to
[[carrillo-2018-analytical]]. The mean-field limit is derived formally (propagation-of-chaos assumption), not proved.
Benchmarks are centre-symmetric functions with the optimum at or near the initial-data centre, exactly the setting
[[kudela-2022-critical]] warns about, although the authors also test shifted optima (x* = 1, 2) and report a small
degradation. Isotropic noise scales badly with dimension (fixed later by anisotropic noise). No comparison against
PSO, CMA-ES or DE.

## Relevance to us

Highest-value bridge between "swarm intelligence algorithms" and "swarm dynamics" for the hackathon: an optimiser
that is literally a consensus/flocking model with a provable continuum limit. Gives us order parameters (variance,
W1 to the minimiser) and phase-like behaviour in (alpha, sigma). Compare with Vicsek/Cucker-Smale entries such as
[[cucker-2007-emergent]], and with PSO dynamics in [[grassi-2021-particle]] and [[huang-2023-global]].
