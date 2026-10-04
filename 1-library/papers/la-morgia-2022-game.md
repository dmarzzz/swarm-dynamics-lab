---
id: la-morgia-2022-game
type: paper
title: 'A Game of NFTs: Characterizing NFT Wash Trading in the Ethereum Blockchain'
authors:
- Massimo La Morgia
- Alessandro Mei
- Alberto Maria Mongardini
- Eugenio Nerio Nemmi
year: 2022
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2212.01225
doi: null
arxiv: '2212.01225'
cite: 'La Morgia, M., Mei, A., Mongardini, A. M., & Nemmi, E. N. (2022). A Game of NFTs: Characterizing NFT Wash Trading in the Ethereum Blockchain. arXiv preprint arXiv:2212.01225.'
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

Measures NFT wash trading on Ethereum from the start of NFT markets to January 2022 using several detection approaches. Wash trading touches 5.66% of NFT collections with about $3.41 billion of artificial volume. Comparing two profit routes, farming marketplace token rewards (for example on LooksRare) is far more profitable (mean gain of successful operations $1.055M), succeeds in over 80% of operations, and is less risky than inflating an NFT's price for resale, where 50% of operations lose money.

## Contribution

Shows that incentive programmes, not price manipulation, drive most NFT wash trading, linking wash-trade swarms to airdrop and reward farming.

## Key results

- 5.66% of collections affected; artificial volume $3,406,110,774.
- Reward-farming wash trades: over 80% success, mean gain $1.055M on LooksRare; resale-inflation wash trades lose money in 50% of cases.

## Methods and models

Several detection approaches applied to Ethereum NFT trades from the beginning of NFT markets to January 2022; specific algorithms not read (abstract only).

## Limitations and open questions

Abstract-level read; detection thresholds and false-positive rate not checked.

## Relevance to us

Wash trading is the market form of a Sybil swarm: one operator controlling several addresses that trade with each other to fake activity. Detection heuristics here (closed cycles between linked addresses, common funders, zero net position change) are the transaction-level analogue of coordination detection for agent swarms. Mirrors airdrop-hunter detection in NFT markets [[zhou-2024-artemis]] and the marketplace comparison in [[niu-2024-unveiling]].
