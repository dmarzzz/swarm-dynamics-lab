---
id: shaw-2020-formic
type: paper
title: 'ForMIC: Foraging via Multiagent RL with Implicit Communication'
authors:
- Samuel Shaw
- Emerson Wenzel
- Alexis Walker
- Guillaume Sartoretti
year: 2020
venue: arXiv preprint
url: https://arxiv.org/abs/2006.08152
doi: null
arxiv: '2006.08152'
cite: 'Shaw, S., Wenzel, E., Walker, A., & Sartoretti, G. (2020). ForMIC: Foraging via multiagent RL with implicit communication. arXiv preprint arXiv:2006.08152.'
topics:
- marl-emergence
- swarm-intelligence
- swarm-robotics
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

ForMIC is a distributed RL approach to multi-agent foraging in which agents communicate implicitly through pheromone-like marks in the shared environment. Learning stigmergic policies has a circular dependency (agents must act well to emit useful signals and read signals to act well); the authors stabilise training with curriculum learning, action filtering and non-learning agents that raise density cheaply. The learned policy outperforms state-of-the-art foraging algorithms across team sizes and resource layouts.

## Contribution

Learned stigmergy, the RL counterpart of ant-colony-style coordination studied in swarm intelligence.

## Key results

- Outperforms existing multi-agent foraging algorithms across team sizes and resource placements (claimed in abstract).

## Methods and models

Distributed RL with environment marking actions; curriculum, action filtering, filler agents. Abstract-level read.

## Limitations and open questions

Preprint (IEEE copyright notice, venue not stated on the arXiv page); simulation only.

## Relevance to us

Stigmergy as learned communication; compare explicit message learning ([[foerster-2016-learning]]). Related: [[cao-2022-pool]], [[pitteri-2026-ant]].
