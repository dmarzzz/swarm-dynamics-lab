---
id: ferrante-2015-evolution
type: paper
title: "Evolution of Self-Organized Task Specialization in Robot Swarms"
authors: ["Eliseo Ferrante", "Ali Emre Turgut", "Edgar Duéñez-Guzmán", "Marco Dorigo", "Tom Wenseleers"]
year: 2015
venue: "PLOS Computational Biology"
url: https://doi.org/10.1371/journal.pcbi.1004273
doi: "10.1371/journal.pcbi.1004273"
arxiv: null
cite: "Ferrante, E., Turgut, A. E., Duéñez-Guzmán, E., Dorigo, M., & Wenseleers, T. (2015). Evolution of Self-Organized Task Specialization in Robot Swarms. PLOS Computational Biology, 11(8), e1004273."
topics: [swarm-robotics, collective-decision, marl-emergence]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "130 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Uses evolutionary swarm robotics as a model system for the evolutionary origin of division of labour. In a
task-partitioning object-retrieval scenario (two subtasks performed in sequence by different individuals), task partitioning is favoured when environmental features reduce switching costs and increase group
efficiency. An optimal mix of specialists evolves most readily when behaviours for the subtasks exist as
pre-adapted building blocks, but self-organised specialisation can also evolve from scratch from low-level
primitives using grammatical evolution, selecting only on group performance.

## Contribution

Shows that division of labour can emerge in robot swarms without being specified, informing both biology and
swarm engineering of task allocation.

## Key results

- Task partitioning evolves when the environment lowers switching costs (from abstract).
- Specialisation evolves from scratch with grammatical evolution.

## Methods and models

Simulated robot swarm performing sequential object retrieval; grammatical evolution of controllers from
behavioural primitives. Abstract read.

## Limitations and open questions

Simulation only; group-level selection with identical robots.

## Relevance to us

Reference for emergent role differentiation; links to [[berman-2009-optimized]] (designed allocation) and the
marl-emergence topic.
