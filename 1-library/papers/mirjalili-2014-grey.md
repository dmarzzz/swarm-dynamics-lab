---
id: mirjalili-2014-grey
type: paper
title: Grey Wolf Optimizer
authors:
- Seyedali Mirjalili
- Seyed Mohammad Mirjalili
- Andrew Lewis
year: 2014
venue: Advances in Engineering Software
url: https://doi.org/10.1016/j.advengsoft.2013.12.007
doi: 10.1016/j.advengsoft.2013.12.007
arxiv: null
cite: Mirjalili, S., Mirjalili, S. M., & Lewis, A. (2014). Grey Wolf Optimizer. Advances in Engineering Software, 69, 46–61. https://doi.org/10.1016/j.advengsoft.2013.12.007
topics:
- swarm-intelligence
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: 19423 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Proposes the Grey Wolf Optimizer (GWO), a metaheuristic modelled on the leadership hierarchy (alpha, beta, delta,
omega) and hunting steps (searching, encircling, attacking prey) of grey wolves. Benchmarked on 29 test functions
against PSO, GSA, DE, EP and ES with "very competitive" results, plus three engineering design problems and an optics
application. (Abstract read via CORE.)

## Contribution

One of the most cited metaphor-based algorithms (about 19k citations), and the canonical target of the metaphor
critique: included here as the case study, not as a recommended method.

## Key results

- Claimed in abstract: competitive with PSO, GSA, DE, EP, ES on 29 functions (numbers not read).
- External findings: [[kudela-2023-evolutionary]] measures strong centre-bias (geometric-mean shift ratio 8.89e5);
  [[camacho-villalon-2023-exposing]] shows its components are pre-existing PSO/EA ideas under new names.

## Methods and models

Population search organised by a four-level alpha/beta/delta/omega hierarchy and three hunting phases; 29 benchmark functions and engineering design problems (abstract only).

## Limitations and open questions

Abstract-level reading. Benchmarks with optima at the origin make the reported performance unreliable (see
external findings above).

## Relevance to us

Cautionary example for the hackathon: high citations do not imply algorithmic novelty or performance.
