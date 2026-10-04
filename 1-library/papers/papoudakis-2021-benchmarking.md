---
id: papoudakis-2021-benchmarking
type: paper
title: "Benchmarking Multi-Agent Deep Reinforcement Learning Algorithms in Cooperative Tasks"
authors: [Georgios Papoudakis, Filippos Christianos, Lukas Schäfer, Stefano V. Albrecht]
year: 2021
venue: Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks (NeurIPS 2021)
url: https://arxiv.org/abs/2006.07869
doi: null
arxiv: '2006.07869'
cite: "Papoudakis, G., Christianos, F., Schäfer, L., & Albrecht, S. V. (2021). Benchmarking multi-agent deep reinforcement learning algorithms in cooperative tasks. In Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks 1 (NeurIPS 2021). arXiv:2006.07869."
topics: [marl-emergence, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: [gh-semitable-lb-foraging, gh-semitable-robotic-warehouse]
---

## Summary

Systematically compares nine MARL algorithms from three families (independent learning, centralised multi-agent policy gradient, value decomposition) across a diverse set of cooperative tasks (matrix games, MPE, SMAC, and two new environments) to give reference performance and practical guidance. Releases EPyMARL, an extension of PyMARL [[gh-oxwhirl-pymarl]] with more algorithms and configurable implementation details such as parameter sharing, and two new sparse-reward coordination environments, Level-Based Foraging and the Multi-Robot Warehouse.

## Contribution

One of the first cross-environment MARL benchmark studies; source paper for LBF [[gh-semitable-lb-foraging]] and RWARE [[gh-semitable-robotic-warehouse]].

## Key results

- Nine algorithms evaluated on 25 cooperative tasks spanning partial/full observability, sparse/dense rewards and 2-10 agents (conclusion).
- Reports maximum and average returns and identifies which environment types favour independent learning, centralised training or value decomposition (per-task numbers not transcribed here).

## Methods and models

EPyMARL implementations of IQL, IA2C, IPPO, MADDPG, COMA, MAA2C, MAPPO, VDN and QMIX (Table 1).

## Limitations and open questions

Cooperative environments and commonly used algorithms only; the authors list competitive settings, exploration, communication and opponent modelling as future work. Skimmed (abstract, algorithm table, conclusion).

## Relevance to us

Explains why LBF and RWARE exist (sparse-reward coordination) and supplies EPyMARL as a training harness for small envs.
