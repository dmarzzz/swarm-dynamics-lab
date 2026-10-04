---
id: reynolds-2026-evoflock
type: paper
title: "EvoFlock: evolved inverse design of multi-agent motion"
authors: ["Craig Reynolds"]
year: 2026
venue: "arXiv preprint (to appear in Proceedings of Artificial Life 2026)"
url: https://arxiv.org/abs/2606.25280
doi: null
arxiv: "2606.25280"
cite: "Reynolds, C. (2026). EvoFlock: evolved inverse design of multi-agent motion. arXiv preprint arXiv:2606.25280. To appear in Proceedings of Artificial Life 2026."
topics: [collective-motion, swarm-intelligence]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null  # arXiv-only; OpenAlex budget exhausted and Semantic Scholar rate-limited on 2026-10-03
code: []
---
## Summary

The author of boids proposes an inverse design method for tuning multi-agent motion models: define a fitness function for the desired group behaviour (here proper neighbour spacing, near-target speed and obstacle avoidance) and optimise the many model parameters with a genetic algorithm. A noted finding is that the vivid alignment seen in bird flocks appears to emerge from maintaining proper spacing, without explicitly rewarding alignment.

## Contribution

Practical parameter-tuning approach for boids-like models from their originator; echoes the claim that alignment can be emergent.

## Key results

- Claimed (abstract): alignment emerges from optimising spacing, speed and obstacle avoidance.

## Methods and models

Genetic algorithm over boids parameters; user-defined objective.

## Limitations and open questions

Abstract only; objective is hand-designed.

## Relevance to us

Directly reusable for tuning our simulators; compare [[kim-2025-commanding]] (gradient-based inverse design) and the alignment-is-emergent results in [[brambati-2025-learning]] and [[salahshour-2025-allocentric]].

## Notes from dmarz/collective-motion-recent-audit

Metadata (title, authors, year) cross-checked against the DataCite arXiv record and passes verify. Not found in OpenAlex by arXiv DOI on 2026-10-03, so citations stays null.
