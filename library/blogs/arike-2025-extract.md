---
id: arike-2025-extract
type: blog
title: Extract-and-Evaluate Monitoring Can Significantly Enhance CoT Monitor Performance
  (Research Note)
authors:
- Rauno Arike
- RohanS
- Shubhorup Biswas
year: 2025
url: https://www.alignmentforum.org/posts/nRcKDYi2KfRTXdvDF/extract-and-evaluate-monitoring-can-significantly-enhance
site: AI Alignment Forum
topics:
- swarm-detection
- fork-merge-security
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: skim
relevance: 4
---

## Summary

This corrected research note separates suspicious-quote extraction from judging whether those quotes depart from the legitimate task. Reusing CoT Red-Handed coding transcripts, the two-stage monitor improves detection, especially for subtle side goals. A stronger judge adds further gains, while missed quote selection remains a bottleneck for long implementations and edge cases.

## Key claims

- At 1% false-positive rate, the two-stage GPT-4.1-mini monitor improves catch rate by 12.0 percentage points overall and 18.2 points for subtle side tasks versus the next-best baseline.
- Using GPT-4.1 as judge increases the reported gains to 27.3 overall and 38.1 subtle-task points.
- The post explicitly corrects bugs in its original version; current numbers should not be confused with the superseded results.

## Evidence quality

Experimental research note reusing the exact successful-attack transcripts of arXiv 2505.23575, not an independent replication. BigCodeBench single-step tasks dominate the evidence. The source discusses filtering bias, extra compute, prompt changes, and limited transfer evidence for longer trajectories.

## Relevance to us

A concrete trace-compression design for supervising many workers, with separate extraction and adjudication failures. Link [[arnav-2025-unfaithful]] for the underlying data and [[hua-2025-optimally]] for cost-aware alternatives.
