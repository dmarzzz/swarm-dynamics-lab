---
id: sartorio-2025-minimalist
type: paper
title: "Minimalist exploration strategies for robot swarms at the edge of chaos"
authors: ["Vinicius Sartorio", "Luigi Feola", "Vito Trianni", "Jonata Tyska Carvalho"]
year: 2025
venue: "Proceedings of the Genetic and Evolutionary Computation Conference (GECCO 2025)"
url: https://arxiv.org/abs/2406.13641
doi: "10.1145/3712256.3726311"
arxiv: "2406.13641"
cite: "Sartorio, V., Feola, L., Trianni, V., & Carvalho, J. T. (2025). Minimalist exploration strategies for robot swarms at the edge of chaos. In Proceedings of the Genetic and Evolutionary Computation Conference (GECCO '25) (pp. 1567-1576). ACM. (arXiv:2406.13641)"
topics: [swarm-robotics, criticality-measurement]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "1 (OpenAlex W4412106727, 2026-10-03); 1 (Crossref, 2026-10-03)"
code: []
---

## Summary

For very constrained robots that can only random-walk, the authors use Random Boolean Networks as controllers for simulated Kilobots. RBN-generated walks beat the best-tuned Lévy-modulated correlated random walk on an exploration task. Chaotic or edge-of-chaos network dynamics maximise exploration, and evolutionary optimisation can improve exploration while keeping the networks chaotic.

## Contribution

It links the 'edge of chaos' idea from complex systems to a concrete swarm-robotics function (exploration) with a minimal controller.

## Key results

- RBN controllers significantly outperform the best Lévy-modulated correlated random walk (simulation, per the abstract).
- Chaotic dynamics are beneficial for exploration.

## Methods and models

Random Boolean Network controllers on simulated Kilobots, plus evolutionary robotics optimisation. The arXiv v1 lists an additional author (Emanuel Estrada); I use the published GECCO author list.

## Limitations and open questions

Abstract-depth entry. Simulation only. Exploration task only.

## Relevance to us

An edge-of-chaos hypothesis applied to swarms, relevant to criticality discussions; compare [[verdoucq-2025-flocking]].
