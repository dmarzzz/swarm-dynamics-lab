---
id: szwajcok-2026-meme
type: paper
title: 'Meme Coin Factories: Uncovering Large-Scale Manipulations on pump.fun'
authors:
- Nicolas Szwajcok
- Taro Tsuchiya
- Enze Liu
- Kyle Soska
- Mathias Payer
- Nicolas Christin
year: 2026
venue: arXiv preprint (cs.CR)
url: https://arxiv.org/abs/2609.10246
doi: null
arxiv: '2609.10246'
cite: 'Szwajcok, N., Tsuchiya, T., Liu, E., Soska, K., Payer, M., & Christin, N. (2026). Meme Coin Factories: Uncovering Large-Scale Manipulations on pump.fun. arXiv preprint arXiv:2609.10246.'
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

Large-scale measurement of manipulation on pump.fun, the Solana memecoin launchpad: metadata for 15,183,009 coins (99.59% of all launched in two years) and full transaction histories for a random 1% coin sample (152,171 coins, about 50M transactions) plus all coins from a 5-day window, over 87M transactions in total. Five manipulation classes: wash trading, creator-address obfuscation, coordinated selling, copycat coins and social-media-triggered launches. A conservative atomic wash-trade rule (buy and sell the same amount in one transaction, only possible by bypassing the UI) finds at least 4 million wash trades (17% of trading transactions); wash trades are 50.3% of transactions for coins with over 10,000 trades, and doubling wash trades raises graduation odds by about 19%. First-funder clustering (with Arkham service labels removed and a leave-one-out robustness test) shrinks 3.2M creator addresses about 11x and the top 1% of clusters create 58.6% of all coins. Over 1.5M coins (10%) are exact copycats, 3.5M (23.5%) launch after Twitter or Truth Social posts, and the authors document Market-Manipulation-as-a-Service tools that sell multi-address creation, AI-generated comments, CAPTCHA solvers and proxy rotation.

## Contribution

The most complete measurement of automated, multi-address manipulation swarms on any chain, with conservative lower-bound detectors and the first documentation of commoditised manipulation services that offer AI-written social content.

## Key results

- At least 4M wash-trade transactions, 17% of all trading transactions; WT1 flags 8.26% of coins in the 1% sample.
- Wash-trade ratio rises with activity: 21.65% for coins with 1,000-10,000 transactions, 50.31% above 10,000.
- Wash-traded coins graduate at 2.0% vs 0.90% for others.
- Top 1% of creator addresses make 38.89% of coins; after 1-hop clustering the top 1% of clusters make 52.99%, and 58.6% at the deepest clustering.
- Nearly 8,000 coordinated-sell instances; one dump involved 312 senders. Dump volume in the 1% sample about USD 2.5-5M.
- Copycats: 1.5-1.9M (10-12%) by strict methods, 5.4M (36%) by name and symbol; originals graduate at 9.20% vs 0.86% for copycats.

## Methods and models

Solana RPC and indexer collection; WT1 (atomic same-amount buy and sell against the same bonding curve) and WT2 (same address buys and sells same amount at about the same price within a varied window, with fee tolerance); first-funder graph clustering to 3 hops with service-label pruning and adversarial leave-one-address-out; dump heuristics DP1/DP2; copycat matching on name, symbol, description and image; timing match to social posts; qualitative analysis of MMaaS websites and software.

## Limitations and open questions

WT2 has false positives at long windows (88.5% of coins flagged at 1 day). Funding-graph clustering can over-link through unlabelled services, which the authors test. Whether manipulators use LLM agents is not measured; MMaaS advertising of AI comments is a qualitative finding. Skimmed sections 1-5 and 9 plus the clustering method.

## Relevance to us

Directly on target for 'swarms in the wild': quantified multi-address coordination, conservative detectors that avoid MEV false positives, and a services market that sells swarm capability including AI-generated social posts. Builds on [[cernera-2022-token]] and [[mongardini-2025-midsummer]]; first-funder method also used in [[xiong-2026-can]]; bot code fingerprints in [[zheng-2026-demystifying]].
