---
id: zhu-2024-self
type: paper
title: "Self-organizing nervous systems for robot swarms"
authors: ["Weixu Zhu", "Sinan Oğuz", "Mary Katherine Heinrich", "Michael Allwright", "Mostafa Wahby", "Anders Lyhne Christensen", "Emanuele Garone", "Marco Dorigo"]
year: 2024
venue: "Science Robotics"
url: https://arxiv.org/pdf/2401.13103
doi: "10.1126/scirobotics.adl5161"
arxiv: "2401.13103"
cite: "Zhu, W., Oğuz, S., Heinrich, M. K., Allwright, M., Wahby, M., Christensen, A. L., Garone, E., & Dorigo, M. (2024). Self-organizing nervous systems for robot swarms. Science Robotics, 9(96), eadl5161."
topics: [swarm-robotics, sync-consensus]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "26 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Robot swarm architectures are usually fixed before deployment as either centralised (single point of failure,
limited scale) or fully decentralised (hard to design analytically). The self-organising nervous system (SoNS)
lets robots autonomously establish, maintain and reconfigure dynamic multi-level hierarchies: a swarm of n
independent robots can merge into one n-robot SoNS with a temporary "brain" and later split into smaller SoNSs.
The paper demonstrates this with heterogeneous ground and aerial robots performing missions that combine
centralised-style coordination with swarm-style robustness.

## Contribution

Operationalises the "hierarchical self-organisation" agenda of [[dorigo-2020-reflections]], extending
[[mathews-2017-mergeable]] from physically connected robots to wirelessly linked heterogeneous swarms.

## Key results

- Demonstrations of establishing, reconfiguring and splitting hierarchies with real robots (abstract; numbers
  not checked).

## Methods and models

Heterogeneous ground robots and drones; self-organised hierarchy maintained through local communication; read
the arXiv abstract and the Crossref abstract.

## Limitations and open questions

Scale of experiments and formal guarantees not checked here.

## Relevance to us

A concrete counterpoint to flat swarms; relevant to any project on hierarchy, leadership or information flow in
collectives (collective-decision topic).
