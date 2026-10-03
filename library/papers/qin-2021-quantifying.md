---
id: qin-2021-quantifying
type: paper
title: 'Quantifying Blockchain Extractable Value: How dark is the forest?'
authors:
- Kaihua Qin
- Liyi Zhou
- Arthur Gervais
year: 2021
venue: arXiv preprint (cs.CR); IEEE S&P 2022
url: https://arxiv.org/abs/2101.05511
doi: null
arxiv: '2101.05511'
cite: 'Qin, K., Zhou, L., & Gervais, A. (2021). Quantifying Blockchain Extractable Value: How dark is the forest?. arXiv preprint arXiv:2101.05511.'
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

Quantifies blockchain extractable value (BEV) from sandwich attacks, liquidations and DEX arbitrage on Ethereum over 32 months: $540.54M of profit divided among 11,289 addresses, across 49,691 cryptocurrencies and 60,830 markets, with a maximum single instance of $4.1M (616.6x the block reward). It gives the first concrete algorithm for a generalised frontrunning bot that copies and replaces unconfirmed profitable transactions without understanding them, estimated to have earned 57,037 ETH ($35.37M), and analyses how BEV relays aggravate consensus attacks.

## Contribution

Population count of extracting addresses (11,289) and a reference generalised-bot algorithm.

## Key results

- $540.54M BEV over 32 months among 11,289 addresses; generalised frontrunner potential 57,037 ETH.

## Methods and models

Heuristic identification of sandwich, liquidation and arbitrage transactions; simulation of a replay-based generalised frontrunner; formal relay analysis.

## Limitations and open questions

Abstract-level read; address counts are not operator counts (one operator may run many addresses).

## Relevance to us

MEV bots are the longest-observed population of autonomous software agents competing in public with real money. Their identification methods (profit-pattern rules, gas-bidding behaviour, private-pool routing) and measured prevalence are the baseline for spotting newer LLM-driven agents on the same chains.
