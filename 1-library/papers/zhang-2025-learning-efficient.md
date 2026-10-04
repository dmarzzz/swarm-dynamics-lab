---
id: zhang-2025-learning-efficient
type: paper
title: "Learning Efficient Flocking Control Based on Gibbs Random Fields"
authors: ["Dengyu Zhang", "Chenghao Yu", "Feng Xue", "Qingrui Zhang"]
year: 2025
venue: "IEEE Robotics and Automation Letters"
url: https://arxiv.org/abs/2502.02984
doi: "10.1109/lra.2025.3541909"
arxiv: "2502.02984"
cite: "Zhang, D., Yu, C., Xue, F., & Zhang, Q. (2025). Learning Efficient Flocking Control Based on Gibbs Random Fields. IEEE Robotics and Automation Letters, 10(4), 3478-3485."
topics: [swarm-robotics, marl-emergence, collective-motion]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "3 (OpenAlex W4407449470, 2026-10-03); 3 (Crossref, 2026-10-03)"
code: []
---

## Summary

A MARL framework for flocking in congested environments that models the multi-robot system as a Gibbs random field: a joint distribution over robot variables that gives a principled flocking reward and a GRF-based credit assignment enabling decentralised training and execution. An action-attention module anticipates neighbours' intentions to reduce non-stationarity. Learned distributed policies reach about 99% success in challenging environments, compared with state-of-the-art methods in simulation and experiments.

## Contribution

It uses statistical-physics-style energy models (GRFs) for reward design and credit assignment in learned flocking.

## Key results

- About 99% success rate in congested environments (simulation and experiments, per the abstract).
- Ablations validate each module.

## Methods and models

GRF-based reward and credit assignment, action-attention, decentralised MARL training and execution, real-robot experiments (platform not checked). Note: arXiv lists the second author's name as only 'Chenghao'; I use the published RA-L author list.

## Limitations and open questions

Abstract-depth entry.

## Relevance to us

A learned-flocking baseline in congested spaces; compare [[choi-2026-communication]] (comm-free) and [[huang-2024-collision]].
