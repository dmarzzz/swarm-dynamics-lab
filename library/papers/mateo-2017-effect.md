---
id: mateo-2017-effect
type: paper
title: 'Effect of Correlations in Swarms on Collective Response'
authors: ['David Mateo', 'Yoke Kong Kuan', 'Roland Bouffanais']
year: 2017
venue: 'Scientific Reports'
url: https://www.nature.com/articles/s41598-017-09830-w
doi: 10.1038/s41598-017-09830-w
arxiv: null
cite: 'Mateo, D., Kuan, Y. K., & Bouffanais, R. (2017). Effect of Correlations in Swarms on Collective Response. Scientific Reports, 7(1), 10388.'
topics: [criticality-measurement, collective-motion, sync-consensus]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: '45 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

In a canonical collective-motion model hit by a localised moving perturbation (a predator), the
collective response is impaired when agents interact with more than a threshold number of neighbours.
Effective predator avoidance tracks the integrated correlation, which peaks at an intermediate level of
interaction. Two consensus decision-making models on static networks show the same interplay; adding
connections helps against slow perturbations but hurts against fast ones.

## Contribution

Shows that more interaction is not always better and ties optimal responsiveness to a peak in
correlation, with explicit dependence on perturbation timescale.

## Key results

- Collective response to a predator-like perturbation is hindered above a threshold number of interacting neighbours (simulation).
- Avoidance effectiveness follows integrated correlation, which peaks at intermediate interaction.
- Slow perturbations favour more connections; fast perturbations favour fewer (network consensus models).

## Methods and models

Vicsek-like self-propelled particle model with k-nearest-neighbour interactions and a moving
perturbation; linear consensus on static networks.

## Limitations and open questions

Simulation; abstract-level read.

## Relevance to us

Gives a tunable knob (number of neighbours k) and a measurable (integrated correlation) for robot
swarm responsiveness experiments. Follow-up: [[mateo-2019-optimal]]. Contrast [[klamser-2021-collective]].
