---
id: dorigo-1996-ant
type: paper
title: 'Ant system: optimization by a colony of cooperating agents'
authors:
- Marco Dorigo
- Vittorio Maniezzo
- A. Colorni
year: 1996
venue: IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics)
url: https://api.openalex.org/works/W2107941094
doi: 10.1109/3477.484436
arxiv: null
cite: 'Dorigo, M., Maniezzo, V., & Colorni, A. (1996). Ant system: Optimization by a colony of cooperating agents. IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics), 26(1), 29–41. https://doi.org/10.1109/3477.484436'
topics:
- swarm-intelligence
- collective-decision
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 12098 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Defines Ant System (AS), the first ant colony optimisation algorithm, from an analogy with ant foraging: artificial
ants build tours on a graph guided by pheromone trails and a greedy heuristic, and reinforce edges of good tours.
The authors identify three ingredients (positive feedback for rapid discovery of good solutions, distributed
computation to avoid premature convergence, and a constructive greedy heuristic for early search), apply AS to the
travelling salesman problem, discuss parameter selection, compare against tabu search and simulated annealing, and
show applicability to asymmetric TSP, quadratic assignment and job-shop scheduling.

## Contribution

Founding journal paper of ACO (building on Dorigo's 1992 thesis); the algorithmic abstraction of the pheromone
trail-recruitment dynamics described for Argentine ants ([[deneubourg-1990-self]]).

## Key results

- Claimed in abstract: AS solves TSP instances and compares with tabu search and simulated annealing; robust across
  asymmetric TSP, QAP and job-shop (numbers not read).

## Methods and models

Probabilistic tour construction with transition probabilities proportional to pheromone^alpha x heuristic^beta,
evaporation and deposition updates (standard AS form; details not read beyond abstract).

## Limitations and open questions

Abstract-level reading. AS itself was soon outperformed by ACS ([[dorigo-1997-ant]]) and MMAS
([[stutzle-2000-max]]); pure AS without local search is weak on large instances.

## Relevance to us

Canonical example of stigmergic coordination turned into an algorithm; the positive-feedback-plus-evaporation loop is
the same bistable recruitment dynamics studied in collective decision-making.
