---
id: jesus-2026-how
type: paper
title: "How Swarms Differ: Challenges in Collective Behaviour Comparison"
authors: ["André Fialho Jesus", "Jonas Kuckling"]
year: 2026
venue: "arXiv preprint (accepted at ANTS 2026)"
url: https://arxiv.org/abs/2602.13016
doi: null
arxiv: "2602.13016"
cite: "Jesus, A. F., & Kuckling, J. (2026). How Swarms Differ: Challenges in Collective Behaviour Comparison. arXiv preprint arXiv:2602.13016 (ANTS 2026)."
topics: [swarm-robotics, criticality-measurement, meta]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (OpenAlex W7129091117, 2026-10-03); 1 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Automatic swarm design and imitation learning need numerical features and similarity measures to compare collective behaviours, but feature sets are usually ad hoc and context-specific. The authors collect feature sets and similarity measures from prior swarm-robotics work, test their robustness outside their original contexts, show that the interplay of features and similarity measures decides which behaviours can be distinguished, and propose a self-organising-map method to find regions of feature space where behaviours are hard to tell apart.

## Contribution

A methodological check on how swarm behaviours are measured and compared. That matters for behaviour discovery ([[mattson-2025-discovery]]) and for any hackathon metric.

## Key results

- Some feature-set and similarity-measure combinations separate behaviour groups better than others (claimed in abstract).
- A SOM-based map of indistinguishable regions.

## Methods and models

Comparative study of feature sets and similarity measures from prior swarm work, plus self-organising maps.

## Limitations and open questions

Abstract-depth entry. The behaviour library is limited to prior swarm-robotics contexts.

## Relevance to us

Directly relevant to choosing metrics for the hackathon's experiments. See also [[kuckling-2023-recent]].
