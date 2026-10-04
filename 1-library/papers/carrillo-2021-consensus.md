---
id: carrillo-2021-consensus
type: paper
title: A consensus-based global optimization method for high dimensional machine learning problems
authors: [José A. Carrillo, Shi Jin, Lei Li, Yuhua Zhu]
year: 2021
venue: 'ESAIM: Control, Optimisation and Calculus of Variations'
url: https://arxiv.org/abs/1909.09249
doi: 10.1051/cocv/2020046
arxiv: '1909.09249'
cite: 'Carrillo, J. A., Jin, S., Li, L., & Zhu, Y. (2021). A consensus-based global optimization method for high dimensional machine learning problems. ESAIM: Control, Optimisation and Calculus of Variations, 27, S5. https://doi.org/10.1051/cocv/2020046'
topics: [swarm-intelligence, sync-consensus]
added_by: dmarz/swarm-intelligence-audit
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: 100 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Modifies the original consensus-based optimisation (CBO) of [[pinnau-2017-consensus]] in two ways so that it works
in high dimension: the isotropic noise sigma |X - x*| dW is replaced by component-wise (anisotropic) geometric
Brownian motion, which removes the dimension from the consensus condition, and the weighted average x* and the
objective are both computed on random mini-batches (of particles and of data). They prove exponential convergence of
the mean-field Fokker-Planck equation, in continuous and semi-discrete time, under parameter conditions independent
of d, and test on 1D landscapes, 20D Rastrigin and MNIST.

## Contribution

The paper that made CBO dimension-robust. The isotropic model needs 2 lambda > d sigma^2 for the swarm to contract; the
component-wise model needs only 2 lambda > sigma^2. Almost every later CBO paper (including the PSO mean-field work
in [[grassi-2021-particle]] and [[huang-2023-global]], and [[fornasier-2024-consensus]]) uses this anisotropic noise.
Random-batch interaction is also what CBX ([[bailo-2024-cbx]]) implements.

## Key results

- Derived (Section 2): for fixed consensus point a, isotropic noise gives d/dt E|X - a|^2 = (-2 lambda + sigma^2 d)
  E|X - a|^2, while component-wise noise gives (-2 lambda + sigma^2) E|X - a|^2. This is the dimension-free condition.
- Proved (Theorem 3.1, Proposition 3.1): with mu := 2 lambda - sigma^2 - (correction terms) > 0 and well-prepared
  initial data, the mean-field variance decays exponentially and the consensus point is within a controllable error
  of the global minimiser for large beta; constants do not depend on d.
- Measured (Rastrigin, d = 20, 100 runs, success = every coordinate within 0.25 of x*): success 94-100% across
  N = 50/100/200 with mini-batch sizes M = 40/70/100 and minimiser shifted to x* = 0, 1, 2, versus the 34-64% reported
  by [[pinnau-2017-consensus]] for isotropic CBO. Partial (mini-batch) updates saved 22-36% compute time.
- Measured (1D landscapes with flat local minima): CBO reaches the global minimum where SGD gets trapped (table in
  Figure 2).
- Measured (MNIST, single-layer softmax net, d = 7290): about 82% test accuracy with 100 particles; with N = 10^4
  about 90%; with 1000 particles slightly better than the best of 1000 SGD runs at equal cost. Mini-batching the
  loss (m = 50) saved 99.5% of loss-evaluation cost without hurting accuracy.
- Observed: for MNIST the explicit diffusion term made little difference (batch randomness already supplies noise),
  and replacing the weighted average by argmin over particles performed similarly; for Rastrigin the noise was
  necessary.

## Methods and models

dX^j = -lambda (X^j - x*) dt + sigma sum_k (X^j - x*)_k dW^j_k e_k, with x* the Gibbs-weighted mean
(weights exp(-beta L)) over a random batch of M particles; Algorithm 2.1 with partial or full updates, a stopping rule
on the change of x*, and a restart with pure Brownian exploration when x* stalls. Proofs via Laplace principle and
variance Lyapunov estimates on the nonlinear Fokker-Planck equation. Initialisation uniform on [-3, 3]^d for the
benchmark tests. No code repository is given in the paper.

## Limitations and open questions

Theory is at the mean-field level only; no particle-to-mean-field rate (later addressed by [[gerber-2025-mean]] and
[[koss-2026-mean]]). The 20D test violates the paper's own sufficient condition (3.8), which the authors acknowledge.
MNIST accuracy (82-90%) is for a tiny network and is compared only with plain SGD at one learning rate, so the ML
claim is a proof of concept. No comparison against PSO, CMA-ES or DE.

## Relevance to us

If the hackathon runs CBO or PSO-like swarms in more than a few dimensions, this is the noise model to use. The
dimension-dependent contraction threshold 2 lambda > d sigma^2 versus 2 lambda > sigma^2 is a clean example of how
a noise model choice moves a swarm's "order-disorder" boundary. Related: [[pinnau-2017-consensus]],
[[carrillo-2018-analytical]], [[carrillo-2022-consensus]], [[totzeck-2021-trends]].
