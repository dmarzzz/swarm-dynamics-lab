---
id: raj-2022-case
type: talk
title: A Case-Study of MEV on Low-Fee Chains - Supragya Raj (Marlin)
authors:
- Supragya Raj
year: 2022
url: https://www.youtube.com/watch?v=YclrmwRv7gk
venue: 'Flashbots, MEV in 2021: A Year In Review'
topics:
- sybil-resistance
added_by: shadow/sol-w8
accessed: '2026-10-03'
read_depth: full
relevance: 5
---

## Summary

Raj studies arbitrage and spam on Polygon PoS. At 2:14-5:42 he reports roughly $37 million of detected Uniswap-v2-style arbitrage from January through October 2021, emphasizing that this excludes more complex extraction. His 100,000-block heuristics attribute 40-57% of transactions to MEV-related spam, not a validated identity classifier. At 8:02-12:44 he compares trace translation with event-based analysis: tracing takes about 1.5 seconds per block on a 5950X, while the restricted event detector backfills the studied period in about 36 hours. At 12:45-17:32 he discusses private bundles, simulation, validator-key safety, double-signing concerns and adoption incentives.

## Relevance to us

Concrete case for how cheap repeated attempts create adversarial population-like traffic without proving distinct identities. Detection coverage and account heuristics must be distinguished from a true Sybil estimate. The engineering trade-off between event features and expensive execution traces is directly useful.

## Reading notes

Read the entire timestamped transcript retrieved with yt_transcript.sh (Apify fallback). Automatic captions contain transcription errors; numerical claims below are attributed to the speaker, not independently replicated. 
