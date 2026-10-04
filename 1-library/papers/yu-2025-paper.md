---
id: yu-2025-paper
type: paper
title: Is Your Paper Being Reviewed by an LLM? Benchmarking AI Text Detection in Peer
  Review
authors:
- Sungduk Yu
- Man Luo
- Avinash Madasu
- Vasudev Lal
- Phillip Howard
year: 2025
venue: arXiv
url: https://export.arxiv.org/api/query?id_list=2502.19614
doi: null
arxiv: '2502.19614'
cite: Sungduk Yu; Man Luo; Avinash Madasu; Vasudev Lal; Phillip Howard. (2025). Is
  Your Paper Being Reviewed by an LLM? Benchmarking AI Text Detection in Peer Review.
  arXiv:2502.19614.
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

The authors introduce paired AI and human peer reviews to benchmark eighteen detection algorithms. Their abstract describes 788,984 AI-written reviews spanning eight years at ICLR and NeurIPS, a manuscript-aware Anchor detector, and sensitivity analysis for LLM-assisted editing of human reviews.

## Contribution

Builds a benchmark of 788,984 AI-written peer reviews from ICLR and NeurIPS and evaluates eighteen detectors plus a manuscript-aware Anchor method.

## Key results

- 788,984 AI-written reviews; eight years at two conferences; eighteen detection algorithms evaluated.

## Methods and models

Paired peer-review benchmark, eighteen detectors, and manuscript-context-aware Anchor detection.

## Limitations and open questions

Detection of fully generated reviews should not be equated with detection of editorial assistance; exact operating-point performance is not given in the abstract.

## Relevance to us

The largest paired human/AI text benchmark in the library; useful if we test whether text detectors can flag agent-written content at all.

## Access provenance

Opened the HTTPS arXiv export record and read its abstract on 2026-10-03. No citation count inferred from an absent or mismatched index record.
