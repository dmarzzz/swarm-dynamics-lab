---
id: kudela-2023-evolutionary
type: paper
title: The Evolutionary Computation Methods No One Should Use
authors:
- Jakub Kudela
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2301.01984
doi: null
arxiv: '2301.01984'
cite: Kudela, J. (2023). The evolutionary computation methods no one should use. arXiv preprint arXiv:2301.01984. https://doi.org/10.48550/arXiv.2301.01984
topics:
- swarm-intelligence
- meta
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: 9 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Proposes a simple shift test for centre-bias: run each optimiser on 13 classic benchmark functions (d = 30, 50,000
evaluations, 20 runs) unshifted and shifted by 10% of the range, take the per-function ratio of mean errors, and flag
a method if the geometric mean ratio exceeds 10. Applied to 90 evolutionary and swarm methods from the mealpy library
and MathWorks repositories (published 1987-2022), 47 of 90 have a centre-bias operator; the first is from 2012 and
nearly all recent "novel" methods are affected.

## Contribution

Scales up [[kudela-2022-critical]] from 7 methods to 90 with a cheap, reproducible diagnostic, turning a qualitative
critique ([[sorensen-2015-metaheuristics]], [[aranha-2022-metaphor]]) into a measured, per-method verdict.

## Key results

- Measured: 47/90 methods show centre-bias (geometric-mean shifted/unshifted error ratio > 10).
- Measured: classic methods pass: ABC 1.29, DE 0.97, PSO 0.97, ACO_R 0.74, ES (2002 variant) 1.14, SA 0.90, LSHADE 1.03.
- Measured: extreme centre-bias in "math-inspired" methods: Arithmetic Optimization Algorithm 1.01e10, Runge Kutta
  Optimizer 7.36e4, Sine Cosine Algorithm 1.18e4, Gradient-Based Optimizer 7.17e7; Grey Wolf Optimizer 8.89e5;
  Whale Optimization 1.87e3; Harris Hawks 1.62e5.
- Measured: earliest centre-biased methods are TLBO (2012), Wind Driven Optimization (2013), Grey Wolf (2014); the
  count of biased methods grows sharply after 2015 (Figure 1).
- Reported: one author group (Mirjalili, Gandomi, Heidari) is associated with 20 of the 47 biased methods.
- Sanity check: the only function with an off-centre optimum (Schwefel 2.26, F08) shows ratio near 1 for all methods.

## Methods and models

Benchmarks: Sphere, Schwefel 2.22/1.2/2.21, Rosenbrock, Step, Quartic with noise, Schwefel 2.26, Rastrigin, Ackley,
Griewank, Penalized 1/2 at d = 30. Shift s = 10% of the range. Errors floored at 1e-8. Implementations: mealpy
(https://doi.org/10.5281/zenodo.3711948) and MathWorks code; baseline (original) versions only, not "improved"
variants.

## Limitations and open questions

Short arXiv note, not peer reviewed at the time of reading. Relies on third-party implementations that may differ
from the original papers. The threshold of 10 and the single 10% shift are heuristic. Only bias toward the centre is
tested; other structural biases (toward boundaries, axes) are not. Methods that pass the test are not thereby shown
to be novel (Kudela notes HS, CS, FA, MFO, ALO are equivalent to older methods).

## Relevance to us

Any hackathon experiment that benchmarks a swarm optimiser must use shifted/rotated problems (e.g. BBOB) or this
artefact will dominate. Pairs with [[vermetten-2024-large]] (294 implementations on BBOB) and
[[camacho-villalon-2023-exposing]].
