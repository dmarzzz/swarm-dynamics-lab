---
id: carrillo-2022-consensus
type: paper
title: Consensus-based sampling
authors: [José A. Carrillo, Franca Hoffmann, Andrew M. Stuart, Urbain Vaes]
year: 2022
venue: Studies in Applied Mathematics
url: https://arxiv.org/abs/2106.02519
doi: 10.1111/sapm.12470
arxiv: '2106.02519'
cite: Carrillo, J. A., Hoffmann, F., Stuart, A. M., & Vaes, U. (2022). Consensus-based sampling. Studies in Applied Mathematics, 148(3), 1069–1140. https://doi.org/10.1111/sapm.12470
topics: [swarm-intelligence, sync-consensus]
added_by: dmarz/swarm-intelligence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: 36 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Proposes consensus-based sampling (CBS): an interacting particle system in which each particle relaxes toward the
Gibbs-weighted mean of the ensemble and is driven by noise scaled by the Gibbs-weighted covariance, rather than by its
own distance to the mean as in CBO. One parameter lambda switches the same dynamics between optimisation mode
(lambda = 1, the ensemble collapses onto a minimiser) and sampling mode (lambda = (1 + beta)^-1, the ensemble
approximates a target measure). The method is derivative-free and affine invariant, so it suits Bayesian inverse
problems with expensive black-box forward models.

## Contribution

Connects the CBO family ([[pinnau-2017-consensus]], [[carrillo-2021-consensus]]) with ensemble Kalman methods
(ensemble Kalman sampler, affine-invariant samplers): it borrows covariance-scaled noise and affine invariance from
the latter and the Laplace-principle weighting from the former. It is the starting point for the consensus-based
sampling literature that [[gerber-2025-mean]] and [[koss-2026-mean]] analyse.

## Key results

- Proved: both the discrete iteration and the continuous mean-field dynamics are affine invariant (Section 2.3.2).
- Proved (Gaussian target, quadratic objective): explicit evolution of mean and covariance; algebraic convergence
  in optimisation mode and exponential convergence in sampling mode (Propositions 2.4-2.6).
- Proved (optimisation mode, lambda = 1): the ensemble collapses (Proposition 3.4) and, under convexity-type
  conditions, converges to a point near the minimiser in W2 (Theorem 3.5); in d = 1 with a rate
  (Propositions 3.7-3.8).
- Proved (sampling mode): existence of steady states for large beta that recover a Laplace approximation of the
  target (Theorem 3.9; d = 1 for the Laplace results).
- Measured: numerical examples show wide basins of attraction for optimisation and that the Laplace approximation
  attracts many initial conditions; sampling is accurate only when the target is unimodal and near-Gaussian.

## Methods and models

Mean-field McKean-Vlasov SDE d theta = -(theta - M_beta(rho)) dt + sqrt(2 lambda^-1 C_beta(rho)) dW, where M_beta and
C_beta are the mean and covariance of rho weighted by exp(-beta f); a discrete-time variant with step parameter
alpha in [0, 1). Analysis by moment equations, Holley-Stroock-type bounds and Wasserstein estimates. I read the
abstract, introduction, Section 2 statements and the main theorem statements of Section 3, not the proofs or all
numerics.

## Limitations and open questions

Sampling is only correct in an asymptotic regime and for near-Gaussian targets; multimodal posteriors are not
sampled faithfully. Several Laplace-approximation results are restricted to d = 1. Mean-field limit is assumed, not
proved here.

## Relevance to us

Shows that the same swarm consensus dynamics can be tuned from "collapse" (optimise) to "maintain spread" (sample)
by one noise parameter; a useful knob if the hackathon studies diversity-versus-convergence in swarms. Pair with
[[pinnau-2017-consensus]], [[totzeck-2021-trends]] and [[bailo-2024-cbx]] (CBX implements CBS).
