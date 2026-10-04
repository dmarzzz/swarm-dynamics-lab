---
id: shtossel-2026-modular
type: paper
title: "Modular Reinforcement Learning For Cooperative Swarms"
authors: ["Erel Shtossel", "Gal A. Kaminka"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2605.04939
doi: null
arxiv: "2605.04939"
cite: "Shtossel, E., & Kaminka, G. A. (2026). Modular Reinforcement Learning For Cooperative Swarms. arXiv preprint arXiv:2605.04939."
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (OpenAlex W7160550197, 2026-10-03)"
code: []
---

## Summary

In cooperative swarms of computationally limited robots, independent distributed MARL can align individual learning with the collective goal, but representing all spatial interaction states is combinatorial and overwhelms robot memory. The authors decompose the state: each feature gets its own learning procedure and the results are aggregated. Simulated foraging swarms show the approach is effective.

## Contribution

A memory-scalable state representation for independent swarm RL, continuing Kaminka's line on collision-aware distributed learning.

## Key results

- Effective learning in numerous simulated foraging experiments (per the abstract; no numbers there).

## Methods and models

Decomposed (modular) state representation: a separate learning procedure per state feature, with results aggregated for action selection; simulated foraging swarms. The underlying RL algorithm is not stated in the abstract.

## Limitations and open questions

Abstract-depth entry. Simulation only; foraging task only.

## Relevance to us

Relevant for learning on very constrained robots; compare [[sebastian-2025-physics]] and [[wang-2025-local]].
