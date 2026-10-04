---
id: mi-2026-unveiling
type: paper
title: Unveiling Complex Collective Behaviors from Simple Rewards
authors:
- Yize Mi
- Jianan Li
- Liang Li
- Shiyu Zhao
year: 2026
venue: arXiv preprint (accepted at IROS 2026)
url: https://arxiv.org/abs/2607.12861
doi: null
arxiv: '2607.12861'
cite: Mi, Y., Li, J., Li, L., & Zhao, S. (2026). Unveiling complex collective behaviors from simple rewards. arXiv preprint arXiv:2607.12861 (accepted at IROS 2026).
topics:
- marl-emergence
- swarm-robotics
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

MARL swarm policies trained on simple rewards produce complex collective behaviour, but neural policies are opaque. The authors propose an explanatory framework built around an Agent Response Map that shows where in space agents are attracted or repelled. It reveals that robots implicitly learn geometric fields of the environment and use them as targets for coordinated motion, validated on cooperative shape assembly and competitive predator-prey pursuit-evasion.

## Contribution

Interpretability tooling for learned swarm policies, from the same group as [[li-2023-predator]]; addresses the black-box objection to MARL as a model of collective behaviour.

## Key results

- In shape assembly, the unoccupied target interior is identified as the navigation target and shifts as it fills (claimed in abstract).
- Similar field-following explanation in predator-prey (claimed).

## Methods and models

Agent Response Map probing of trained MARL policies across positions. Abstract-level read.

## Limitations and open questions

Very recent preprint; generality of the response-map explanation beyond two tasks unknown.

## Relevance to us

Directly useful for analysing any learned swarm policy we train (map the response field, compare to Couzin-style zones). Related: [[brambati-2025-learning]], [[couzin-2002-collective]].
