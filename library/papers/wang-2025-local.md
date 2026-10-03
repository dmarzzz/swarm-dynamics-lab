---
id: wang-2025-local
type: paper
title: "Local-Canonicalization Equivariant Graph Neural Networks for Sample-Efficient and Generalizable Swarm Robot Control"
authors: ["Keqin Wang", "Tao Zhong", "David Chang", "Christine Allen-Blanchette"]
year: 2025
venue: "arXiv preprint (accepted at IROS 2026)"
url: https://arxiv.org/abs/2509.14431
doi: null
arxiv: "2509.14431"
cite: "Wang, K., Zhong, T., Chang, D., & Allen-Blanchette, C. (2025). Local-Canonicalization Equivariant Graph Neural Networks for Sample-Efficient and Generalizable Swarm Robot Control. arXiv preprint arXiv:2509.14431."
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "1 (Semantic Scholar, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

LEGO is a MARL policy architecture that canonicalises each agent's observations into its own frame (making the policy E(2)-equivariant once actions are mapped back) and uses role-wise graph encoders for permutation equivariance and variable team sizes. Paired with MAPPO on MPE Spread and Tag-occlusion, it improves sample efficiency and final performance over MLP, graph-only, canonicalisation-only and equivariant baselines. Policies transfer without fine-tuning to unseen team sizes, and a Crazyflie pursuit test keeps working after one pursuer is disabled.

## Contribution

It builds symmetry (E(2) and permutation) into swarm policies cheaply via local canonicalisation, an alternative to heavier equivariant GNNs.

## Key results

- Better sample efficiency and task performance than four baseline architectures on MPE tasks (claimed in abstract).
- Zero-shot transfer to unseen team sizes; Crazyflie experiment robust to one disabled pursuer.

## Methods and models

Agent-centric canonicalisation + role-wise GNN encoders + MAPPO. Code: https://github.com/CAB-Lab-Princeton/LEGO-MARL (from the arXiv abstract).

## Limitations and open questions

Abstract-depth entry. MPE benchmarks are simple particle tasks; hardware is a small demonstration.

## Relevance to us

An architecture choice for any learned swarm policy at the hackathon. See [[agarwal-2025-lpac]] and [[sebastian-2025-physics]].
