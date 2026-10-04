---
id: xu-2025-everything
type: paper
title: 'Everything is Context: Agentic File System Abstraction for Context Engineering'
authors:
- Xiwei Xu
- Robert Mao
- Quan Bai
- Xuewu Gu
- Yechao Li
- Liming Zhu
year: 2025
arxiv: '2512.05470'
doi: null
url: https://arxiv.org/abs/2512.05470
venue: arXiv
cite: 'Xiwei Xu; Robert Mao; Quan Bai; Xuewu Gu; Yechao Li; Liming Zhu (2025). Everything is Context: Agentic File System Abstraction for Context Engineering. arXiv:2512.05470.'
topics:
- llm-agent-swarms
- fork-merge-security
added_by: vishesh/codex-methods
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

The authors propose a file-system abstraction for managing context, including persistent artifacts, metadata and access control. The AIGNE implementation illustrates construction, loading and evaluation of context through a memory agent and a GitHub assistant.

## Contribution

Context Constructor, Loader and Evaluator within AIGNE.

## Key results

Two architectural exemplars are described; the abstract supplies no controlled accuracy comparison.

## Methods and models

Assessment based on the source sections specified below; no implementation was run.

## Limitations and open questions

Abstract only. Uniform storage does not itself establish trustworthy contents or secure permission enforcement.

## Relevance to us

Supports explicit storage-layer comparisons in SOC-21 and SEC-07, alongside [[langchain-2026-how]].
