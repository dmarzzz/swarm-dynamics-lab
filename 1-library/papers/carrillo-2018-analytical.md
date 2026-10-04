---
id: carrillo-2018-analytical
type: paper
title: An analytical framework for consensus-based global optimization method
authors:
- José A. Carrillo
- Young-Pil Choi
- Claudia Totzeck
- Oliver Tse
year: 2018
venue: Mathematical Models and Methods in Applied Sciences
url: https://arxiv.org/abs/1602.00220
doi: 10.1142/S0218202518500276
arxiv: '1602.00220'
cite: Carrillo, J. A., Choi, Y.-P., Totzeck, C., & Tse, O. (2018). An analytical framework for consensus-based global optimization method. Mathematical Models and Methods in Applied Sciences, 28(06), 1037–1066. https://doi.org/10.1142/S0218202518500276
topics:
- swarm-intelligence
- sync-consensus
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 131 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Provides the analytical framework for the consensus-based optimisation model of [[pinnau-2017-consensus]] with noise:
justifies the algorithm in the mean-field sense by proving convergence to the global minimiser for a large class of
functions, and illustrates consensus estimates by simulations of variants including nonlinear diffusion.

## Contribution

Supplies the stochastic (sigma > 0) mean-field convergence theory that the founding CBO paper deferred; introduces the
variance-based Lyapunov argument reused for PSO by [[huang-2023-global]].

## Key results

- Claimed in abstract: mean-field convergence to the global minimiser for a large class of objectives; numerical
  illustration of consensus estimates (numbers not read).

## Methods and models

Well-posedness and long-time analysis of the nonlocal Fokker-Planck/McKean-Vlasov equation; simulations
(abstract only).

## Limitations and open questions

Abstract-level reading. Initial-datum well-preparation assumptions; later relaxed by [[fornasier-2024-consensus]].

## Relevance to us

Theory backbone for CBO as a swarm-dynamics model; cite alongside [[pinnau-2017-consensus]].
