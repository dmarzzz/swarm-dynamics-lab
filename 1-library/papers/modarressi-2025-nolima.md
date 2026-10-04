---
id: modarressi-2025-nolima
type: paper
title: 'NoLiMa: Long-Context Evaluation Beyond Literal Matching'
authors:
- Ali Modarressi
- Hanieh Deilamsalehy
- Franck Dernoncourt
- Trung Bui
- Ryan A. Rossi
- Seunghyun Yoon
- Hinrich Schütze
year: 2025
arxiv: '2502.05167'
doi: null
url: https://arxiv.org/abs/2502.05167
venue: arXiv
cite: 'Ali Modarressi; Hanieh Deilamsalehy; Franck Dernoncourt; Trung Bui; Ryan A. Rossi; Seunghyun Yoon; Hinrich Schütze (2025). NoLiMa: Long-Context Evaluation Beyond Literal Matching. arXiv:2502.05167.'
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

NoLiMa tests retrieval with minimal lexical overlap between questions and relevant facts. This reduces straightforward string matching as a shortcut and reveals substantial degradation when the same kinds of associations must be recovered from longer inputs.

## Contribution

Needle retrieval requiring latent associations rather than direct word overlap.

## Key results

At 32K tokens, 11 of 13 models fall below half their short-context baselines, according to the abstract.

## Methods and models

Assessment based on the source sections specified below; no implementation was run.

## Limitations and open questions

Abstract only, version 3; ICML 2025 acceptance noted. Retrieval transfer to multi-agent memory is a proposed comparison, not a result.

## Relevance to us

Helps separate exact-copy recall from semantic recovery in SOC-21 and SOC-23; related [[chroma-2025-context]].
