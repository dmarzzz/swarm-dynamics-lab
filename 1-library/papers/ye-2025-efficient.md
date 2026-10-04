---
id: ye-2025-efficient
type: paper
title: "An Efficient Open World Environment for Multi-Agent Social Learning"
authors: ["Eric Ye", "Ren Tao", "Natasha Jaques"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2508.15679
doi: null
arxiv: '2508.15679'
cite: "Ye, E., Tao, R., & Jaques, N. (2025). An efficient open world environment for multi-agent social learning. arXiv:2508.15679."
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "3 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Presents an open-ended multi-agent environment where self-interested agents pursue independent long-horizon goals, with implicit incentives to cooperate (shared enemies, tool building and sharing). Uses it to study social learning from expert agents and emergent collaborative tool use, and whether agents gain from cooperation or competition. A prior lane entry notes the environment is called Multi-Agent Craftax (MAC) and is distinct from [[al-omari-2025-multi]].

## Contribution

A JAX open world built for mixed-motive social learning (learning from experts present in the environment) rather than shared-reward cooperation.

## Key results

- Abstract reports investigations of social learning with experts and implicit cooperation; no headline numbers in the abstract.

## Methods and models

Abstract only. The arXiv HTML references JAX and a recurrent PPO JAX implementation (subho406/Recurrent-PPO-Jax); I found no environment repository link in the paper page.

## Limitations and open questions

No code link located, so not directly bootstrappable. Abstract only.

## Relevance to us

Borrow idea: self-interested agents with independent goals in a Craftax-like world is the mixed-motive variant that [[tessera-2026-benchmarking]] lacks. Skip as a base until code is found.
