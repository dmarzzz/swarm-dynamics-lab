---
id: dorigo-1997-ant
type: paper
title: 'Ant colony system: a cooperative learning approach to the traveling salesman problem'
authors:
- Marco Dorigo
- Luca Maria Gambardella
year: 1997
venue: IEEE Transactions on Evolutionary Computation
url: https://doi.org/10.1109/4235.585892
doi: 10.1109/4235.585892
arxiv: null
cite: 'Dorigo, M., & Gambardella, L. M. (1997). Ant colony system: A cooperative learning approach to the traveling salesman problem. IEEE Transactions on Evolutionary Computation, 1(1), 53–66. https://doi.org/10.1109/4235.585892'
topics:
- swarm-intelligence
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 8104 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Introduces Ant Colony System (ACS) for the TSP: cooperating ants communicate indirectly through pheromone deposited
on graph edges while building solutions. Experiments study how ACS operates; ACS outperforms other nature-inspired
methods such as simulated annealing and evolutionary computation, and ACS-3-opt (with local search) is compared to
some of the best algorithms for symmetric and asymmetric TSP.

## Contribution

Strengthens AS ([[dorigo-1996-ant]]) with more exploitative state transitions and local/global pheromone updates;
establishes the pattern "ACO + local search" that made ACO competitive.

## Key results

- Claimed in abstract: ACS beats SA and EC on tested TSPs; ACS-3-opt competitive with best TSP algorithms of the
  time (numbers not read).

## Methods and models

ACS on symmetric/asymmetric TSP benchmarks with and without 3-opt local search (abstract only).

## Limitations and open questions

Abstract-level reading; much of the performance comes from the local search component.

## Relevance to us

Background for ACO variants; illustrates how much of a swarm algorithm's success can come from a non-swarm component.
