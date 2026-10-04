---
id: loffler-2023-collective
type: paper
title: Collective foraging of active particles trained by reinforcement learning
authors:
- Robert C. Löffler
- Emanuele Panizon
- Clemens Bechinger
year: 2023
venue: Scientific Reports
url: https://doi.org/10.1038/s41598-023-44268-3
doi: 10.1038/s41598-023-44268-3
arxiv: null
cite: Löffler, R. C., Panizon, E., & Bechinger, C. (2023). Collective foraging of active particles trained by reinforcement learning. Scientific Reports, 13(1), 17055.
topics:
- marl-emergence
- active-matter
- collective-motion
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 17 (Crossref, 2026-10-03)
code: []
---

## Summary

Using an experimental model system of light-responsive active colloidal particles, the authors optimise each particle's motion with RL for foraging randomly appearing food sources. Although each particle maximises only its own reward, collective behaviour emerges in the group. The collective strategy compensates for missing local information and makes the learned policy much more robust.

## Contribution

One of very few MARL-collective-behaviour studies run on physical active matter rather than in pure simulation, extending the Bechinger group's RL-controlled colloids to groups.

## Key results

- Emergence of collective behaviour from individually rewarded foraging (measured in the experimental colloid system, per the abstract).
- Collective strategy increases policy robustness to lack of local information (claimed).

## Methods and models

Light-activated active colloids steered by feedback; RL optimisation of individual policies for foraging. Abstract-level read; the exact algorithm and particle numbers were not checked.

## Limitations and open questions

Abstract-level read. Experimental groups of colloids are small; how much training happened in simulation versus experiment was not checked.

## Relevance to us

Evidence that selfish learning in physical active particles can yield collective behaviour, a useful bridge for any team proposing to move learned swarm policies onto real hardware. Related: [[lopez-incera-2020-development]], [[cai-2025-reinforcement]], [[falk-2021-learning]].
