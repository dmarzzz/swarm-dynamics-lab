---
id: zhu-2026-blockchain
type: paper
title: 'Blockchain Empowered Trustworthy Agent Networks: Foundations, Taxonomy, and Future Directions'
authors:
- Liehuang Zhu
- Yuhang Li
- Tianxing Wang
- Zhihao Chen
- Ke Li
- Hongyi Liu
- Yajie Wang
- Lei Xu
- Peng Jiang
- Zijian Zhang
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.04626
doi: null
arxiv: '2608.04626'
cite: 'Zhu, L., Li, Y., Wang, T., Chen, Z., Li, K., Liu, H., Wang, Y., Xu, L., Jiang, P., & Zhang, Z. (2026). Blockchain Empowered Trustworthy Agent Networks: Foundations, Taxonomy, and Future Directions. arXiv preprint arXiv:2608.04626.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A survey and tutorial covering literature from 1980 to 2026 on the move from classical multi-agent systems to open agent networks, where agents owned by different stakeholders interact without shared infrastructure for identity, authorisation, auditability, reputation or settlement. It proposes a five-dimension taxonomy of trust (entity and capability; authorisation and delegation; information and provenance; coordination and group robustness; accountability and settlement) and examines how blockchains supply shared identity, verifiable authorisation, tamper-evident provenance, auditable collaboration, incentives and settlement. It positions blockchain as a shared trust layer, not a replacement for agent security, semantic verification, privacy or robust reasoning.

## Contribution

A review article that organises the blockchain-for-agents line ([[chen-2024-blockagents]], [[luo-2025-weighted]], [[jo-2025-byzantine]], ERC-8004 style registries) under one taxonomy.

## Key results

- Review; no new measurements (abstract-level read).

## Methods and models

Literature survey and taxonomy.

## Limitations and open questions

Abstract only. Whether it treats Sybil resistance as part of "entity trust" or "group robustness" was not checked.

## Relevance to us

Its "information and provenance trust" and "coordination and group-robustness trust" dimensions correspond to the two Sybil failure modes in this lane: epistemic replication ([[bara-2026-epistemic]]) and identity-count capture ([[jo-2025-byzantine]], [[xia-2026-when]]). Compare the protocol comparison in [[hu-2025-inter-agent]].
