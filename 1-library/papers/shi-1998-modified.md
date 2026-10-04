---
id: shi-1998-modified
type: paper
title: A modified particle swarm optimizer
authors:
- Yuhui Shi
- Russell Eberhart
year: 1998
venue: 1998 IEEE International Conference on Evolutionary Computation Proceedings (IEEE World Congress on Computational Intelligence)
url: https://doi.org/10.1109/ICEC.1998.699146
doi: 10.1109/ICEC.1998.699146
arxiv: null
cite: Shi, Y., & Eberhart, R. (1998). A modified particle swarm optimizer. In 1998 IEEE International Conference on Evolutionary Computation Proceedings. IEEE World Congress on Computational Intelligence (pp. 69–73). IEEE. https://doi.org/10.1109/ICEC.1998.699146
topics:
- swarm-intelligence
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 10253 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Adds an inertia weight w multiplying the previous velocity in the PSO update and shows by simulation that this new
parameter has a significant effect on optimiser behaviour. The abstract contrasts PSO, where particles adjust
"flying" from their own and companions' experience, with evolutionary computation's genetic operators.

## Contribution

Defines the "canonical" PSO with inertia that most later variants and theory use; inertia is the knob that trades
exploration against convergence. In the SDE picture of [[grassi-2021-particle]], w = m sets friction gamma = 1 - m.

## Key results

- Claimed in abstract: inertia weight has a significant and effective impact on performance (numbers not read).

## Methods and models

PSO velocity update v <- w v + c1 r1 (p - x) + c2 r2 (g - x); simulations on test functions (abstract only).

## Limitations and open questions

Abstract-level reading; the choice of w was empirical. Later theory ([[clerc-2002-particle]], [[trelea-2003-particle]])
gave stability regions for (w, c).

## Relevance to us

Inertia is the parameter that moves a swarm optimiser between underdamped (exploratory, oscillating) and overdamped
(CBO-like) regimes, see [[cipriani-2022-zero]]; useful for any experiment mapping regimes of swarm search.
