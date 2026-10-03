---
id: falk-2023-can
type: paper
title: Can AI Detect Wash Trading? Evidence from NFTs
authors:
- Brett Hemenway Falk
- Gerry Tsoukalas
- Niuniu Zhang
year: 2023
venue: arXiv preprint (q-fin)
url: https://arxiv.org/abs/2311.18717
doi: null
arxiv: '2311.18717'
cite: Falk, B. H., Tsoukalas, G., & Zhang, N. (2023). Can AI Detect Wash Trading? Evidence from NFTs. arXiv preprint arXiv:2311.18717.
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Uses public on-chain NFT data to estimate wash trading directly on three major NFT exchanges and to audit indirect methods. About 38% of trades (range 30-40%) and about 60% of traded value (range 25-95%) likely involve manipulation, varying by exchange. With this direct evidence the authors find roundedness-based regressions in the style of [[cong-2021-crypto]] the most promising indirect method but still error-prone, and build an AI-based estimator that embeds those regressions in a machine-learning model, reducing exchange-level and trade-level error.

## Contribution

A validation of indirect fake-activity estimators against on-chain ground truth: the kind of calibration step agent-swarm prevalence estimates usually lack.

## Key results

- About 38% of trades and about 60% of value likely manipulated across three NFT exchanges.
- Roundedness regressions are the best indirect method but err in the NFT setting; ML hybrid reduces error.

## Methods and models

On-chain identification of wash trades on NFT exchanges, then comparison with Benford, roundedness and tail-based indirect estimators; ML estimator integrating roundedness features.

## Limitations and open questions

Abstract-level read; ground truth is itself heuristic on-chain linking.

## Relevance to us

Wash trading is the market form of a Sybil swarm: one operator controlling several addresses that trade with each other to fake activity. Detection heuristics here (closed cycles between linked addresses, common funders, zero net position change) are the transaction-level analogue of coordination detection for agent swarms. Method template: calibrate a cheap population-level estimator against a smaller directly linked sample, then apply it where linkage is unavailable.
