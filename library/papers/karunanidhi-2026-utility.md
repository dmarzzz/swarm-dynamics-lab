---
id: karunanidhi-2026-utility
type: paper
title: 'Utility Under Attack: Agent Memory Poisoning and the Limits of Content Screening and Provenance Ranking'
authors: [Arulnidhi Karunanidhi]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.21230
doi: null
arxiv: '2608.21230'
cite: 'Karunanidhi, A. (2026). Utility Under Attack: Agent Memory Poisoning and the Limits of Content Screening and Provenance Ranking. arXiv preprint arXiv:2608.21230.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 1  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

The paper measures how much damage plainly worded false statements do when stored in agent memory, with no instruction, trigger or retriever optimisation, and tests two defence families. Measured (abstract): poisoning 1.2% of a LongMemEval corpus cuts accuracy from 0.850 to 0.300. A four-stage write-time screening pipeline reaches 0.832 recall on indirect prompt injection and flags 1.5% of trigger-word-laden benign text, yet it rejects 0 of 360 poisoned memories. Additive provenance-weighted retrieval at the shipped weight is statistically indistinguishable from no defence (p=0.80). A stronger weight restores utility (0.3167 to 0.7000) only by excluding untrusted content. When the answer-bearing evidence is itself untrusted, recall falls to zero and accuracy to 0.0417. The author argues for bounded occupancy constraints at retrieval instead of additive provenance penalties.

## Contribution

A negative result. Content screening cannot catch false assertions without external grounding, and additive provenance penalties have no setting that both resists poison and keeps legitimate untrusted evidence.

## Key results

- 1.2% poison drops LongMemEval accuracy from 0.850 to 0.300 (abstract).
- A screen with 0.832 injection recall rejects 0 of 360 false-fact poisons (abstract).
- Provenance weight: p=0.80 against no defence at the shipped weight. At a strong weight, untrusted-evidence recall goes to 0 (abstract).

## Methods and models

LongMemEval, one-pass generated false assertions, and harnesses and corpora released per the abstract (not opened).

## Limitations and open questions

Single author, abstract only. Occupancy bounds are proposed but, judging from the abstract, not evaluated.

## Relevance to us

Bears on Q2 and Q3. For Q3, the strongest attack may not be prompt injection at all. Fluent false facts gathered in a hostile information domain pass every injection screen, and a sub-agent sent to explore a foreign web will bring back exactly such content, honestly. For Q2, the result argues against "trust the parent's own memory more than the child's" as a soft weight. The proposed alternative, an occupancy bound on how many retrieved items can come from one origin, is a per-source cap in the same spirit as k-of-n thresholds and complements [[xiang-2024-certifiably]] and [[sharma-2026-smsr]]. Compare [[zou-2024-poisonedrag]] for optimised false facts.
