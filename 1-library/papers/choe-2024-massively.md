---
id: choe-2024-massively
type: paper
title: "Massively Multiagent Minigames for Training Generalist Agents"
authors: ["Kyoung Whan Choe", "Ryan Sullivan", "Joseph Suárez"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2406.05071
doi: null
arxiv: '2406.05071'
cite: "Choe, K. W., Sullivan, R., & Suárez, J. (2024). Massively multiagent minigames for training generalist agents. arXiv:2406.05071."
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: [gh-kywch-meta-mmo, gh-neuralmmo-environment]
---

## Summary

Introduces Meta MMO, a set of computationally cheap many-agent minigames (team battle, protect the king, race to the center, king of the hill, sandwich) built on Neural MMO 2, and studies whether one set of weights can play several minigames. Environment, baselines and training code released under MIT.

## Contribution

Turns Neural MMO into a multi-task, many-agent generalisation benchmark with short configurable games.

## Key results

- Abstract gives no numbers; README shows a generalist trained for 400M timesteps across five minigames and Elo-based evaluation.

## Methods and models

Built on Neural MMO 2.1 and its baselines; PufferLib-style PPO training (repo).

## Limitations and open questions

Abstract only. Repo last pushed 2024-08; tied to Neural MMO 2.x.

## Relevance to us

Borrow idea: short, configurable minigames on a shared many-agent engine are cheaper experiment units than full open worlds. Builds on [[suarez-2023-neural]].
