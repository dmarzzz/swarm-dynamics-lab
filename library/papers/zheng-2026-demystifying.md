---
id: zheng-2026-demystifying
type: paper
title: 'Demystifying Solana Bots: From GitHub Blueprints to On-Chain Fingerprints'
authors:
- Xiaoye Zheng
- Yujing Chen
- Minghao Wu
- David Lo
- Difan Xie
- Daoyuan Wu
- Xiaohu Yang
- Zhiyuan Wan
year: 2026
venue: arXiv preprint (cs.SE)
url: https://arxiv.org/abs/2607.28424
doi: null
arxiv: '2607.28424'
cite: 'Zheng, X., Chen, Y., Wu, M., Lo, D., Xie, D., Wu, D., Yang, X., & Wan, Z. (2026). Demystifying Solana Bots: From GitHub Blueprints to On-Chain Fingerprints. arXiv preprint arXiv:2607.28424.'
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Joint code-and-chain study of Solana bots. From 586 GitHub bot repositories the authors derive a 15-category taxonomy in five domains (including trading operations, MEV and on-chain analytics), a shared five-stage operational pipeline, and 2,003 code building blocks with a long tail (90% appear in at most 3.1% of repos; trade execution in 58.5%). On chain they take 200 bot addresses (top-100 SolanaMevBot addresses from circular.bot and top-100 Axiom trading-bot addresses from Dune, February 2026) with 44,118,825 transactions and cluster execution fingerprints: submission intensity, execution success, cost and traded assets. Three clusters (56 addresses) look like MEV bots with WSOL as pivot in 70.9-99.9% of transactions; one cluster (102 addresses) looks like trading-operations bots with 80.9% of activity on pump.fun. Bot-related DEX volume exceeds $250M a day (January 2026).

## Contribution

Links bot source code to observable on-chain fingerprints, which is the bridge needed to attribute on-chain swarms to specific open-source frameworks.

## Key results

- 586 repos: TypeScript 48.2%, Python 17.9%, JavaScript 15.5%, Rust 14.9%; median 18 stars.
- Four execution clusters among 200 bot addresses separated by submission intensity and execution effectiveness.
- MEV bots that touch proprietary AMMs (for example HumidiFi) are profitable at three times the rate of those that do not (62.3% positive).
- Over 30% of dependencies are more than a year behind latest versions.

## Methods and models

GitHub collection and LLM-assisted tagging with two-author taxonomy reconciliation (91/100 sampled repos correctly categorised); function embeddings clustered with UMAP+HDBSCAN and labelled by DeepSeek-v3.2 at temperature 0; on-chain fingerprint features and clustering over the 200 addresses.

## Limitations and open questions

On-chain set comes from two bot services' leaderboards, so it covers successful, visible bots, not hidden or Sybil-farm wallets; no human control group. Skimmed.

## Relevance to us

The code-to-fingerprint method is what we would need to say 'this cluster of wallets runs framework X' for LLM agent frameworks such as ElizaOS. Compare MEV-bot ground truth on Ethereum [[niedermayer-2024-detecting]] and pump.fun manipulation [[szwajcok-2026-meme]]. MEV bots are the longest-observed population of autonomous software agents competing in public with real money. Their identification methods (profit-pattern rules, gas-bidding behaviour, private-pool routing) and measured prevalence are the baseline for spotting newer LLM-driven agents on the same chains.
