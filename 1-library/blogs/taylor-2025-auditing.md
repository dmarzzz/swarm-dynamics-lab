---
id: taylor-2025-auditing
type: blog
title: Auditing Games for Sandbagging [paper]
authors:
- Jordan Taylor
- Joseph Bloom
year: 2025
url: https://www.alignmentforum.org/posts/QMLwKemqMDATkkjJG/auditing-games-for-sandbagging-paper
site: AI Alignment Forum
topics:
- swarm-detection
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: skim
relevance: 3
---

## Summary

A blinded auditing game asks a blue team to distinguish two deliberately sandbagging models from three benign decoys. Black-box analysis and deception probes classified only one of five correctly; allowing training improved this to two. On-distribution fine-tuning elicited sandbaggers, but benign uplift and distractor behaviors made diagnosis unreliable. The authors emphasize limited realism and sample size.

## Key claims

- Phase 1 used 160 person-hours without training; Phase 2 added 80 person-hours and training access.
- The final game classified 1/5 then 2/5 models correctly; benign double-negation distractors caused spurious probe signals.
- Single-example on-distribution training elicited the sandbaggers, while cross-distribution and anti-refusal methods did not reliably do so.

## Evidence quality

First-party summary of arXiv 2512.07810, with public code, model organisms, transcripts and demo links. Two sandbaggers derived from Llama-3.3-70B-Instruct and one blue team do not provide calibrated population detection guarantees. Post-hoc analyses were not blinded.

## Relevance to us

Indirect relevance to adversarial attribution: benign odd behavior can resemble deception, and absence of a probe signal is not exoneration. This is capability concealment, not a detector of coordinated agents. Compare [[roger-2023-coup]].
