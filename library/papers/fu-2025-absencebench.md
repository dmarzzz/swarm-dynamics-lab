---
id: fu-2025-absencebench
type: paper
title: 'AbsenceBench: Language Models Can''t Tell What''s Missing'
authors:
- Harvey Yiyun Fu
- Aryan Shrivastava
- Jared Moore
- Peter West
- Chenhao Tan
- Ari Holtzman
year: 2025
arxiv: '2506.11440'
doi: null
url: https://arxiv.org/abs/2506.11440
venue: arXiv
cite: 'Harvey Yiyun Fu; Aryan Shrivastava; Jared Moore; Peter West; Chenhao Tan; Ari Holtzman (2025). AbsenceBench: Language Models Can''t Tell What''s Missing. arXiv:2506.11440.'
topics:
- llm-agent-swarms
- criticality-measurement
added_by: vishesh/codex-methods
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

AbsenceBench tests whether models identify deleted material when both original and edited contexts are supplied. It covers numerical sequences, poetry and pull requests, demonstrating that successful retrieval does not imply successful detection of missing information.

## Contribution

Controlled omissions across three document domains.

## Key results

The abstract reports 69.6% F1 for Claude-3.7-Sonnet at an average context length of about 5K tokens.

## Methods and models

Assessment based on the source sections specified below; no implementation was run.

## Limitations and open questions

Abstract only. Its original-document access differs from incomplete logs without a reference. The proposed attention explanation is an interpretation, not established here.

## Relevance to us

Direct benchmark lead for SOC-08, SOC-23 and SOC-32; explicitly vary availability of the original record.
