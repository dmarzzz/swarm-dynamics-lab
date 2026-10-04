---
id: neumann-2009-runtime
type: paper
title: Runtime analysis of a simple ant colony optimization algorithm
authors:
- Frank Neumann
- Carsten Witt
year: 2009
venue: Algorithmica
url: https://doi.org/10.1007/s00453-007-9134-2
doi: 10.1007/s00453-007-9134-2
arxiv: null
cite: Neumann, F., & Witt, C. (2009). Runtime analysis of a simple ant colony optimization algorithm. Algorithmica, 54(2), 243. https://doi.org/10.1007/s00453-007-9134-2
topics:
- swarm-intelligence
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 111 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Gives the first runtime analysis of an ACO algorithm (a simple 1-ant ACO on pseudo-Boolean functions), transferring
rigorous results for simple evolutionary algorithms to ACO. Studies the evaporation factor in detail and, using new
lower bounds on tails of sums of independent Poisson trials, proves a phase transition from exponential to
polynomial expected runtime as evaporation varies.

## Contribution

Opens the runtime-complexity theory of ACO, beyond the finite-time convergence results surveyed in [[dorigo-2005-ant]].

## Key results

- Proved (abstract): phase transition in expected runtime (exponential to polynomial) as a function of the
  evaporation factor (exact thresholds not read).

## Methods and models

Probabilistic runtime analysis on OneMax-type pseudo-Boolean functions (abstract only).

## Limitations and open questions

Abstract-level reading. Single-ant, simple functions; far from practical ACO.

## Relevance to us

One of few rigorous "phase transition" results for a swarm-intelligence algorithm; evaporation acts like a
forgetting/temperature parameter.
