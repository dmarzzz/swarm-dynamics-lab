---
id: zhou-2024-artemis
type: paper
title: 'ARTEMIS: Detecting Airdrop Hunters in NFT Markets with a Graph Learning System'
authors:
- Chenyu Zhou
- Hongzhou Chen
- Hao Wu
- Junyu Zhang
- Wei Cai
year: 2024
venue: Proceedings of the ACM Web Conference 2024 (WWW '24)
url: https://faculty.washington.edu/weicaics/paper/papers/ChenyuZCWZC2024.pdf
doi: 10.1145/3589334.3645597
arxiv: null
cite: 'Zhou, C., Chen, H., Wu, H., Zhang, J., & Cai, W. (2024). ARTEMIS: Detecting Airdrop Hunters in NFT Markets with a Graph Learning System. In Proceedings of the ACM Web Conference 2024 (WWW ''24) (pp. 1824-1834). ACM. https://doi.org/10.1145/3589334.3645597'
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

Graph neural network for identifying airdrop hunters on the Blur NFT marketplace. The dataset has 2,453,280 NFT transactions over 203,370 addresses; of 123,815 airdrop recipients, 4,808 (about 4%) are labelled hunters using Blur's own exclusion records plus analyst review of clustered transaction loops. ARTEMIS combines a multimodal module (image and text embeddings of NFT metadata), a node aggregation that keeps the order of NFT transaction paths instead of merging parallel edges, and engineered market-manipulation features (Benford and last-digit tests, wash-trade loops). It reaches precision 0.820, recall 0.833, F1 0.826 against GraphSAGE 0.701, GIN 0.776, LightGBM 0.680 and SVM 0.629.

## Contribution

First detector specific to NFT airdrop farming, where hunters inflate trading volume through self-trades between their own wallets; it ties airdrop Sybil detection to wash-trading detection.

## Key results

- ARTEMIS F1 0.826 (P 0.820, R 0.833) on a 9:1 split; ablation shows transaction-based features matter most and image embeddings more than text.
- Context cited in the paper (not measured by it): analysts estimated about half of Blur's NFT volume and 84% of its bid-pool value came from hunters.

## Methods and models

Blur Season 1 transaction history and airdrop records; heterogeneous graph of wallets with ordered NFT transfers; frequency-inverse-order sampling for neighbours; pretrained vision and language encoders for NFT metadata; comparison to SVM, LightGBM, DeepWalk, Node2Vec, GCN, GraphSAGE, GAT, GIN. Data and code: doi.org/10.5281/zenodo.10676801.

## Limitations and open questions

Labels partly reflect Blur's own banning decisions, which the authors note were criticised as aggressive; boundary between professional hunters and active traders is blurred. One marketplace and one season. I skimmed the PDF (method, results, discussion), not the appendices in full.

## Relevance to us

Shows that incentive programmes produce self-trading swarms whose signature is shared with wash trading, so detectors from both literatures combine. Relates to [[la-morgia-2022-game]] (token-reward wash trading), [[niu-2024-unveiling]], [[liu-2025-detecting]] and [[fan-2023-altruistic]] from the same group.
