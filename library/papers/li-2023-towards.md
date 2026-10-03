---
id: li-2023-towards
type: paper
title: Towards Understanding and Characterizing the Arbitrage Bot Scam In the Wild
authors:
- Kai Li
- Shixuan Guan
- Darren Lee
year: 2023
venue: arXiv preprint (cs.CR)
url: https://arxiv.org/abs/2310.12306
doi: null
arxiv: '2310.12306'
cite: Li, K., Guan, S., & Lee, D. (2023). Towards Understanding and Characterizing the Arbitrage Bot Scam In the Wild. arXiv preprint arXiv:2310.12306.
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

Measures the 'arbitrage bot' scam, in which YouTube videos lure victims to deploy a so-called bot contract that steals their funds. The automated CryptoScamHunter system collected and classified YouTube videos from June 2022 to June 2023, finding 10,442 scam videos from thousands of accounts, including crafted popular accounts and spam accounts, plus obfuscation that hides the scam address in contract code. From 800+ bot contracts it extracts 354 scam addresses, expands to 1,697 by contract similarity, and traces over 25,000 victims and up to $15M in losses on Ethereum and BNB Smart Chain.

## Contribution

A cross-platform detection pipeline that links a social-media account swarm (spam and crafted YouTube accounts) to on-chain addresses, and uses contract similarity to expand seed addresses.

## Key results

- 10,442 scam videos detected over 12 months; 1,697 scam addresses after similarity expansion.
- Over 25,000 victims; losses up to $15M.

## Methods and models

Continuous YouTube crawling and classification; source download and address extraction from linked contracts; similar-contract matching; transaction tracing.

## Limitations and open questions

Abstract-level read. Detects the scam campaign, not bots acting on chain; the social accounts are the swarm.

## Relevance to us

One of few works joining social-platform account swarms with on-chain money flows, the linkage a cross-platform agent-swarm detector needs. Seed-expansion by code similarity parallels [[bartnicki-2026-compression]].
