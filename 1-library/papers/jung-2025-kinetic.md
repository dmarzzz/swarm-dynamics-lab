---
id: jung-2025-kinetic
type: paper
title: Kinetic Theory of Decentralized Learning for Smart Active Matter
authors:
- Gerhard Jung
- Misaki Ozawa
- Eric Bertin
year: 2025
venue: Physical Review Letters
url: https://arxiv.org/abs/2501.03948
doi: 10.1103/5m44-kwhv
arxiv: '2501.03948'
cite: Jung, G., Ozawa, M., & Bertin, E. (2025). Kinetic theory of decentralized learning for smart active matter. Physical Review Letters, 134(24), 248302.
topics:
- marl-emergence
- active-matter
- swarm-robotics
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 5 (Crossref, 2026-10-03); 7 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Agents of "smart" active matter learn in a decentralised way by locally exchanging policies to maximise a reward. The authors build a kinetic theory of this learning process and derive explicit hydrodynamic equations for the policy dynamics, applied to two microscopic models (policies as fixed parameters, akin to evolutionary dynamics, and state-dependent robotic controllers), with good agreement against agent-based simulations. They derive control parameters and uncertainty relations as a basis for statistical-physics analysis of decentralised learning.

## Contribution

First coarse-grained (hydrodynamic) theory of the learning dynamics of a swarm rather than of its motion; theoretical companion to the simulations of [[durve-2020-learning]] and [[brambati-2025-learning]], and to the learning-phase view of [[yamaguchi-2025-emergent]].

## Key results

- Hydrodynamic equations for policy fields match agent-based simulations for two models (claimed in abstract).

## Methods and models

Kinetic theory (Boltzmann-like) of policy exchange among self-propelled agents. Abstract-level read.

## Limitations and open questions

Policy exchange (social learning) rather than gradient-based RL; abstract-level read.

## Relevance to us

Gives the continuum equations to compare a learned-swarm experiment against. Related: [[yang-2018-mean]], [[lauriere-2022-learning]].
