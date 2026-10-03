---
id: heuthe-2024-counterfactual
type: paper
title: Counterfactual rewards promote collective transport using individually controlled swarm microrobots
authors:
- Veit-Lorenz Heuthe
- Emanuele Panizon
- Hongri Gu
- Clemens Bechinger
year: 2024
venue: Science Robotics
url: https://arxiv.org/abs/2407.20041
doi: 10.1126/scirobotics.ado5888
arxiv: '2407.20041'
cite: Heuthe, V.-L., Panizon, E., Gu, H., & Bechinger, C. (2024). Counterfactual rewards promote collective transport using individually controlled swarm microrobots. Science Robotics, 9(97), eado5888.
topics:
- marl-emergence
- swarm-robotics
- active-matter
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 51 (Crossref, 2026-10-03); 51 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Up to 200 light-driven microrobots, each individually steered by a laser spot, learn with MARL to transport a large cargo to an arbitrary position and orientation, like ants carrying an object. Counterfactual rewards assign credit to individual microrobots, making training fast and unbiased despite thermal noise, many degrees of freedom, physical coupling between robots and collisions. The learned strategy is robust to group size, malfunctioning units and environmental noise.

## Contribution

The strongest experimental demonstration in this set of MARL producing a collective function in a physical swarm at scale (hundreds of agents), using difference-reward credit assignment in the spirit of [[foerster-2018-counterfactual]].

## Key results

- Collective cargo transport to arbitrary pose with up to 200 microrobots (measured, experiment, per abstract).
- Robust to changes in group size, faulty units and noise (claimed).

## Methods and models

Light-activated microrobots individually addressed by laser spots; MARL with counterfactual (difference) rewards. Abstract-level read.

## Limitations and open questions

Abstract-level read; training-in-simulation versus on-hardware split not checked.

## Relevance to us

Benchmark-quality evidence that per-agent credit assignment is the key to learning in large physical swarms. Related: [[loffler-2023-collective]], [[foerster-2018-counterfactual]], [[cai-2025-reinforcement]], [[casert-2024-learning]], [[ben-zion-2023-morphological]].
