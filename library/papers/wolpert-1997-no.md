---
id: wolpert-1997-no
type: paper
title: No free lunch theorems for optimization
authors:
- David H. Wolpert
- William G. Macready
year: 1997
venue: IEEE Transactions on Evolutionary Computation
url: https://doi.org/10.1109/4235.585893
doi: 10.1109/4235.585893
arxiv: null
cite: Wolpert, D. H., & Macready, W. G. (1997). No free lunch theorems for optimization. IEEE Transactions on Evolutionary Computation, 1(1), 67–82. https://doi.org/10.1109/4235.585893
topics:
- swarm-intelligence
- meta
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 14350 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Develops a framework linking optimisation algorithms to the problems they solve and proves "no free lunch" theorems:
averaged over all problems, any elevated performance of an algorithm on one class is offset by worse performance on
another. Gives a geometric interpretation of algorithm-problem fit, applications to information-theoretic aspects and
benchmark measures, time-varying problems, and head-to-head minimax distinctions that survive NFL.

## Contribution

Foundational limit result cited, and often misread, by nearly every new metaheuristic paper to justify yet another
algorithm; [[camacho-villalon-2023-exposing]] and [[velasco-2024-literature]] discuss that misuse.

## Key results

- Proved (abstract): performance averaged uniformly over all objective functions is identical for all algorithms.

## Methods and models

Probabilistic analysis over the space of cost functions (abstract only).

## Limitations and open questions

Abstract-level reading. Uniform average over all functions is not representative of structured real problems, so NFL
does not by itself justify new algorithms.

## Relevance to us

Needed to frame any "our swarm beats X" claim correctly: specify the problem class.
