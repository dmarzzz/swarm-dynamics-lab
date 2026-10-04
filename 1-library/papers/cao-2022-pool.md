---
id: cao-2022-pool
type: paper
title: 'PooL: Pheromone-inspired Communication Framework for Large Scale Multi-Agent Reinforcement Learning'
authors:
- Zixuan Cao
- Mengzhi Shi
- Zhanbo Zhao
- Xiujun Ma
year: 2022
venue: arXiv preprint
url: https://arxiv.org/abs/2202.09722
doi: null
arxiv: '2202.09722'
cite: 'Cao, Z., Shi, M., Zhao, Z., & Ma, X. (2022). PooL: Pheromone-inspired communication framework for large scale multi-agent reinforcement learning. arXiv preprint arXiv:2202.09722.'
topics:
- marl-emergence
- swarm-intelligence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

To scale MARL to large populations, PooL lets agents release "pheromones" defined as outputs of their RL networks, which summarise their view of the environment; a pheromone update mechanism aggregates these into low-dimensional local summaries that nearby agents perceive. Implemented on Q-learning and evaluated in large-scale cooperative environments, it is reported to improve coordination.

## Contribution

Indirect, field-mediated communication as a scaling device for MARL, similar in purpose to the mean action of [[yang-2018-mean]].

## Key results

- Agents capture effective information and coordinate better in large-scale cooperative tasks (claimed; abstract truncated).

## Methods and models

Q-learning base, pheromone field update and perception. Abstract-level read.

## Limitations and open questions

Preprint; benchmarks and baselines not checked.

## Relevance to us

Minor; listed for completeness of the stigmergic-MARL thread. Related: [[shaw-2020-formic]], [[pitteri-2026-ant]].
