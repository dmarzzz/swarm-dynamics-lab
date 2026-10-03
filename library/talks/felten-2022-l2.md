---
id: felten-2022-l2
type: talk
title: L2 sequencing and MEV - Ed Felten (Arbitrum)
authors:
- Ed Felten
year: 2022
url: https://www.youtube.com/watch?v=qxml80TparY
venue: Flashbots
topics:
- sybil-resistance
added_by: shadow/sol-w8
accessed: '2026-10-03'
read_depth: full
relevance: 5
---

## Summary

Felten explains Arbitrum sequencing and cautions against importing Ethereum L1 assumptions. At 1:01-5:43 the sequencer feed offers subsecond ordering while deterministic execution and later L1 batch publication record its history. At 5:54-9:33 he describes a planned distributed sequencer, not the deployed centralized system: independently reported receipt orders are merged under an honest-supermajority assumption, potentially with threshold encryption. At 9:44-18:23 he prioritizes low mean and variance of latency, resource-aligned fees and opt-in external MEV intermediaries. Q&A at 24:07-26:43 explicitly answers cheap sequencer replacement: committee membership is permissioned and community-selected, with reputational sanctions, not open entry.

## Relevance to us

Directly relevant Sybil boundary: an honest-supermajority guarantee presupposes controlled membership and cannot be interpreted as Sybil resistance by itself. Differing receipt orders are not automatically provable misbehavior. Related architectural framing: [[adler-2022-exploring]].

## Reading notes

Read the entire timestamped transcript retrieved with yt_transcript.sh (Apify fallback). Automatic captions contain transcription errors; numerical claims below are attributed to the speaker, not independently replicated. 
