---
id: oliveri-2021-continuous
type: paper
title: "Continuous learning of emergent behavior in robotic matter"
authors: ["Giorgio Oliveri", "Lucas C. van Laake", "Cesare Carissimo", "Clara Miette", "Johannes T. B. Overvelde"]
year: 2021
venue: "Proceedings of the National Academy of Sciences"
url: https://doi.org/10.1073/pnas.2017015118
doi: "10.1073/pnas.2017015118"
arxiv: null
cite: "Oliveri, G., van Laake, L. C., Carissimo, C., Miette, C., & Overvelde, J. T. B. (2021). Continuous learning of emergent behavior in robotic matter. Proceedings of the National Academy of Sciences, 118(21), e2017015118."
topics: [swarm-robotics, marl-emergence, active-matter]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "26 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

A modular robot assembled from identical autonomous units learns to locomote without central control: each unit
independently adapts its own actuation with a basic Monte Carlo scheme based on its own sensed performance.
Experiments and simulations show the assembly learns and maintains optimal behaviour in a changing environment
and after damage, as long as each unit's memory represents the current environment. Physical connection between
units is enough for learning; no extra communication or central information is required.

## Contribution

Demonstrates decentralised learning through physical coupling alone, a "robotic matter" counterpart to the
social learning in [[ben-zion-2023-morphological]].

## Key results

- Learning succeeds without communication; requirement identified: memory representative of current
  environment (from abstract).

## Methods and models

Chain or assembly of actuated units; per-unit stochastic (Monte Carlo) behaviour updates. Abstract read.

## Limitations and open questions

Simple locomotion task; scaling not checked.

## Relevance to us

Example of emergent coordination via physics plus local learning; relevant to marl-emergence comparisons.
