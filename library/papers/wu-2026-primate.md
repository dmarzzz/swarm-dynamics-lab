---
id: wu-2026-primate
type: paper
title: "Primate-Inspired Cooperation Emergence and Strategy Generation in Heterogeneous Robot Swarm"
authors: ["Bowen Wu", "Renbin Xiao", "Jia Zhao"]
year: 2026
venue: "Research"
url: https://doi.org/10.34133/research.1412
doi: "10.34133/research.1412"
arxiv: null
cite: "Wu, B., Xiao, R., & Zhao, J. (2026). Primate-Inspired Cooperation Emergence and Strategy Generation in Heterogeneous Robot Swarm. Research, 9, 1412. https://doi.org/10.34133/research.1412"
topics: [swarm-robotics, swarm-intelligence]
added_by: dmarz/swarm-robotics-recent-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "0 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex search budget exhausted during this audit)"
code: []
---

## Summary

The authors propose Cooperation Emergence and Strategy Generation (CE&SG), an architecture in which a heterogeneous robot swarm synthesises composite cooperative strategies on the fly. It is inspired by fission-fusion cooperation in primate groups and implemented with a hyper-heuristic that weights base strategies (the "PIHH" algorithm). On a proof-of-concept air-defence-suppression task, it beats several existing methods, scales to 250 robots and 1,500 tasks in discrete-event simulation under disruptions, and is checked for physical feasibility with 5 UAVs in AirSim.

## Contribution

A task-allocation architecture where strategy, not just assignment, emerges from self-organised interaction. The authors compare it explicitly with Self-organizing Nervous Systems ([[zhu-2024-self]]) and present the two as complementary: SoNS supplies communication topology, CE&SG supplies decision strategy.

## Key results

- (abstract) Outperforms several advanced baselines on the air-defence-suppression task.
- (abstract) Scalability and fault tolerance tested at up to 250 robots and 1,500 tasks with multiple disruptive disturbances in discrete-event simulation.
- (comparison table read in the full text) Physical validation is a high-fidelity AirSim simulation with 5 UAVs, not real robots, unlike SoNS's 8 real heterogeneous robots.

## Methods and models

Hyper-heuristic with attention-like strategy weights trained by multiscale evolutionary training; fission-fusion subgroup partitioning. Read: abstract plus the SoNS comparison and limitations passages.

## Limitations and open questions

Authors: the biological mapping rests on interpreted behaviour patterns, not quantitative primate field data. I add: military task framing, no hardware experiments, and "emergence" is claimed for a trained hyper-heuristic.

## Relevance to us

Low to moderate. One of few recent heterogeneous-swarm task-allocation papers; a foil for [[zhu-2024-self]].
