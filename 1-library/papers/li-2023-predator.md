---
id: li-2023-predator
type: paper
title: Predator–prey survival pressure is sufficient to evolve swarming behaviors
authors:
- Jianan Li
- Liang Li
- Shiyu Zhao
year: 2023
venue: New Journal of Physics
url: https://arxiv.org/abs/2308.12624
doi: 10.1088/1367-2630/acf33a
arxiv: '2308.12624'
cite: Li, J., Li, L., & Zhao, S. (2023). Predator–prey survival pressure is sufficient to evolve swarming behaviors. New Journal of Physics, 25(9), 092001.
topics:
- marl-emergence
- collective-motion
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 23 (Crossref, 2026-10-03); 25 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Most RL models of collective motion hand-craft rewards that implicitly favour aggregation. Here prey and predators co-evolve with mixed cooperative-competitive MARL under a reward based only on survival: prey get -1 when caught, predators +1. The abstract reports a rich set of emergent behaviours: flocking and swirling (milling) in prey, and dispersion, confusion and marginal predation tactics in predators.

## Contribution

Moves the "why flock?" question from proxy rewards (cohesion in [[durve-2020-learning]], collision-cost in [[brambati-2025-learning]]) to the primary selective pressure the earlier papers only speculated about, predation. Follow-up interpretability work is [[mi-2026-unveiling]].

## Key results

- Flocking and swirling of prey emerge without any alignment or cohesion term in the reward (claimed in abstract).
- Predators learn dispersion, exploit confusion, and pick off marginal prey (claimed).

## Methods and models

Mixed cooperative-competitive MARL with a predator-prey coevolution framework (algorithm details not read; abstract level).

## Limitations and open questions

Abstract-level read; whether swarming depends on sensing range, speed ratios or network architecture was not checked. Relation to the empirical selfish-herd literature not examined here.

## Relevance to us

Directly answers the open question posed by [[durve-2020-learning]]; a strong candidate baseline for a predator-prey swarm experiment. Compare with [[baker-2020-emergent]] for competitive autocurricula and [[mi-2026-unveiling]] for interpreting the learned policies.
