---
id: cipriani-2022-zero
type: paper
title: 'Zero-inertia limit: from particle swarm optimization to consensus-based optimization'
authors:
- Cristina Cipriani
- Hui Huang
- Jinniao Qiu
year: 2022
venue: SIAM Journal on Mathematical Analysis
url: https://api.openalex.org/works/W3154085036
doi: 10.1137/21M1412323
arxiv: null
cite: 'Cipriani, C., Huang, H., & Qiu, J. (2022). Zero-inertia limit: From particle swarm optimization to consensus-based optimization. SIAM Journal on Mathematical Analysis, 54(3), 3091–3121. https://doi.org/10.1137/21M1412323'
topics:
- swarm-intelligence
- sync-consensus
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 24 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Solves the open problem posed by [[grassi-2021-particle]]: rigorously derives CBO from the SDE model of PSO in the
limit of zero inertia, with a quantified convergence rate, by studying weak and strong convergence of the
McKean-type SDEs in path space; illustrated numerically.

## Contribution

Makes the PSO -> CBO overdamped limit a theorem rather than a formal computation, completing the kinetic hierarchy
PSO (second order) -> CBO (first order).

## Key results

- Claimed in abstract: rigorous zero-inertia limit with quantified rate; numerical examples (numbers not read).

## Methods and models

Probabilistic analysis of McKean-Vlasov SDEs in continuous path space (abstract only).

## Limitations and open questions

Abstract-level reading. Concerns the regularised SDE version of PSO, not the discrete textbook algorithm.

## Relevance to us

The overdamped limit is the same one taken in active-matter models (inertial vs overdamped active Brownian
particles); a clean theoretical link for a swarm-dynamics framing of optimisers.
