---
id: agarwal-2025-lpac
type: paper
title: "LPAC: Learnable Perception-Action-Communication Loops With Applications to Coverage Control"
authors: ["Saurav Agarwal", "Ramya Muthukrishnan", "Walker Gosrich", "Vijay Kumar", "Alejandro Ribeiro"]
year: 2025
venue: "IEEE Transactions on Robotics"
url: https://arxiv.org/abs/2401.04855
doi: "10.1109/tro.2025.3619047"
arxiv: null
cite: "Agarwal, S., Muthukrishnan, R., Gosrich, W., Kumar, V., & Ribeiro, A. (2025). LPAC: Learnable Perception-Action-Communication Loops With Applications to Coverage Control. IEEE Transactions on Robotics, 41, 5986-6005. (arXiv:2401.04855)"
topics: [swarm-robotics, marl-emergence, sync-consensus]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "6 (Crossref, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

LPAC is a learnable perception-action-communication architecture for decentralised coverage control: a CNN processes each robot's local map, a GNN decides what to communicate and aggregates neighbour messages, and a shallow MLP outputs actions. It is trained by imitating a centralised clairvoyant algorithm. The abstract reports that LPAC beats standard decentralised and centralised coverage controllers, generalises to larger environments and more robots, and is robust to noisy positions.

## Contribution

A clean example of learned communication in swarms from the Kumar/Ribeiro graph-learning line, in the tradition of 'Learning Decentralized Controllers for Robot Swarms with GNNs' (Tolstaya et al., CoRL 2019).

## Key results

- Outperforms standard decentralised and centralised coverage algorithms (claimed in abstract).
- Transfers to larger environments and robot counts without retraining (claimed in abstract).

## Methods and models

CNN perception + GNN communication + MLP action, trained by imitation of a centralised clairvoyant coverage algorithm (Lloyd-style). Published in T-RO volume 41.

## Limitations and open questions

Abstract-depth entry. Imitation of a clairvoyant expert caps performance at the expert's. Communication is assumed reliable within range.

## Relevance to us

A template for learned message passing in a swarm hackathon project. Compare [[zhang-2025-gcbf]] and [[wang-2025-local]].
