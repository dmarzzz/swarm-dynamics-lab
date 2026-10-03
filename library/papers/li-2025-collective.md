---
id: li-2025-collective
type: paper
title: "Collective Behavior Clone with Visual Attention via Neural Interaction Graph Prediction"
authors: ["Kai Li", "Zhao Ma", "Liang Li", "Shiyu Zhao"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2503.06869
doi: null
arxiv: "2503.06869"
cite: "Li, K., Ma, Z., Li, L., & Zhao, S. (2025). Collective Behavior Clone with Visual Attention via Neural Interaction Graph Prediction. arXiv preprint arXiv:2503.06869."
topics: [collective-motion, swarm-robotics, marl-emergence]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null  # arXiv-only; OpenAlex budget exhausted and Semantic Scholar rate-limited on 2026-10-03
code: []
---
## Summary

Collective behavioural cloning (CBC): a graph variational autoencoder learns the local interaction graph from swarm trajectories, then behaviour cloning learns the control policy given that graph. A visual attention network trained on the learned graph selects neighbours online, and the system is deployed on a real decentralised vision-based robot swarm. The authors report better prediction of both interaction graphs and actions than previous approaches; code and data are said to be available.

## Contribution

End-to-end pipeline from trajectories to an interaction graph to a deployable vision-based policy.

## Key results

- Claimed (abstract): higher accuracy for interaction-graph and action prediction than prior methods; real-robot deployment.

## Methods and models

Graph VAE (NRI-like), behaviour cloning, visual attention for neighbour selection.

## Limitations and open questions

Abstract only; repository URL not found on the abstract page.

## Relevance to us

Bridges [[han-2024-collective]] style relational inference and robot control; compare [[zheng-2024-body]].
