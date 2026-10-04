---
id: salman-2024-automatic
type: paper
title: "Automatic design of stigmergy-based behaviours for robot swarms"
authors: ["Muhammad Salman", "David Garzón Ramos", "Mauro Birattari"]
year: 2024
venue: "Communications Engineering"
url: https://doi.org/10.1038/s44172-024-00175-7
doi: "10.1038/s44172-024-00175-7"
arxiv: null
cite: "Salman, M., Garzón Ramos, D., & Birattari, M. (2024). Automatic design of stigmergy-based behaviours for robot swarms. Communications Engineering, 3(1), 30."
topics: [swarm-robotics, swarm-intelligence]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "26 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Stigmergy, coordination through modifications of the environment such as pheromone trails, has inspired swarm
algorithms but stigmergic robot behaviours have always been hand-designed. The authors show that an automatic
design process (optimisation in simulation, in the AutoMoDe line) can generate collective behaviours for robots
that lay and sense artificial pheromones, and that these are as good as or better than manually designed ones,
exhibiting spatial organisation, memory and communication through the pheromone field.

## Contribution

Extends automatic modular design ([[francesca-2014-automode]]) to stigmergy, linking the swarm-intelligence
(ant algorithms) and swarm-robotics topics with physical experiments.

## Key results

- Automatically designed stigmergic behaviours match or beat manual designs (from abstract; numbers not checked).

## Methods and models

Robots that lay and sense artificial pheromones; simulation-based optimisation of controllers. Abstract read;
how pheromones are physically implemented and the real-robot protocol not checked.

## Limitations and open questions

Artificial pheromone requires special infrastructure; tasks are benchmark missions.

## Relevance to us

Concrete pipeline for automatically discovering stigmergic swarm behaviours; compare [[wang-2021-emergent]]
(robots coupled through a depletable light field).
