---
id: fornasier-2021-consensus
type: paper
title: 'Consensus-Based Optimization on the Sphere: Convergence to Global Minimizers and Machine Learning'
authors: [Massimo Fornasier, Lorenzo Pareschi, Hui Huang, Philippe Sünnen]
year: 2021
venue: Journal of Machine Learning Research
url: https://jmlr.org/papers/v22/21-0259.html
doi: null
arxiv: '2001.11988'
cite: 'Fornasier, M., Pareschi, L., Huang, H., & Sünnen, P. (2021). Consensus-based optimization on the sphere: Convergence to global minimizers and machine learning. Journal of Machine Learning Research, 22(237), 1–55.'
topics: [swarm-intelligence, sync-consensus, collective-motion]
added_by: dmarz/swarm-intelligence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null  # OpenAlex lookup rate-limited (HTTP 429) during this audit, 2026-10-03
code: []
---

## Summary

Recasts consensus-based optimisation on the unit sphere as a stochastic Kuramoto-Vicsek (sKV) model: particles move
on S^{d-1} with a drift toward a Gibbs-weighted consensus point and a projected noise whose variance is proportional
to their distance from it, so noise vanishes at consensus. They prove that the numerical scheme converges to global
minimisers for well-prepared initial data, and show the method scaling to high dimension on phase retrieval and robust
subspace detection, where it performs about as well as specialised state-of-the-art methods.

## Contribution

Makes the swarm-optimisation-equals-flocking link explicit: the optimiser is literally a noisy Kuramoto-Vicsek
alignment model with a fitness-weighted leader. Extends the CBO theory of [[carrillo-2018-analytical]] to a manifold
constraint and adds a full convergence chain (particles to mean field to global minimiser) for the implemented
algorithm, which earlier CBO papers lacked.

## Key results

- Proved (Theorem 1.1 with Theorem 3.1): for E in C^2 on the sphere and well-prepared initial datum, the
  discretised particle scheme approximates a global minimiser with high probability, combining mean-field convergence
  ([31] in the paper), large-time asymptotics of the PDE and classical SDE discretisation error.
- Measured (Ackley on S^2, N = 50, 1000 runs): 100% success for all tested (sigma, alpha), although the swarm does
  not always reach exact consensus.
- Measured (Ackley on S^19, sigma = 0.3, dt = 0.05, alpha = 5e4, T = 100, 100 runs, minimum at the pole or shifted
  to (d^-1/2, ..., d^-1/2)): success 98-100% for N = 50, 100, 200 and the tested batch sizes M (Table 1); a "fast"
  variant that shrinks the particle number during the run gives better accuracy per cost (Table 2).
- Reported: on phase retrieval and robust subspace detection, KV-CBO is competitive with dedicated methods (I did
  not check the comparison tables in detail).

## Methods and models

SDE dV^i = lambda P(V^i) v_alpha dt + sigma |V^i - v_alpha| P(V^i) dB^i - (d-1) sigma^2 |V^i - v_alpha|^2 V^i / 2 dt
(projection P onto the tangent space), with v_alpha the Laplace-weighted mean. Algorithm 1 adds mini-batches and a
fast first-order projected scheme. Code: https://github.com/PhilippeSu/KV-CBO (Matlab). I read the introduction,
main theorem statement, algorithm section and the Ackley experiments, not the proofs.

## Limitations and open questions

Convergence needs well-prepared initial data concentrated enough near the minimiser, a locality-flavoured assumption.
Restricted to the sphere; general manifolds came later. Benchmarks on Ackley are again landscapes with a dominant
global basin (see the centre-bias critique in [[kudela-2022-critical]]).

## Relevance to us

The cleanest bridge between [[vicsek-1995-novel]]-type alignment dynamics and swarm optimisation in the library: a
hackathon project could reuse KV-CBO as "flocking that optimises" and measure Kuramoto order parameters during
optimisation. Pair with [[pinnau-2017-consensus]], [[carrillo-2021-consensus]], [[huang-2023-global]].
