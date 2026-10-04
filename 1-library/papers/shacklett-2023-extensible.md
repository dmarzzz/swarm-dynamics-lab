---
id: shacklett-2023-extensible
type: paper
title: "An Extensible, Data-Oriented Architecture for High-Performance, Many-World Simulation"
authors: [Brennan Shacklett, Luc Guy Rosenzweig, Zhiqiang Xie, Bidipta Sarkar, Andrew Szot, Erik Wijmans, Vladlen Koltun, Dhruv Batra, Kayvon Fatahalian]
year: 2023
venue: ACM Transactions on Graphics 42(4) (SIGGRAPH 2023)
url: https://madrona-engine.github.io/shacklett_siggraph23.pdf
doi: 10.1145/3592427
arxiv: null
cite: "Shacklett, B., Rosenzweig, L. G., Xie, Z., Sarkar, B., Szot, A., Wijmans, E., Koltun, V., Batra, D., & Fatahalian, K. (2023). An extensible, data-oriented architecture for high-performance, many-world simulation. ACM Transactions on Graphics, 42(4). https://doi.org/10.1145/3592427"
topics: [marl-emergence, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: [gh-shacklettbp-madrona]
---

## Summary

Argues that the entity-component-system (ECS) pattern used for CPU game logic also gives the structure needed for GPU batch simulation, and contributes the first fully GPU-accelerated ECS that natively steps many independent environments at once. Several learning environments built in the framework show two to three orders of magnitude speedup over open-source CPU baselines and 5-33x over strong 32-thread CPU baselines; a port of OpenAI's hide-and-seek 3D environment with rigid-body physics and ray tracing reaches over 1.9 million environment steps per second on one GPU.

## Contribution

A general authoring framework for batch simulators, rather than one fast environment; it is the engine under [[gh-emerge-lab-gpudrive]] and GPU ports of Overcooked, Hanabi and hide-and-seek ([[baker-2020-emergent]]).

## Key results

- 1.9M+ env steps/s for hide-and-seek on a single GPU (abstract).
- 5-33x over 32-thread CPU baselines; 100-1000x over open-source CPU baselines (abstract).

## Methods and models

GPU ECS with per-world entity tables, amortised work across worlds, coherent parallel execution of systems across environments; XPBD physics; batch renderer.

## Limitations and open questions

Read at abstract and introduction level.

## Relevance to us

Lesson for any custom swarm sim: lay out state as flat per-component arrays across all worlds and agents (data-oriented design); this is what makes both GPU batching and variable agent counts cheap.
