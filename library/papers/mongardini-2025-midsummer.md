---
id: mongardini-2025-midsummer
type: paper
title: 'A Midsummer Meme''s Dream: Investigating Market Manipulations in the Meme Coin Ecosystem'
authors:
- Alberto Maria Mongardini
- Alessandro Mei
year: 2025
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2507.01963
doi: null
arxiv: '2507.01963'
cite: 'Mongardini, A. M., & Mei, A. (2025). A Midsummer Meme''s Dream: Investigating Market Manipulations in the Meme Coin Ecosystem. arXiv preprint arXiv:2507.01963.'
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

Cross-chain analysis of 34,988 meme coins on Ethereum, BNB Smart Chain, Solana and Base over a three-month longitudinal window. Among high-return tokens (over 100%), 82.8% show evidence of artificial growth: wash trading and a newly defined Liquidity Pool-Based Price Inflation (LPI), where small strategic purchases trigger large price increases. Profit extraction (pump-and-dumps, rug pulls) typically follows these initial manipulations. Over 17,000 victim addresses lost more than $9.3M.

## Contribution

Shows coordinated artificial activity is the norm, not the exception, among successful meme coins across four chains, and introduces LPI as a manipulation pattern.

## Key results

- 82.8% of high-return (>100%) meme coins show artificial growth.
- Over 17,000 victimised addresses; realised losses over $9.3M.

## Methods and models

Token discovery and tokenomics characterisation across four chains; detection of wash trading and LPI; linkage of early manipulation to later pump-and-dump or rug pull (details not read).

## Limitations and open questions

Abstract-level read; detection thresholds and false-positive rates not checked.

## Relevance to us

A measured base rate of coordinated manipulation among one asset class, and a sequencing result (fake activity first, extraction later) that a swarm detector could use as an early warning. See [[szwajcok-2026-meme]] for pump.fun at full scale.
