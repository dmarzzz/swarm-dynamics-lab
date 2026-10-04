---
id: bektas-2025-emergent
type: paper
title: "Emergent interactions lead to collective frustration in robotic matter"
authors: ["Onurcan Bektas", "Adolfo Alsina", "Steffen Rulands"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2507.22148
doi: null
arxiv: "2507.22148"
cite: "Bektas, O., Alsina, A., & Rulands, S. (2025). Emergent interactions lead to collective frustration in robotic matter. arXiv preprint arXiv:2507.22148."
topics: ["active-matter", "marl-emergence", "swarm-robotics"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "0 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Bektas, Alsina and Rulands study "robotic matter": stochastic interacting particles in 1D, each with a deep neural
network that learns its transitions from its environment. The collective self-organizes into distinct temporal learning
regimes, emergent particle species and long-lived frustrated states with suboptimal reward, and shows an abrupt,
density-dependent change in behaviour that active-matter theory reads as a phase transition with criticality
signatures. Read from the abstract on the page in `url`; details beyond the abstract are not checked.

## Contribution

Brings the active-matter phase-transition lens to collectives of learning agents, linking this topic to MARL.

## Key results

- Emergent frustration and density-dependent transition in learning-agent collectives (abstract; simulation).

## Methods and models

Interacting particle system with per-agent deep RL. arXiv:2507.22148; full text not read.

## Limitations and open questions

1D toy model; preprint.

## Relevance to us

Direct bridge to LLM/RL agent swarms: learning agents can get collectively stuck in frustrated states, a failure mode
worth testing. Related: [[casert-2024-learning]], [[cichos-2020-machine]], [[brambati-2025-learning]].
