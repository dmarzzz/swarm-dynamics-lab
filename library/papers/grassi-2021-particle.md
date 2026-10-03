---
id: grassi-2021-particle
type: paper
title: 'From particle swarm optimization to consensus based optimization: stochastic modeling and mean-field limit'
authors:
- Sara Grassi
- Lorenzo Pareschi
year: 2021
venue: Mathematical Models and Methods in Applied Sciences
url: https://arxiv.org/abs/2012.05613
doi: 10.1142/S0218202521500342
arxiv: '2012.05613'
cite: 'Grassi, S., & Pareschi, L. (2021). From particle swarm optimization to consensus based optimization: Stochastic modeling and mean-field limit. Mathematical Models and Methods in Applied Sciences, 31(08), 1625–1657. https://doi.org/10.1142/S0218202521500342'
topics:
- swarm-intelligence
- sync-consensus
- active-matter
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 51 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Writes canonical PSO (inertia weight m, cognitive and social pulls toward personal and global bests, uniform random
multipliers) as a second-order system of SDEs, replaces the personal-best memory by an extra ODE
dY = nu (X - Y) S_beta(X, Y) dt and the global best by the CBO Gibbs average, and then derives formally the
mean-field Vlasov-Fokker-Planck equation for the PSO swarm. In the small-inertia (overdamped) limit m -> 0 the
kinetic equation reduces to the CBO equation, so CBO is a hydrodynamic approximation of PSO. Numerics (N = 5e5
particles in 1D, d = 20 benchmarks) confirm agreement between particles and mean-field solvers.

## Contribution

First continuous-time stochastic model of PSO with memory that admits a formal mean-field limit; makes explicit the
family tree PSO (second order, inertial) -> CBO (first order, overdamped) used by later rigorous work
([[cipriani-2022-zero]] proved the zero-inertia limit; [[huang-2023-global]] proved global convergence).

## Key results

- Derived: discrete PSO = semi-implicit Euler-Maruyama discretisation (dt = 1) of
  m dV = -gamma V dt + lambda1 (Y - X) dt + lambda2 (Ybar - X) dt + sigma1 D(Y - X) dB1 + sigma2 D(Ybar - X) dB2,
  dX = V dt, with gamma = 1 - m acting as friction. Classic c_k = 2 corresponds to lambda = 1, sigma = 1/sqrt(3).
- Derived (formal): mean-field Vlasov-Fokker-Planck equation for f(x, y, v, t); with m = eps -> 0 a local
  Maxwellian closure yields the CBO PDE with component-wise (anisotropic) diffusion, and a new CBO-with-local-best.
- Measured (1D, Ackley/Rastrigin): with personal best only, the swarm concentrates on every local minimum
  (memory peaks); adding the global best removes this and converges faster than the memoryless model.
- Measured: as m decreases (0.5, 0.1, 0.01) the PSO density converges to the CBO mean-field density.
- Measured (d = 20): with alpha up to 5e4 and the stabilised weight exp(-alpha (F - F_min)), success on Ackley and
  Rastrigin improves; classical PSO parameter constraints gave poor success rates, as did Matlab's particleswarm with
  default PSO settings (stated by the authors, numbers in tables).

## Methods and models

SDE models (2.7)-(2.15), regularised global best X_alpha (Laplace principle), sigmoid S_beta = 1 + tanh(beta(F(y) -
F(x))). Particle solver: semi-implicit scheme equivalent to discrete PSO at dt = 1, nu = 0.5. Mean-field solver:
dimensional splitting with second-order semi-Lagrangian transport, implicit central Fokker-Planck, Lax-Wendroff for
the memory term (second order was essential to resolve memory peaks). Grids 90 x 120 in (x, v). High-dimensional
tests on Ackley, Griewank, Rastrigin, Salomon, Schwefel and Xin-She Yang random function, 500 runs each, success
= sup-norm error < 0.25. No code link in the paper.

## Limitations and open questions

All limits are formal: rigorous mean-field and small-inertia limits are left open (later partly closed by
[[cipriani-2022-zero]] and [[huang-2023-global]]). Parameter tuning for the d = 20 tests was rough grid variation.
The benchmarks are again origin-centred (the authors shift to x = 1, 2 in some tables). The comparison with standard
PSO is anecdotal rather than a controlled benchmark.

## Relevance to us

Gives the exact dictionary between PSO and kinetic/active-matter language (inertia, friction, multiplicative noise,
Vlasov-Fokker-Planck), which is what we need to talk about "swarm optimisers as swarm dynamics". Pair with
[[pinnau-2017-consensus]], [[clerc-2002-particle]] (constriction from the discrete dynamical-systems side) and
[[kadirkamanathan-2006-stability]] (Lyapunov view).
