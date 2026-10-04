---
id: nayak-2023-order
type: talk
title: 'Order Policy Enforcement: Limitations and Circumvention - Kartik Nayak | MEV-SBC
  ’23'
authors:
- Kartik Nayak
year: 2023
url: https://www.youtube.com/watch?v=Js0gD50vx4I
venue: MEV-SBC 2023 / Flashbots
topics:
- sybil-resistance
added_by: shadow/sol-w8
accessed: '2026-10-03'
read_depth: full
relevance: 5
---

## Summary

Transcript coverage: 0:00-26:27, including closing discussion when present. Nayak distinguishes arrival-time fairness from content-oblivious ordering, then asks whether either remains enforceable when all ordering parties are rational rather than an honest majority. In the main proof discussion, a framework with ephemeral clients, transaction binding and an unchanged prereveal transaction state permits colluding parties to reconstruct a more profitable stream indistinguishable from another legitimate input. The framework excludes time-lock protocols. Proposed escapes keep clients online through commitment or relax binding through a polarity-hiding flipper for AMM trades. The latter is explicitly work in progress: a Byzantine flipper can cause incorrect execution despite penalties, and Q&A challenges whether its incentive compensation matches the attack payoff.

## Relevance to us

Separates honest-majority ordering guarantees from coalition-resistant incentives. Direct warning against treating encryption or decentralized receipt ordering as sufficient when committee members can collude. Complements [[felten-2022-l2]] and [[drake-2022-tackling]].

## Reading notes

Read the entire timestamped transcript retrieved with yt_transcript.sh (Apify fallback). Automatic captions contain transcription errors; numerical claims below are attributed to the speaker, not independently replicated. 
