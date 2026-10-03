---
id: weintraub-2022-flash
type: paper
title: 'A Flash(bot) in the Pan: Measuring Maximal Extractable Value in Private Pools'
authors:
- Ben Weintraub
- Christof Ferreira Torres
- Cristina Nita-Rotaru
- Radu State
year: 2022
venue: arXiv preprint (cs.CR); ACM IMC 2022
url: https://arxiv.org/abs/2206.04185
doi: null
arxiv: '2206.04185'
cite: 'Weintraub, B., Torres, C. F., Nita-Rotaru, C., & State, R. (2022). A Flash(bot) in the Pan: Measuring Maximal Extractable Value in Private Pools. arXiv preprint arXiv:2206.04185.'
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

Measures whether Flashbots, a private transaction pool built to reduce MEV externalities, meets its stated goals. Flashbots miners held over 99.9% of hash power; powerful miners earned more than twice what they made before; over 90% of Flashbots blocks came from two miners; and over 80% of MEV extraction ran through Flashbots while 13.2% came from other private pools.

## Contribution

Shows bot activity migrated from the public mempool to private channels, which changes what an outside observer can see and therefore how bots can be detected.

## Key results

- Over 80% of MEV via Flashbots, 13.2% via other private pools; 90%+ of Flashbots blocks from two miners.

## Methods and models

Block and bundle analysis comparing Flashbots and non-Flashbots blocks (details not read).

## Limitations and open questions

Abstract-level read; pre-Merge proof-of-work period.

## Relevance to us

MEV bots are the longest-observed population of autonomous software agents competing in public with real money. Their identification methods (profit-pattern rules, gas-bidding behaviour, private-pool routing) and measured prevalence are the baseline for spotting newer LLM-driven agents on the same chains. Private order flow is an observability problem for any on-chain agent census.
