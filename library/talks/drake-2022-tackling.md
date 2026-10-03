---
id: drake-2022-tackling
type: talk
title: Tackling MEV with cryptography - Justin Drake (Ethereum Foundation)
authors:
- Justin Drake
year: 2022
url: https://www.youtube.com/watch?v=mpRq-WFihz8
venue: Flashbots
topics:
- sybil-resistance
added_by: shadow/sol-w8
accessed: '2026-10-03'
read_depth: full
relevance: 4
---

## Summary

Transcript coverage: 0:00-18:53, including closing discussion when present. Drake treats several consensus weaknesses as MEV opportunities: predictable proposers invite denial of service, ranked fallback proposers permit time-buying, randomness withholding changes valuable future slots, and reorgs enable time-bandit extraction. He proposes secret single leader election, verifiable delay randomness and aggregated-signature single-slot finality as research directions. The second half proposes encrypting transactions before inclusion with guaranteed decryption afterward, comparing committee threshold, delay and witness-based decryption. An envisioned multistage PBS/finality/decryption schedule preserves one user-visible execution slot, but implementation details and encrypted metadata remain open. Throughput multipliers and postmerge block values are forecasts, not demonstrated performance.

## Relevance to us

Catalogues attacks in which ownership across slots and roles matters more than node count. Cryptographic proposals require explicit timing, trust and deployment assumptions. Compare the rational-coalition limitation in [[nayak-2023-order]].

## Reading notes

Read the entire timestamped transcript retrieved with yt_transcript.sh (Apify fallback). Automatic captions contain transcription errors; numerical claims below are attributed to the speaker, not independently replicated. 
