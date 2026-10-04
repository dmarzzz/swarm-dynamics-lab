---
id: burstedde-2001-simulation
type: paper
title: Simulation of pedestrian dynamics using a two-dimensional cellular automaton
authors:
- C Burstedde
- K Klauck
- A Schadschneider
- J Zittartz
year: 2001
venue: 'Physica A: Statistical Mechanics and its Applications'
url: https://arxiv.org/abs/cond-mat/0102397
doi: 10.1016/s0378-4371(01)00141-8
arxiv: cond-mat/0102397
cite: 'Burstedde, C., Klauck, K., Schadschneider, A., & Zittartz, J. (2001). Simulation of pedestrian dynamics using a two-dimensional cellular automaton. Physica A: Statistical Mechanics and its Applications, 295(3-4), 507–525. https://doi.org/10.1016/s0378-4371(01)00141-8'
topics:
- crowds-and-traffic
- swarm-intelligence
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 1786 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Introduces the floor-field cellular automaton for pedestrians: a v_max = 1 lattice model with exclusion and parallel update, in which long-range interactions are mediated by a "floor field" that pedestrians lay down as they move, which diffuses and decays and biases neighbours' transition probabilities. It reproduces lane formation in counterflow and is applied to evacuating a room with reduced visibility.

## Contribution

The founding floor-field CA, which made pedestrian simulation cheap and is explicitly chemotaxis-inspired (virtual rather than chemical trails), so it is a direct analogue of stigmergy in ant colonies.

## Key results

- Simulated (abstract): the floor field alone suffices to produce collective effects such as lane formation in a wide corridor.
- Simulated: evacuation of a large room with failed lights or smoke.

## Methods and models

Two-dimensional lattice, exclusion statistics, parallel dynamics; static and dynamic floor fields with diffusion and decay. Physica A 295(3–4), 507–525. The arXiv version title uses "2-dimensional".

## Limitations and open questions

Discrete space and time limit quantitative realism (later works study discretisation effects); conflicts resolved stochastically. Abstract-level read only.

## Relevance to us

A stigmergic swarm model of humans, bridging crowds to ant-trail and pheromone-based swarm algorithms. Useful as a fast baseline for lattice swarm experiments. Reviewed in [[chowdhury-2000-statistical]] (vehicle CA) and [[corbetta-2023-physics]].
