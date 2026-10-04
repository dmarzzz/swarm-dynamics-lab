---
id: cong-2021-crypto
type: paper
title: Crypto Wash Trading
authors:
- Lin William Cong
- Xi Li
- Ke Tang
- Yang Yang
year: 2021
venue: arXiv preprint (q-fin)
url: https://arxiv.org/abs/2108.10984
doi: null
arxiv: '2108.10984'
cite: Cong, L. W., Li, X., Tang, K., & Yang, Y. (2021). Crypto Wash Trading. arXiv preprint arXiv:2108.10984.
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

Statistical tests for fabricated volume on 29 centralised cryptocurrency exchanges, using regularities seen in regulated markets and in nature: first-significant-digit (Benford) distributions, round-number clustering of trade sizes, and power-law trade-size tails. Regulated exchanges conform; unregulated exchanges deviate in ways not explained by strategy or exchange heterogeneity. The estimated wash share averages over 70% of reported volume on unregulated exchanges, trillions of dollars a year, and fabricated volume improves exchange rankings and temporarily moves prices.

## Contribution

The standard indirect (distributional) detector for fake volume when counterparties are not observable; its features reappear in on-chain bot detectors ([[niedermayer-2024-detecting]] uses Benford and round-number features).

## Key results

- Wash trading averages over 70% of reported volume on unregulated exchanges.
- Deviations in Benford, round-number clustering and tail exponents separate regulated from unregulated venues.

## Methods and models

Exchange-level trade data; Benford chi-square tests; trade-size clustering at round numbers; power-law tail fits; regressions of fake volume on exchange characteristics.

## Limitations and open questions

Abstract-level read. Indirect estimates: [[falk-2023-can]] uses on-chain NFT ground truth and finds roundedness regressions most promising but still error-prone.

## Relevance to us

Wash trading is the market form of a Sybil swarm: one operator controlling several addresses that trade with each other to fake activity. Detection heuristics here (closed cycles between linked addresses, common funders, zero net position change) are the transaction-level analogue of coordination detection for agent swarms. Distributional tests that need no identity linkage are relevant to detecting swarm-generated volume or content when individual accounts cannot be linked.
