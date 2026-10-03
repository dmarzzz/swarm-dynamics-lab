---
id: karaboga-2007-powerful
type: paper
title: 'A powerful and efficient algorithm for numerical function optimization: artificial bee colony (ABC) algorithm'
authors:
- Dervis Karaboga
- Bahriye Basturk
year: 2007
venue: Journal of Global Optimization
url: https://api.openalex.org/works/W2143560894
doi: 10.1007/s10898-007-9149-x
arxiv: null
cite: 'Karaboga, D., & Basturk, B. (2007). A powerful and efficient algorithm for numerical function optimization: Artificial bee colony (ABC) algorithm. Journal of Global Optimization, 39(3), 459–471. https://doi.org/10.1007/s10898-007-9149-x'
topics:
- swarm-intelligence
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: 7684 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Presents the Artificial Bee Colony (ABC) algorithm, modelled on honey bee foraging, for optimising multivariable
functions, and compares it with a genetic algorithm, PSO and a particle-swarm-inspired evolutionary algorithm
(PS-EA). The abstract reports that ABC outperforms the other algorithms on the tested functions. (Abstract read via
CORE.)

## Contribution

The most-cited bee-inspired optimiser (about 7.7k citations); one of the "second generation" SI metaphors after PSO and
ACO.

## Key results

- Claimed in abstract: ABC outperforms GA, PSO and PS-EA on multivariable test functions (numbers not read).
- External check: [[kudela-2023-evolutionary]] found no centre-bias in ABC (geometric-mean ratio 1.29); in
  [[vermetten-2024-large]] ABC is effective in low dimension but scales poorly.

## Methods and models

Bee-foraging-inspired population search compared with GA, PSO and PS-EA on multivariable test functions (abstract only).

## Limitations and open questions

Abstract-level reading. Early comparisons were against untuned baselines on centre-symmetric benchmarks.

## Relevance to us

Representative bee-metaphor algorithm; useful as a contrast to actual honeybee collective decision models in the
collective-decision topic.
