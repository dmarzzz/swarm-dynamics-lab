---
id: liu-2025-detecting
type: paper
title: 'Detecting Sybil Addresses in Blockchain Airdrops: A Subgraph-based Feature Propagation and Fusion Approach'
authors:
- Qiangqiang Liu
- Qian Huang
- Frank Fan
- Haishan Wu
- Xueyan Tang
year: 2025
venue: arXiv preprint (cs.CR); also IEEE ICBC 2025 per citing work
url: https://arxiv.org/abs/2505.09313
doi: null
arxiv: '2505.09313'
cite: 'Liu, Q., Huang, Q., Fan, F., Wu, H., & Tang, X. (2025). Detecting Sybil Addresses in Blockchain Airdrops: A Subgraph-based Feature Propagation and Fusion Approach. arXiv preprint arXiv:2505.09313.'
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: null
code: []
---

## Summary

Binance risk-team paper on supervised Sybil detection for airdrops, trained on confirmed Sybils from the Binance Account Bound (BAB) soulbound-token airdrop on BNB Smart Chain: 193,701 addresses including 23,240 Sybils (January 2023 to May 2024), with labels confirmed by clawback and a manual appeal process. For each address it builds a two-hop in/out transaction subgraph (58.4M transactions in total) and propagates 75 features toward the root: lifecycle timestamps (first gas receipt, first transaction, first airdrop-qualifying action, last transaction), amount statistics, and degree and neighbour counts. A LightGBM on these reaches precision 0.943, recall 0.918, F1 0.930, AUC 0.981, against 0.796/0.816/0.806/0.864 for the Trusta community-detection pipeline.

## Contribution

A rare industry dataset with adjudicated Sybil labels at scale, and evidence that 'just-in-time' lifecycle timing plus star, chain and tree funding motifs separate airdrop farms from users.

## Key results

- Subgraph LightGBM: P 0.9428, R 0.9182, F1 0.9303, AUC 0.9806.
- Baselines: plain LightGBM F1 0.747, decision tree 0.743, SVM 0.062 (recall 0.033), Trusta clustering 0.806.
- Top features: first airdrop-activity date, first transaction date, first gas date, total balance, USDT sent; Sybils hold balances just above the activity minimum and abandon the address after claiming.
- Authors state some notable airdrops contained over 30% Sybil addresses (cited, not measured here).

## Methods and models

Arkham labels used to drop exchange hot wallets and contracts; addresses with lifecycle over one year removed (2.6%). Cascade feature extraction over levels -2..+2, min/max/avg/var aggregation for amounts, summed degrees. Comparison to SVM, DT, LightGBM on first-order features and to TrustaLabs' open-source ATG community detection plus K-means.

## Limitations and open questions

Labels originate from the team's own clustering plus appeals, so the model may partly relearn the labelling heuristics. Train/test split and temporal holdout are not described. One chain and one campaign; the authors acknowledge features are dataset-specific. No adversarial evaluation.

## Relevance to us

Shows that supervised on-chain Sybil detection reaches above 0.9 when an operator can adjudicate labels, a useful upper bound; and that funding-tree topology and lifecycle timing are the core signals, the same ones used against agent reviewer swarms in [[xiong-2026-can]]. Compare unsupervised [[liu-2022-fighting]], training-free [[bartnicki-2026-compression]], and airdrop economics in [[messias-2023-airdrops]].
