---
id: foerster-2016-learning
type: paper
title: Learning to Communicate with Deep Multi-Agent Reinforcement Learning
authors:
- Jakob N. Foerster
- Yannis M. Assael
- Nando de Freitas
- Shimon Whiteson
year: 2016
venue: Advances in Neural Information Processing Systems 29 (NIPS 2016)
url: https://arxiv.org/abs/1605.06676
doi: null
arxiv: '1605.06676'
cite: Foerster, J. N., Assael, Y. M., de Freitas, N., & Whiteson, S. (2016). Learning to communicate with deep multi-agent reinforcement learning. In Advances in Neural Information Processing Systems 29 (NIPS 2016). arXiv:1605.06676.
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1055 for the arXiv record (OpenAlex, 2026-10-03)
code: []
---

## Summary

Cooperative agents with partial observability must invent a communication protocol to maximise shared utility. Two methods are proposed: RIAL, where each agent uses deep Q-learning and treats messages as actions, and DIAL, which during centralised training backpropagates gradients through a noisy, differentiable communication channel and discretises messages at execution. The abstract reports end-to-end learned protocols on communication riddles and multi-agent vision tasks.

## Contribution

With [[sukhbaatar-2016-learning]] it opened deep learned communication in MARL, and it introduced the centralised-learning, decentralised-execution framing later used by [[lowe-2017-multi]] and [[foerster-2018-counterfactual]].

## Key results

- DIAL learns protocols that solve switch-riddle and MNIST-based communication games where RIAL is slower (claimed in the abstract; numbers not read).

## Methods and models

Deep recurrent Q-networks with parameter sharing; DIAL's discretise-regularise unit adds noise to real-valued messages during training. Abstract-level read.

## Limitations and open questions

Small numbers of agents and toy tasks; message semantics are task-specific.

## Relevance to us

Communication bandwidth and protocol learning are a lever in swarm coordination; this is the canonical citation. See [[zhu-2024-survey]], [[lazaridou-2020-emergent]].
