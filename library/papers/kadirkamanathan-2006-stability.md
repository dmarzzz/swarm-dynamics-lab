---
id: kadirkamanathan-2006-stability
type: paper
title: Stability analysis of the particle dynamics in particle swarm optimizer
authors:
- Visakan Kadirkamanathan
- Kirusnapillai Selvarajah
- Peter J. Fleming
year: 2006
venue: IEEE Transactions on Evolutionary Computation
url: https://api.openalex.org/works/W2016695533
doi: 10.1109/TEVC.2005.857077
arxiv: null
cite: Kadirkamanathan, V., Selvarajah, K., & Fleming, P. J. (2006). Stability analysis of the particle dynamics in particle swarm optimizer. IEEE Transactions on Evolutionary Computation, 10(3), 245–255. https://doi.org/10.1109/TEVC.2005.857077
topics:
- swarm-intelligence
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 375 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Drops the assumption, used in earlier PSO stability analyses, that all parameters are nonrandom, and analyses the
stochastic particle dynamics with Lyapunov stability theory and passive-systems concepts. Derives sufficient
conditions for stability and confirms in simulation the theoretical prediction that stability requires increasing
the maximum value of the random parameter when the inertia factor is reduced.

## Contribution

Brings control-theory tools (Lyapunov, passivity) to PSO and handles randomness explicitly, a step between
[[clerc-2002-particle]]'s deterministic analysis and the stochastic mean-field results of [[huang-2023-global]].

## Key results

- Claimed in abstract: sufficient stability conditions for stochastic PSO; simulation confirms coupling between
  inertia and the bound on the random acceleration (numbers not read).

## Methods and models

Lyapunov/passivity analysis of the particle dynamics treated as a feedback system with random gains (abstract only).

## Limitations and open questions

Abstract-level reading. Sufficient (conservative) conditions; single-particle, stagnation-style analysis.

## Relevance to us

Control-community vocabulary for swarm optimiser stability; useful if we frame swarm search as a feedback system.
