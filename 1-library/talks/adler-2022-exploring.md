---
id: adler-2022-exploring
type: talk
title: Exploring MEV in the modular blockchain stack - John Adler (Celestia)
authors:
- John Adler
year: 2022
url: https://www.youtube.com/watch?v=lLuHFFbYv0Y
venue: Flashbots
topics:
- sybil-resistance
added_by: shadow/sol-w8
accessed: '2026-10-03'
read_depth: full
relevance: 4
---

## Summary

Adler separates consensus/data availability, settlement and execution to locate where MEV can be extracted. At 4:47-6:38 he labels conservation of MEV an informal observation, not a law, and approximates miner-extractable value by leader-extractable value. At 10:20-13:45, fixed or stake-rotating execution-layer leaders retain local ordering power, whereas first-come-first-served rollup production lets base-layer producers reorder submissions and capture value. At 14:00-17:47 he extends this reasoning to sovereign and settlement-based rollups, noting reorgs as a route for leakage into the data layer. Q&A at 18:19-20:44 motivates pushing MEV upwards to contain disruptions and reduce shared-layer spillovers.

## Relevance to us

Maps adversarial authority to leader selection rather than visible account counts. Useful for deciding whether modular agent subsystems contain corruption or merely shift which layer can manipulate ordering. Architectural argument, not a quantitative security theorem.

## Reading notes

Read the entire timestamped transcript retrieved with yt_transcript.sh (Apify fallback). Automatic captions contain transcription errors; numerical claims below are attributed to the speaker, not independently replicated. 
