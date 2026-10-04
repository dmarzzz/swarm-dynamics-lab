---
id: das-2026-identifying
type: paper
title: "Identifying Intelligent Processes via Online Sequential Testing"
authors: ["Aritra Das", "Debayan Gupta"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.26193
doi: null
arxiv: "2609.26193"
cite: "Das, A., & Gupta, D. (2026). Identifying Intelligent Processes via Online Sequential Testing. arXiv:2609.26193."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Treats identifying which LLM one is conversing with (from a known set) as active sequential hypothesis testing. The outer problem chooses which probe environments to build; the authors show that selecting minimum-cost evaluations that distinguish every pair of candidates is exactly weighted set cover, estimated from calibration samples. The inner problem sequentially sends a budget-minimising subset of probes, with bounds on the number of evaluations needed in terms of pairwise distinguishability.

## Contribution

Theory for query-efficient model identification: probe design as set cover plus sequential testing bounds.

## Key results

- Probe selection reduces to weighted set cover; identification cost is bounded by pairwise distinguishability of candidates (abstract; theoretical).

## Methods and models

Formal analysis; one-shot estimation of the cover instance from calibration samples.

## Limitations and open questions

Abstract-only reading; empirical scale not known.

## Relevance to us

Gives a principled way to minimise probes per suspect account, which matters when screening thousands of swarm members. Practical counterparts: [[pasquini-2024-llmmap]], [[kurian-2025-attacks]].
