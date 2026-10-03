---
id: cernera-2022-token
type: paper
title: 'Token Spammers, Rug Pulls, and SniperBots: An Analysis of the Ecosystem of Tokens in Ethereum and in the Binance Smart Chain (BNB)'
authors:
- Federico Cernera
- Massimo La Morgia
- Alessandro Mei
- Francesco Sassi
year: 2022
venue: arXiv preprint (cs.CR); 32nd USENIX Security Symposium (USENIX Security 23)
url: https://arxiv.org/abs/2206.08202
doi: null
arxiv: '2206.08202'
cite: 'Cernera, F., La Morgia, M., Mei, A., & Sassi, F. (2022). Token Spammers, Rug Pulls, and SniperBots: An Analysis of the Ecosystem of Tokens in Ethereum and in the Binance Smart Chain (BNB). arXiv preprint arXiv:2206.08202. Also in 32nd USENIX Security Symposium (USENIX Security 23).'
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

Longitudinal analysis of tokens and liquidity pools on BNB Smart Chain and Ethereum from inception to March 2022. About 60% of tokens are active for less than one day, and 1% of addresses create 20-25% of all tokens. These disposable tokens are used for a '1-day rug pull' that the authors estimate generated $240M in profit, more prevalent on BNB Smart Chain. They identify 'sniper bots', trader bots that buy newly listed tokens in the first blocks, detect them and quantify their activity in rug-pull operations.

## Contribution

Defines and measures sniper bots and shows token-creation concentration (1% of addresses making a fifth of tokens), an early example of operator-level swarms of disposable contracts.

## Key results

- About 60% of tokens live under one day; 1% of addresses create 20-25% of tokens.
- 1-day rug pulls estimated at $240M profit.
- Sniper bots detected and their participation in rug-pull pools quantified.

## Methods and models

Full-history crawl of token and pool contracts on two chains; heuristics for rug pulls and sniper-bot behaviour (details not read).

## Limitations and open questions

Abstract-level read.

## Relevance to us

MEV bots are the longest-observed population of autonomous software agents competing in public with real money. Their identification methods (profit-pattern rules, gas-bidding behaviour, private-pool routing) and measured prevalence are the baseline for spotting newer LLM-driven agents on the same chains. The creator-concentration finding is repeated at much larger scale on pump.fun in [[szwajcok-2026-meme]].
