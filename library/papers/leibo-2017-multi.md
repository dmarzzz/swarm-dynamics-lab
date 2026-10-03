---
id: leibo-2017-multi
type: paper
title: Multi-agent Reinforcement Learning in Sequential Social Dilemmas
authors:
- Joel Z. Leibo
- Vinicius Zambaldi
- Marc Lanctot
- Janusz Marecki
- Thore Graepel
year: 2017
venue: Proceedings of the 16th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2017)
url: https://arxiv.org/abs/1702.03037
doi: null
arxiv: '1702.03037'
cite: Leibo, J. Z., Zambaldi, V., Lanctot, M., Marecki, J., & Graepel, T. (2017). Multi-agent reinforcement learning in sequential social dilemmas. In Proceedings of the 16th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2017). arXiv:1702.03037.
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 741 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Matrix-game social dilemmas treat cooperate or defect as atomic actions, but real dilemmas are temporally extended. The authors define sequential social dilemmas, Markov games with the incentive structure of matrix dilemmas, and study independent deep Q-learners in two of them: Gathering (fruit collection with the option to tag rivals) and Wolfpack (cooperative hunting). Learned behaviour shifts with environmental factors such as resource abundance, and conflict emerges from competition over scarce resources.

## Contribution

Started the DeepMind line on emergent cooperation and conflict among self-interested learners, continued in [[jaques-2019-social]], [[leibo-2019-autocurricula]] and [[leibo-2021-scalable]].

## Key results

- Aggressiveness in Gathering increases as resources become scarce (claimed in abstract).
- Cooperation in Wolfpack depends on environment parameters (claimed).

## Methods and models

Independent DQN agents in 2D gridworld Markov games; empirical game-theoretic analysis of learned policies. Abstract-level read.

## Limitations and open questions

Two agents per game; independent learners only.

## Relevance to us

Environmental control parameters (resource density) shifting emergent collective behaviour is the MARL analogue of a phase diagram. Related: [[lopez-incera-2020-development]], [[yamaguchi-2025-emergent]].
