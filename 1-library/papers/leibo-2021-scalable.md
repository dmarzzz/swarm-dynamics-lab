---
id: leibo-2021-scalable
type: paper
title: Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot
authors:
- Joel Z. Leibo
- Edgar Duéñez-Guzmán
- Alexander Sasha Vezhnevets
- John P. Agapiou
- Peter Sunehag
- Raphael Koster
- Jayd Matyas
- Charles Beattie
- Igor Mordatch
- Thore Graepel
year: 2021
venue: Proceedings of the 38th International Conference on Machine Learning (ICML), PMLR 139
url: https://arxiv.org/abs/2107.06857
doi: null
arxiv: '2107.06857'
cite: Leibo, J. Z., Duéñez-Guzmán, E., Vezhnevets, A. S., Agapiou, J. P., Sunehag, P., Koster, R., Matyas, J., Beattie, C., Mordatch, I., & Graepel, T. (2021). Scalable evaluation of multi-agent reinforcement learning with Melting Pot. In Proceedings of the 38th International Conference on Machine Learning, PMLR 139, 6187–6199.
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 158 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Melting Pot is a MARL evaluation suite whose primary objective is generalisation to novel social situations. It exploits the fact that other agents form part of an agent's environment: test scenarios are built by placing trained "background" populations alongside the focal agents. The initial release has over 80 test scenarios spanning social dilemmas, reciprocity, resource sharing and task partitioning, and reveals weaknesses of standard MARL algorithms not visible in training performance.

## Contribution

The standard benchmark for social generalisation in mixed-motive MARL (seed in the task brief); successor of the sequential social dilemmas of [[leibo-2017-multi]].

## Key results

- Standard MARL training algorithms show generalisation failures on held-out scenarios (claimed in abstract).

## Methods and models

DeepMind Lab2D substrates, focal-population evaluation against background bots. Abstract-level read. Code is public (Melting Pot repository; URL not opened in this session).

## Limitations and open questions

Focus on small-group social behaviour (up to ~16 players), not large swarms or physics-based motion.

## Relevance to us

Useful if a team studies cooperation or division of labour rather than motion; less so for flocking. Related: [[jaques-2019-social]], [[leibo-2019-autocurricula]].
