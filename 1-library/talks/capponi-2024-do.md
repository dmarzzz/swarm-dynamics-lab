---
id: capponi-2024-do
type: talk
title: Agostino Capponi - Do Flashbots Relays Mitigate Frontrunning Risk and MEV?
authors:
- Agostino Capponi
year: 2024
url: https://www.youtube.com/watch?v=LCIZo6QVMMI
venue: CyLab
topics:
- sybil-resistance
added_by: shadow/sol-w8
accessed: '2026-10-03'
read_depth: full
relevance: 4
---

## Summary

Capponi models whether private transaction pools actually mitigate frontrunning. At 7:22-10:44 he defines a three-period game with homogeneous profit-maximizing validators, a frontrunnable user, other users and two competing arbitrageurs. Private-pool transactions have execution priority, and monitored private pools are assumed not to frontrun. At 11:39-15:58 a user trades public-pool exploitation risk against private-pool nonexecution risk. Large losses induce full adoption, but smaller losses can sustain partial adoption because validators retain profitable frontrunning competition. At 16:00-18:16 he argues that full adoption improves allocation while validators may require compensation for lost MEV. Q&A explicitly notes that the model does not specify a slippage constraint and assumes homogeneous, risk-neutral participants.

## Relevance to us

Provides a negative mechanism-design result: availability of a protective channel does not ensure equilibrium adoption. The nonfrontrunning and transaction-priority assumptions are essential, not universal properties of Flashbots or Ethereum. This is incentive analysis, not a measured Sybil defense.

## Reading notes

Read the entire timestamped transcript retrieved with yt_transcript.sh (Apify fallback). Automatic captions contain transcription errors; numerical claims below are attributed to the speaker, not independently replicated. 
