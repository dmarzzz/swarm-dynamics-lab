---
id: munoz-gil-2026-emergent
type: paper
title: Emergent aggregation from collective foraging
authors:
- Gorka Muñoz-Gil
- Andrea López-Incera
- Vide Ramsten
- Giovanni Volpe
- Thomas Müller
- Hans J. Briegel
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.28046
doi: null
arxiv: '2608.28046'
cite: Muñoz-Gil, G., López-Incera, A., Ramsten, V., Volpe, G., Müller, T., & Briegel, H. J. (2026). Emergent aggregation from collective foraging. arXiv preprint arXiv:2608.28046.
topics:
- marl-emergence
- collective-motion
- collective-decision
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

RL foragers start as random walkers and optimise their movement for a purely individual reward, finding replenishable targets, while perceiving only conspecifics and never the targets. As visual range grows, agents undergo a sharp crossover from environment-tuned individual search to a scale-agnostic collective search, coinciding with the onset of spatial aggregation. A minimal first-passage model reproduces the crossover analytically, so a collective phase arises as a by-product of optimal foraging without any reward for grouping.

## Contribution

The cleanest 2026 statement of "indirect, resource-driven reward as a generic route to collective phenomena", extending [[lopez-incera-2020-development]] and complementing the cohesion and collision rewards of [[durve-2020-learning]] and [[brambati-2025-learning]] and the predation reward of [[li-2023-predator]].

## Key results

- Sharp crossover in search strategy with visual range, coinciding with aggregation onset (claimed in abstract).
- First-passage model reproduces the transition (claimed).

## Methods and models

RL foragers (Projective Simulation family, inferred from the authors; not checked) perceiving conspecifics only; first-passage analytical model. Abstract-level read.

## Limitations and open questions

Very recent preprint, not peer reviewed; abstract-level read.

## Relevance to us

Strong candidate to replicate or extend: visual range is a single control parameter with a measurable transition. Related: [[loffler-2023-collective]], [[brambati-2025-learning]].
