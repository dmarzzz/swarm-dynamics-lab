---
id: luceri-2023-leveraging
type: paper
title: Leveraging Large Language Models to Detect Influence Campaigns in Social Media
authors:
- Luca Luceri
- Eric Boniardi
- Emilio Ferrara
year: 2023
venue: arXiv preprint (WWW '24 Companion)
url: https://arxiv.org/abs/2311.07816
doi: null
arxiv: '2311.07816'
cite: Luceri, L., Boniardi, E., & Ferrara, E. (2023). Leveraging Large Language Models to Detect Influence Campaigns in Social Media. arXiv preprint arXiv:2311.07816.
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Converts user metadata and network structure into text and feeds it to an LLM to detect accounts in influence campaigns, so the same detector handles multilingual content and changing tactics. The authors report superior performance on several datasets.

## Contribution

Early use of an LLM as the classifier for influence-campaign accounts, using serialised metadata and network context rather than post text alone.

## Key results

- Reported superior performance across multiple datasets (abstract; numbers not recorded).

## Methods and models

LLM classification over textualised user metadata and network features. Abstract-level read.

## Limitations and open questions

LLM-as-judge detectors are themselves attackable ([[orenstein-2026-breaking]]); few details at abstract level.

## Relevance to us

Option for a swarm detector front end. Same group as [[luceri-2024-unmasking]] and [[ezzeddine-2022-exposing]].
