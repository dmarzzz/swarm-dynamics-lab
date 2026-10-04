---
id: zheng-2018-magent
type: paper
title: 'MAgent: A Many-Agent Reinforcement Learning Platform for Artificial Collective Intelligence'
authors:
- Lianmin Zheng
- Jiacheng Yang
- Han Cai
- Ming Zhou
- Weinan Zhang
- Jun Wang
- Yong Yu
year: 2018
venue: Proceedings of the AAAI Conference on Artificial Intelligence
url: https://arxiv.org/abs/1712.00600
doi: 10.1609/aaai.v32i1.11371
arxiv: '1712.00600'
cite: 'Zheng, L., Yang, J., Cai, H., Zhou, M., Zhang, W., Wang, J., & Yu, Y. (2018). MAgent: A many-agent reinforcement learning platform for artificial collective intelligence. Proceedings of the AAAI Conference on Artificial Intelligence, 32(1). https://doi.org/10.1609/aaai.v32i1.11371'
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 252 (Semantic Scholar, 2026-10-03); 97 (Crossref, 2026-10-03)
code: []
---

## Summary

MAgent is a gridworld platform for many-agent RL that targets hundreds to millions of agents, hosting up to one million agents on a single GPU server. Beyond algorithms, it is meant for observing individual behaviours and social phenomena emerging in AI societies, such as communication, leadership and altruism. The demo presents three environments (including pursuit and battle) where collective intelligence emerges from learning from scratch.

## Contribution

The main scalable environment for large-population MARL, used for the battle experiments in [[yang-2018-mean]].

## Key results

- Scales to one million agents on one GPU server (claimed in abstract).

## Methods and models

Grid world with configurable agent types, observation as multi-channel local views, DQN/A2C baselines. Abstract-level read; arXiv lists six authors, the AAAI record seven (Ming Zhou added), cite follows AAAI.

## Limitations and open questions

Gridworld physics; discrete actions. Now maintained elsewhere (PettingZoo/MAgent2, not checked).

## Relevance to us

Ready-made environment for large-N learned collective behaviour at the hackathon. Related: [[yang-2018-mean]], [[huttenrauch-2019-deep]].
