---
id: richmond-2023-flame
type: paper
title: "FLAME GPU 2: A framework for flexible and performant agent based simulation on GPUs"
authors: ["Paul Richmond", "Robert Chisholm", "Peter Heywood", "Mozhgan Kabiri Chimeh", "Matthew Leach"]
year: 2023
venue: "Software: Practice and Experience"
url: https://eprints.whiterose.ac.uk/id/eprint/199416/
doi: 10.1002/spe.3207
arxiv: null
cite: "Richmond, P., Chisholm, R., Heywood, P., Chimeh, M. K., & Leach, M. (2023). FLAME GPU 2: A framework for flexible and performant agent based simulation on GPUs. Software: Practice and Experience, 53(8), 1659-1680."
topics: [meta, collective-motion]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "17 (Crossref, 2026-10-03)"
code: [gh-flamegpu-flamegpu2]
---

## Summary

Describes the design of FLAME GPU 2, a general-purpose GPU ABM framework that separates model description from CUDA implementation, and four methods for keeping it fast: minimising host-device data movement with run-time compiled agent functions, ensembles of simulations sharing one GPU, concurrent execution of independent agent functions within a step, and hierarchical sub-models for conflict resolution. Benchmarks use a continuous-space particle (Boids-like) model and a Sugarscape implementation following NetLogo's.

## Contribution

Shows that a flexible, general GPU ABM API need not give up the performance of hand-written GPU simulations, and that small models need ensembles or intra-model concurrency to use a modern GPU at all.

## Key results

- Continuous-space benchmark: 1M agents at about 0.003 s per step with spatial messaging and run-time compilation.
- Sugarscape with sub-modelling: environment of 16M agents at about 1 s per step.
- Ensembles raise device utilisation by up to 8x (most effective for small populations with less dense communication); concurrent execution of non-interacting species gives up to about 14x (e.g. 2,048 agents with 25 species). The abstract states speedups of 3.5x and 10x over a baseline GPU implementation for ensembles and concurrency respectively.
- Spatial messaging beats brute-force messaging until roughly half of all messages fall inside each agent's radius.
- Run-time compilation costs about one second on first execution.

## Methods and models

CUDA C++ library with Python bindings; message specialisations (brute force, spatial 2D/3D, array, bucket); benchmark GPU models not recorded in my skim (the discussion cites a Volta GV100 needing up to 160k resident threads for full occupancy).

## Limitations and open questions

Skimmed (abstract, design and messaging sections, ensemble and concurrency results, conclusion). Comparisons are to their own GPU baseline, not to CPU frameworks. Notes that use cases needing millions of agents are rarer than small populations.

## Relevance to us

Defines what GPU ABM can do at the top end and gives the message-specialisation design worth copying for adversarial-message experiments. Compare CPU throughputs measured in this scan ([[gh-krabmaga-krabmaga]], [[gh-jofmi-agentpy]], [[gh-mesa-mesa]]).
