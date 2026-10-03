---
id: gerber-2025-mean
type: paper
title: Mean-field limits for Consensus-Based Optimization and Sampling
authors: [Nicolai Jurek Gerber, Franca Hoffmann, Urbain Vaes]
year: 2025
venue: 'ESAIM: Control, Optimisation and Calculus of Variations'
url: https://api.openalex.org/works/doi:10.1051/cocv/2025060
doi: 10.1051/cocv/2025060
arxiv: null
cite: 'Gerber, N. J., Hoffmann, F., & Vaes, U. (2025). Mean-field limits for consensus-based optimization and sampling. ESAIM: Control, Optimisation and Calculus of Variations, 31, 74. https://doi.org/10.1051/cocv/2025060'
topics: [swarm-intelligence, sync-consensus]
added_by: dmarz/swarm-intelligence-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 7 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Proves quantitative mean-field limits for two consensus-type interacting particle systems, consensus-based
optimisation (CBO, [[pinnau-2017-consensus]]) and consensus-based sampling (CBS, [[carrillo-2022-consensus]]): as
the number of particles N grows, the particle dynamics converge to the McKean-Vlasov mean-field dynamics at a
quantified rate. Because the CBO/CBS coefficients (Gibbs-weighted mean and covariance) are not globally Lipschitz,
Sznitman's classical coupling argument is generalised by discarding a small-probability event controlled by moment
bounds.

## Contribution

Supplies the missing step that lets mean-field convergence theorems ([[carrillo-2018-analytical]],
[[fornasier-2024-consensus]]) say something about the finite swarms people actually run. Also gives new
well-posedness results for the particle systems and stability estimates for the weighted mean and weighted
covariance.

## Key results

- Claimed (abstract): quantitative mean-field limit results for CBO and CBS; well-posedness of the particle systems
  and their mean-field limits; stability estimates for weighted mean and covariance. The rate and constants were not
  read (abstract only).

## Methods and models

Generalised Sznitman coupling of the N-particle SDE system with N independent copies of the mean-field process,
with a truncation event of small probability handled through moment estimates. Open versions exist on HAL
(hal-04346646), which was behind a bot wall during this audit.

## Limitations and open questions

Unread beyond the abstract. Typical issue for this line: constants grow exponentially with the inverse temperature
alpha and the time horizon (as in [[huang-2023-global]]), so the bounds may be uninformative at practical swarm
sizes; check when read in full.

## Relevance to us

Cite when claiming that a finite CBO swarm behaves like its PDE limit. Pair with [[koss-2026-mean]] (qualitative
mean-field limit for a broader class of consensus methods) and [[totzeck-2021-trends]].
