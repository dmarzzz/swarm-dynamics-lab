---
id: tosic-2023-beyond
type: paper
title: 'Beyond the Surface: Advanced Wash Trading Detection in Decentralized NFT Markets'
authors:
- Aleksandar Tošić
- Niki Hrovatin
- Jernej Vičič
year: 2023
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2312.16603
doi: null
arxiv: '2312.16603'
cite: 'Tošić, A., Hrovatin, N., & Vičič, J. (2023). Beyond the Surface: Advanced Wash Trading Detection in Decentralized NFT Markets. arXiv preprint arXiv:2312.16603.'
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

Extends NFT wash-trading detection beyond direct trades by joining NFT ownership traces with the full Ethereum transaction network of the accounts, so accounts linked through ordinary ETH transfers are merged. Across 7 notable collections, wash trading reaches up to 25% of volume excluding Meebits, and 93% of Meebits volume is attributed to wash trading. The authors conclude wash trading is underestimated by surface-level methods.

## Contribution

Shows that adding funding-graph linkage raises measured coordinated activity substantially, the same effect seen when Sybil detectors add first-funder trees.

## Key results

- Up to 25% of volume across six collections; 93% for Meebits.

## Methods and models

Joint analysis of NFT transfer traces and the Ethereum normal-transaction network to link accounts before cycle detection.

## Limitations and open questions

Abstract-level read; seven collections only; merging via transfers can over-link through shared services.

## Relevance to us

Wash trading is the market form of a Sybil swarm: one operator controlling several addresses that trade with each other to fake activity. Detection heuristics here (closed cycles between linked addresses, common funders, zero net position change) are the transaction-level analogue of coordination detection for agent swarms. Compare the much lower surface-level estimates in [[von-wachter-2022-nft]] and [[chen-2023-dark]].
