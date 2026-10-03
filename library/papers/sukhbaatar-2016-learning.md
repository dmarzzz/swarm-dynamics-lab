---
id: sukhbaatar-2016-learning
type: paper
title: Learning Multiagent Communication with Backpropagation
authors:
- Sainbayar Sukhbaatar
- Arthur Szlam
- Rob Fergus
year: 2016
venue: Advances in Neural Information Processing Systems 29 (NIPS 2016)
url: https://arxiv.org/abs/1605.07736
doi: null
arxiv: '1605.07736'
cite: Sukhbaatar, S., Szlam, A., & Fergus, R. (2016). Learning multiagent communication with backpropagation. In Advances in Neural Information Processing Systems 29 (NIPS 2016). arXiv:1605.07736.
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

CommNet lets fully cooperative agents exchange continuous vectors that are learned jointly with their policies: each agent's hidden state is updated with the mean of the other agents' communication vectors over several rounds. On a range of cooperative tasks the communicating agents outperform non-communicating ones, and in some cases the learned protocol is interpretable.

## Contribution

The mean-pooled continuous communication layer is a direct ancestor of the permutation-invariant encoders used for swarms ([[huttenrauch-2019-deep]]) and of graph-network controllers ([[tolstaya-2020-learning]]).

## Key results

- Improved performance over non-communicative agents and baselines on traffic-junction, combat and similar tasks (claimed in the abstract).

## Methods and models

Multi-round communication where each agent receives the average of others' hidden vectors; trained by backpropagation (supervised or policy gradient). Abstract-level read.

## Limitations and open questions

Broadcast averaging assumes all-to-all or masked communication and identical agents; no analysis of scaling to large swarms.

## Relevance to us

Mean-field style message passing is the simplest learned interaction rule; useful as a learned-communication baseline. See [[foerster-2016-learning]], [[yang-2018-mean]].
