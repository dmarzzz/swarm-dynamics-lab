---
id: daian-2019-flash
type: paper
title: 'Flash Boys 2.0: Frontrunning, Transaction Reordering, and Consensus Instability in Decentralized Exchanges'
authors:
- Philip Daian
- Steven Goldfeder
- Tyler Kell
- Yunqi Li
- Xueyuan Zhao
- Iddo Bentov
- Lorenz Breidenbach
- Ari Juels
year: 2019
venue: arXiv preprint (cs.CR); IEEE S&P 2020
url: https://arxiv.org/abs/1904.05234
doi: null
arxiv: '1904.05234'
cite: 'Daian, P., Goldfeder, S., Kell, T., Li, Y., Zhao, X., Bentov, I., Breidenbach, L., & Juels, A. (2019). Flash Boys 2.0: Frontrunning, Transaction Reordering, and Consensus Instability in Decentralized Exchanges. arXiv preprint arXiv:1904.05234.'
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

Documents and quantifies the deployment of arbitrage bots on decentralised exchanges, which pay high fees and optimise latency to frontrun ordinary users. The authors observe bots competing in priority gas auctions (PGAs), repeatedly outbidding each other's fees to win transaction ordering, formalise PGAs as a continuous-time partial-information game, release a live data portal (frontrun.me), and introduce miner extractable value (MEV), showing that ordering fees create consensus-layer security risk.

## Contribution

Seminal: names MEV and identifies bot populations by their bidding behaviour in the public mempool, the first behavioural fingerprint of competing autonomous agents on chain.

## Key results

- Widespread and rising arbitrage-bot deployment on DEXs; PGAs observed and modelled; MEV shown to threaten consensus stability.

## Methods and models

Mempool observation of pending transactions and gas-price updates; revenue attribution for a subset of bot transactions; game-theoretic model of PGAs.

## Limitations and open questions

Abstract-level read; the population counted is limited to transactions with quantifiable revenue.

## Relevance to us

MEV bots are the longest-observed population of autonomous software agents competing in public with real money. Their identification methods (profit-pattern rules, gas-bidding behaviour, private-pool routing) and measured prevalence are the baseline for spotting newer LLM-driven agents on the same chains. Bidding-war interaction between bots is an early observed example of agent-agent strategic dynamics in the wild.
