---
id: victor-2021-detecting
type: paper
title: Detecting and Quantifying Wash Trading on Decentralized Cryptocurrency Exchanges
authors:
- Friedhelm Victor
- Andrea Marie Weintraud
year: 2021
venue: arXiv preprint (q-fin); WWW 2021
url: https://arxiv.org/abs/2102.07001
doi: null
arxiv: '2102.07001'
cite: Victor, F., & Weintraud, A. M. (2021). Detecting and Quantifying Wash Trading on Decentralized Cryptocurrency Exchanges. arXiv preprint arXiv:2102.07001.
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

First detection of wash trading on decentralised exchanges, on the order-book DEXs IDEX and EtherDelta (Ethereum). The authors identify a lower bound of accounts and trade structures meeting legal definitions of wash trading: self-trades, two-account round trips and more complex multi-account cycles. They measure wash volume equivalent to $159 million, find that more than 30% of all traded tokens on both exchanges were wash traded, and that on EtherDelta 10% of tokens were almost exclusively wash traded. Data are released.

## Contribution

Seminal on-chain coordinated-trading measurement, made possible because every trade and counterparty is public.

## Key results

- Wash trading volume about $159M across IDEX and EtherDelta (lower bound).
- Over 30% of traded tokens on each exchange affected; 10% of EtherDelta tokens almost exclusively wash traded.
- Self-trades and two-account structures dominate; larger rings occur.

## Methods and models

Reconstruction of order-book DEX trades on IDEX and EtherDelta and identification of accounts and trading structures (self-trades, two-account and larger structures) that meet legal definitions of wash trading. Exact algorithm not read (abstract only).

## Limitations and open questions

Abstract-level read. Lower bound only: accounts linked through other channels (funding, off-chain) are not merged.

## Relevance to us

Wash trading is the market form of a Sybil swarm: one operator controlling several addresses that trade with each other to fake activity. Detection heuristics here (closed cycles between linked addresses, common funders, zero net position change) are the transaction-level analogue of coordination detection for agent swarms. Foundational for the NFT studies [[la-morgia-2022-game]], [[von-wachter-2022-nft]], [[chen-2023-dark]] and the pump.fun measurement [[szwajcok-2026-meme]].
