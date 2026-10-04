---
id: rashid-2018-qmix
type: paper
title: 'QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning'
authors:
- Tabish Rashid
- Mikayel Samvelyan
- Christian Schroeder de Witt
- Gregory Farquhar
- Jakob Foerster
- Shimon Whiteson
year: 2018
venue: Proceedings of the 35th International Conference on Machine Learning (ICML), PMLR 80
url: https://arxiv.org/abs/1803.11485
doi: null
arxiv: '1803.11485'
cite: 'Rashid, T., Samvelyan, M., Schroeder de Witt, C., Farquhar, G., Foerster, J., & Whiteson, S. (2018). QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning. In Proceedings of the 35th International Conference on Machine Learning, PMLR 80, 4295–4304.'
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 2198 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

QMIX trains decentralised policies centrally by estimating the joint action-value as a non-linear mixing of per-agent utilities that each condition only on local observations. A mixing network conditioned on global state enforces that the joint value is monotonic in each per-agent value, so the joint argmax decomposes into per-agent argmaxes, keeping centralised and decentralised policies consistent. It significantly outperforms prior value-based MARL on StarCraft II micromanagement.

## Contribution

The dominant value-factorisation method for cooperative MARL and the default baseline on SMAC ([[samvelyan-2019-starcraft]]).

## Key results

- Outperforms IQL and VDN on StarCraft II micromanagement maps (claimed in abstract).

## Methods and models

Per-agent recurrent Q-networks, monotonic hypernetwork mixer, centralised TD training. Abstract-level read.

## Limitations and open questions

Monotonicity limits representable coordination; fixed agent count.

## Relevance to us

Baseline for cooperative swarm tasks with team rewards. Related: [[foerster-2018-counterfactual]], [[oroojlooy-2023-review]].
