---
id: hermann-2022-mev
type: talk
title: MEV Reduction via Batch Auction - Alex Hermann (Cowswap)
authors:
- Alex Hermann
year: 2022
url: https://www.youtube.com/watch?v=nEpDHiZfFyA
venue: Flashbots / CoW Swap
topics:
- sybil-resistance
added_by: shadow/sol-w8
accessed: '2026-10-03'
read_depth: full
relevance: 4
---

## Summary

Hermann compares sequential AMM trading with frequent batch auctions. At 2:57-5:17 opposite orders cross internally and residual demand alone reaches AMMs, with a uniform clearing price. At 5:44-7:50 he illustrates within-block price dispersion and presents speaker-estimated annual savings of $27 million and $28 million on two ETH stablecoin pairs, not a replicated benchmark. At 8:03-10:20 he argues that internal matching shrinks the MEV surface and reports roughly 13% potentially internally matched ETH-USDC volume. At 10:22-15:20 he discusses latency, information leakage, large-order splitting and changing AMM state. Q&A acknowledges current centralization and censorship exposure while presenting solver decentralization as a direction.

## Relevance to us

A mechanism that reduces competition over ordering by changing the allocation rule rather than identifying bots. Protection of residual trades still relies on routing and privacy assumptions. Explicit censorship caveats prevent treating vendor claims as universal guarantees.

## Reading notes

Read the entire timestamped transcript retrieved with yt_transcript.sh (Apify fallback). Automatic captions contain transcription errors; numerical claims below are attributed to the speaker, not independently replicated. 
