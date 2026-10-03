---
id: jaques-2019-social
type: paper
title: Social Influence as Intrinsic Motivation for Multi-Agent Deep Reinforcement Learning
authors:
- Natasha Jaques
- Angeliki Lazaridou
- Edward Hughes
- Caglar Gulcehre
- Pedro A. Ortega
- DJ Strouse
- Joel Z. Leibo
- Nando de Freitas
year: 2019
venue: Proceedings of the 36th International Conference on Machine Learning (ICML), PMLR 97
url: https://arxiv.org/abs/1810.08647
doi: null
arxiv: '1810.08647'
cite: Jaques, N., Lazaridou, A., Hughes, E., Gulcehre, C., Ortega, P. A., Strouse, D. J., Leibo, J. Z., & de Freitas, N. (2019). Social influence as intrinsic motivation for multi-agent deep reinforcement learning. In Proceedings of the 36th International Conference on Machine Learning, PMLR 97, 3040–3049.
topics:
- marl-emergence
- criticality-measurement
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Agents receive an intrinsic reward for causal influence over other agents' actions, assessed counterfactually: each agent simulates alternative actions and measures how much others' behaviour would change. This equals rewarding mutual information between agents' actions. Influence rewards improve coordination and communication in sequential social dilemmas, speed learning, give more meaningful learned communication, and can be computed decentrally by learning models of other agents.

## Contribution

Ties an information-theoretic coupling measure (action mutual information) to emergent coordination, linking MARL to information-flow measures used for animal collectives.

## Key results

- Enhanced coordination and communication and much faster learning in social dilemma environments (claimed in abstract).

## Methods and models

Counterfactual influence reward, models of other agents, A3C-style agents. Abstract-level read.

## Limitations and open questions

Influence is not always prosocial; small groups.

## Relevance to us

Information-theoretic coupling between agents is a measurable quantity in learned swarms; see the criticality-measurement topic. Related: [[leibo-2017-multi]], [[leibo-2021-scalable]].
