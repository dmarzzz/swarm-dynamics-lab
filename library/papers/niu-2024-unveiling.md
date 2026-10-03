---
id: niu-2024-unveiling
type: paper
title: Unveiling Wash Trading in Popular NFT Markets
authors:
- Yuanzheng Niu
- Xiaoqi Li
- Hongli Peng
- Wenkai Li
year: 2024
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2403.10361
doi: null
arxiv: '2403.10361'
cite: Niu, Y., Li, X., Peng, H., & Li, W. (2024). Unveiling Wash Trading in Popular NFT Markets. arXiv preprint arXiv:2403.10361.
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Systematic analysis of four NFT marketplaces covering more than 25 million transactions, tracking how wash trading evolved. The authors propose a heuristic combining transaction-network features with behavioural analysis. Marketplaces with token-incentive structures show far higher wash-trading shares: LooksRare 94.5% and X2Y2 84.2% of volume.

## Contribution

Cross-marketplace evidence that reward incentives create the majority of volume through self-trading swarms.

## Key results

- Wash-trading share of volume: LooksRare 94.5%, X2Y2 84.2%; higher on incentivised markets.

## Methods and models

Network plus behavioural heuristic over marketplace transactions.

## Limitations and open questions

Abstract-level read; heuristic thresholds unchecked.

## Relevance to us

Wash trading is the market form of a Sybil swarm: one operator controlling several addresses that trade with each other to fake activity. Detection heuristics here (closed cycles between linked addresses, common funders, zero net position change) are the transaction-level analogue of coordination detection for agent swarms. Agrees with [[la-morgia-2022-game]] that rewards drive wash volume.
