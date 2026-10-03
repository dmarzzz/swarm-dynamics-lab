---
id: tolstaya-2020-learning
type: paper
title: Learning Decentralized Controllers for Robot Swarms with Graph Neural Networks
authors:
- Ekaterina Tolstaya
- Fernando Gama
- James Paulos
- George Pappas
- Vijay Kumar
- Alejandro Ribeiro
year: 2020
venue: Proceedings of the Conference on Robot Learning (CoRL 2019), PMLR 100
url: https://proceedings.mlr.press/v100/tolstaya20a.html
doi: null
arxiv: '1903.10527'
cite: Tolstaya, E., Gama, F., Paulos, J., Pappas, G., Kumar, V., & Ribeiro, A. (2020). Learning decentralized controllers for robot swarms with graph neural networks. In Proceedings of the Conference on Robot Learning, PMLR 100, 671–682.
topics:
- marl-emergence
- swarm-robotics
- sync-consensus
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 209 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Mobile robots with interacting dynamics and sparse communication need local controllers. The authors imitate a centralised flocking controller that uses global information, training a single shared local controller built from aggregation graph neural networks extended to time-varying signals and graphs. The learned controller uses multi-hop information from distant teammates via local exchanges, and the value of multi-hop information grows as communication radius shrinks and speeds increase.

## Contribution

Established graph neural networks as the decentralised policy class for swarms, via imitation of a centralised expert rather than RL; a standard alternative to the mean embedding of [[huttenrauch-2019-deep]]. Links learned control to the Olfati-Saber/Tanner flocking-control tradition ([[olfati-saber-2006-flocking]], [[tanner-2007-flocking]]).

## Key results

- Learned decentralised flocking works on communication graphs that change as robots move (claimed in abstract).
- Multi-hop aggregation matters more for smaller communication radii and faster velocities (claimed).

## Methods and models

Aggregation GNN over time-varying proximity graphs, behaviour cloning (DAgger-style imitation) of a global controller. Abstract-level read.

## Limitations and open questions

Imitation learning needs a centralised expert; no RL, so it cannot discover behaviours the expert lacks.

## Relevance to us

GNN policy architecture for any learned-flocking experiment; compare with [[batra-2022-decentralized]] (end-to-end RL on real quadrotors) and [[huttenrauch-2019-deep]].
