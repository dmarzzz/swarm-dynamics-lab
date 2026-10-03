---
id: huang-2023-global
type: paper
title: On the global convergence of particle swarm optimization methods
authors:
- Hui Huang
- Jinniao Qiu
- Konstantin Riedl
year: 2023
venue: Applied Mathematics & Optimization
url: https://arxiv.org/abs/2201.12460
doi: 10.1007/s00245-023-09983-3
arxiv: '2201.12460'
cite: Huang, H., Qiu, J., & Riedl, K. (2023). On the global convergence of particle swarm optimization methods. Applied Mathematics & Optimization, 88(2), Article 30. https://doi.org/10.1007/s00245-023-09983-3
topics:
- swarm-intelligence
- sync-consensus
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 57 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Proves, for the continuous-time SDE model of PSO from [[grassi-2021-particle]], that the mean-field dynamics forms
consensus (variance and velocity second moment decay exponentially) and that the consensus point lies within eps of
a global minimiser for large alpha, both with and without personal-best memory, under a tractability (inverse
continuity) condition on the objective. For PSO without memory they also prove a dimension-independent N^{-1}
mean-field approximation rate, giving a probabilistic global convergence statement with polynomial complexity for the
implemented algorithm. They add a mini-batch, parallel implementation and train MNIST classifiers derivative-free.

## Contribution

Closes the theoretical gap left open by [[grassi-2021-particle]]: the first rigorous global-convergence result for a
PSO variant with memory and inertia, transferring the variance-Lyapunov technique developed for CBO
([[carrillo-2018-analytical]], [[fornasier-2024-consensus]]). Prior PSO theory ([[clerc-2002-particle]],
[[trelea-2003-particle]], [[kadirkamanathan-2006-stability]]) gave only stability/convergence to some point.

## Key results

- Proved (Thm 2.5, no memory): under well-prepared initial data and parameters, E[H(t)] (a Lyapunov functional
  combining position variance and velocity energy) decays exponentially with rate chi; E[X_t] -> x_tilde at rate
  chi/2, and for any eps there is alpha_0 with E(x_tilde) - inf E <= eps; with assumption A5,
  |x_tilde - x*| <= eps^nu / eta.
- Proved (Thm 3.3): the same with memory effects (local best Y_t).
- Proved (Thm 4.1): mean-field approximation error of order N^{-1} without curse of dimensionality; combined
  (Thm 4.3) total error <= C_NA dt^m + C_MFA N^{-1} + C_LLN N^{-1} + eps + eps^{2 nu}/eta^2 with high probability.
  C_MFA grows exponentially in alpha and T*.
- Measured (Rastrigin, d = 20, N = 100, alpha = 100, 25 runs per cell): phase diagrams over inertia m and noise
  sigma show a noise threshold above which the swarm explodes and a minimal noise needed for success; larger N lowers
  the minimal noise.
- Measured (MNIST, N = 100 agents, derivative-free): shallow net > 89% test accuracy (SGD reaches similar), small CNN
  almost 97% (vs 98.3% for comparable CNN with SGD). Using local-best positions in the consensus point helped
  substantially; an extra drift toward local best helped less.

## Methods and models

Mean-field McKean processes for (X, Y, V) with anisotropic diffusion D(.), Itô calculus, Laplace principle, Leray-
Schauder well-posedness. Assumptions A1-A5 on the objective (attained infimum, local Lipschitz, quadratic growth or
bounded, C^2 with bounded Hessian for the analysis, inverse continuity). Algorithm 1: random mini-batches over data
and over particles, cooling of alpha (x2 per epoch) and sigma (sigma / log(epoch + 2)), optional variance-based
particle discarding. Code (Matlab): https://github.com/KonstantinRiedl/PSOAnalysis

## Limitations and open questions

Results are in the mean-field law; the finite-N bound is only for the memoryless model and its constant blows up
exponentially in alpha. Well-preparation of the initial datum is a locality-flavoured assumption. The C^2 assumption
is needed for the proofs only. The analysed PSO is the regularised SDE version, not the textbook discrete update with
uniform random multipliers, so claims about "PSO" are about a close relative. MNIST is a modest benchmark.

## Relevance to us

If we want a provable swarm-optimiser baseline whose dynamics we can measure (variance decay, consensus formation,
explosion threshold in (m, sigma)), this is the reference. The (m, sigma) phase diagram is directly analogous to
order-disorder transitions in flocking models; see [[pinnau-2017-consensus]] and [[cipriani-2022-zero]].
