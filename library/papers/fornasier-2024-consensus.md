---
id: fornasier-2024-consensus
type: paper
title: Consensus-based optimization methods converge globally
authors:
- Massimo Fornasier
- Timo Klock
- Konstantin Riedl
year: 2024
venue: SIAM Journal on Optimization
url: https://arxiv.org/abs/2103.15130
doi: 10.1137/22M1527805
arxiv: '2103.15130'
cite: Fornasier, M., Klock, T., & Riedl, K. (2024). Consensus-based optimization methods converge globally. SIAM Journal on Optimization, 34(3), 2973–3004. https://doi.org/10.1137/22M1527805
topics:
- swarm-intelligence
- sync-consensus
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 33 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Proves global convergence of CBO in mean-field law for a rich class of nonconvex, nonsmooth, merely locally
Lipschitz objectives, based on the intuition (supported experimentally) that CBO on average performs gradient descent
of the squared distance to the global minimiser. Shows CBO convexifies a large class of problems as the number of
agents grows, establishes a quantitative nonasymptotic Laplace principle, and argues that the hardness of a global
optimisation problem is encoded in the rate of the mean-field approximation, for which a probabilistic estimate is
given.

## Contribution

Strongest general convergence theorem for CBO to date among the entries here; weakens initialisation assumptions of
[[carrillo-2018-analytical]] and supplies the technique reused in [[huang-2023-global]].

## Key results

- Claimed in abstract: convergence in mean-field law under mild assumptions; convexification as N -> infinity;
  quantitative Laplace principle; probabilistic global convergence of numerical CBO (numbers not read).

## Methods and models

Mean-field analysis of anisotropic/isotropic CBO SDEs (abstract only).

## Limitations and open questions

Abstract-level reading. Mean-field approximation constants may grow quickly with alpha; practical rates in high
dimension remain a question.

## Relevance to us

"Hardness lives in the finite-N fluctuation term" is a quantitative statement about how many agents a swarm needs,
directly relevant to swarm-size scaling experiments.
