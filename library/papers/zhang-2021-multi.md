---
id: zhang-2021-multi
type: paper
title: 'Multi-Agent Reinforcement Learning: A Selective Overview of Theories and Algorithms'
authors:
- Kaiqing Zhang
- Zhuoran Yang
- Tamer Başar
year: 2021
venue: Handbook of Reinforcement Learning and Control (Springer, Studies in Systems, Decision and Control)
url: https://arxiv.org/abs/1911.10635
doi: 10.1007/978-3-030-60990-0_12
arxiv: '1911.10635'
cite: 'Zhang, K., Yang, Z., & Başar, T. (2021). Multi-agent reinforcement learning: A selective overview of theories and algorithms. In Handbook of Reinforcement Learning and Control (Studies in Systems, Decision and Control), pp. 321–384. Springer.'
topics:
- marl-emergence
- sync-consensus
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1783 (Semantic Scholar, 2026-10-03); 982 (Crossref, 2026-10-03)
code: []
---

## Summary

A theory-focused review of MARL covering algorithms with convergence or sample-complexity guarantees within Markov (stochastic) games and extensive-form games, organised by cooperative, competitive and mixed tasks. It highlights angles missing from earlier surveys: learning in extensive-form games, decentralised MARL with networked agents (consensus-based actor-critic), MARL in the mean-field regime, and (non-)convergence of policy-gradient methods in games.

## Contribution

The main bridge between control-theory consensus methods (networked agents) and MARL, and a theory complement to empirical surveys like [[gronauer-2022-multi]].

## Key results

- Review; synthesis of convergence results (per abstract).

## Methods and models

Literature survey. Abstract-level read.

## Limitations and open questions

Selective by design; emergent behaviour and swarm applications are peripheral.

## Relevance to us

Read the networked-agents and mean-field sections before building theory around a learned swarm. Related: [[yang-2018-mean]], [[lauriere-2022-learning]], [[olfati-saber-2004-consensus]].
