---
id: lopez-incera-2020-development
type: paper
title: Development of swarm behavior in artificial learning agents that adapt to different foraging environments
authors:
- Andrea López-Incera
- Katja Ried
- Thomas Müller
- Hans J. Briegel
year: 2020
venue: PLOS ONE
url: https://arxiv.org/abs/2004.00552
doi: 10.1371/journal.pone.0243628
arxiv: '2004.00552'
cite: López-Incera, A., Ried, K., Müller, T., & Briegel, H. J. (2020). Development of swarm behavior in artificial learning agents that adapt to different foraging environments. PLOS ONE, 15(12), e0243628.
topics:
- marl-emergence
- collective-motion
- collective-decision
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 18 (Crossref, 2026-10-03)
code: []
---

## Summary

Each agent is a Projective Simulation learner that perceives neighbours and surroundings and is rewarded for reaching food in a one-dimensional world. The type of collective motion that emerges depends on how far the food is: distant resources produce strongly aligned swarms, nearby resources do not. Individual trajectories in aligned swarms are best fit by composite correlated random walks resembling Levy walks, while agents trained for nearby food move in Brownian-like fashion.

## Contribution

Links learned collective motion to foraging ecology and to movement statistics (Levy versus Brownian), using a non-deep RL model (Projective Simulation). Complements the cohesion-based rewards of [[durve-2020-learning]].

## Key results

- Strong alignment emerges when food is far from the starting region (claimed).
- Levy-like composite correlated random walks emerge as a by-product of collective motion; Brownian trajectories for nearby food (claimed).

## Methods and models

Projective Simulation agents in 1D, reward on reaching resources, neighbour-based percepts. Abstract-level read.

## Limitations and open questions

One-dimensional; abstract-level read, so parameter dependence and robustness not checked.

## Relevance to us

Suggests movement-statistics observables (step-length distributions) to measure in learned swarms, beyond polar order. Related: [[loffler-2023-collective]], [[brambati-2025-learning]].
