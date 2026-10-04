---
id: jiang-2020-graph
type: paper
title: Graph Convolutional Reinforcement Learning
authors: [Jiechuan Jiang, Chen Dun, Tiejun Huang, Zongqing Lu]
year: 2020
venue: International Conference on Learning Representations (ICLR 2020)
url: https://arxiv.org/abs/1810.09202
doi: null
arxiv: '1810.09202'
cite: Jiang, J., Dun, C., Huang, T., & Lu, Z. (2020). Graph convolutional reinforcement learning. In International Conference on Learning Representations (ICLR 2020). arXiv:1810.09202.
topics: [marl-emergence]
added_by: dmarz/marl-emergence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null  # OpenAlex budget exhausted and Semantic Scholar returned 429 on 2026-10-03
code: []
---

## Summary

DGN (deep graph network) treats the agents as nodes of a dynamic proximity graph and applies stacked graph
convolutions with multi-head attention as the kernel ("relation kernels"), so each agent's Q-value draws on
features from progressively larger neighbourhoods. A temporal relation regularisation keeps attention weights
consistent between steps. The authors report that DGN beats DQN, CommNet and MeanField Q baselines on MAgent-style
jungle and battle games and on packet routing.

## Contribution

A widely used architecture for local, variable-neighbourhood interaction in MARL, the graph-attention alternative
to the mean embedding of [[huttenrauch-2019-deep]] and the action-mean of [[yang-2018-mean]].

## Key results

- Against independent DQN, CommNet and MeanField Q-learning (all parameter-shared, similar sizes, three runs),
  DGN converges to a much higher mean reward in battle, jungle and routing; in battle MFQ beats CommNet and DQN
  (measured, learning curves; exact numbers not transcribed). DGN also beats ATOC in an extra battle comparison.
- Ablations: graph convolution is the main source of gains; temporal relation regularisation adds consistency
  (claimed).

## Methods and models

Agents observe local features; adjacency from k nearest neighbours; convolution layers with multi-head
dot-product attention; shared parameters; DQN-style training with a KL regulariser between attention
distributions at consecutive steps. Environments built on MAgent [[zheng-2018-magent]].

## Limitations and open questions

Gridworld and network tasks only, no physical collective-motion model; attention weights are a tempting but
unvalidated read-out of "who influences whom".

## Relevance to us

If a hackathon learned-swarm needs more than mean pooling, this is the canonical graph-attention baseline, and its
attention weights could be compared to empirical interaction networks.
