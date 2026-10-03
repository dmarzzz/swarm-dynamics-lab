---
id: thompson-2024-shocking
type: paper
title: 'A Shocking Amount of the Web is Machine Translated: Insights from Multi-Way Parallelism'
authors:
- Brian Thompson
- Mehak Preet Dhaliwal
- Peter Frisch
- Tobias Domhan
- Marcello Federico
year: 2024
venue: Findings of ACL 2024
url: https://arxiv.org/abs/2401.05749
doi: null
arxiv: '2401.05749'
cite: 'Thompson, B., Dhaliwal, M. P., Frisch, P., Domhan, T., & Federico, M. (2024). A Shocking Amount of the Web is Machine Translated: Insights from Multi-Way Parallelism. In Findings of the Association for Computational Linguistics: ACL 2024. arXiv:2401.05749.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 58 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Shows that web content is often translated into many languages at once and that the low quality of these multi-way translations indicates machine translation. Multi-way parallel machine-generated content dominates translations into lower-resource languages and forms a large fraction of all web content in those languages, with a selection bias toward low-quality English content translated en masse.

## Contribution

A structural detector (multi-way parallelism plus quality) for machine-generated web content that needs no text classifier, applied at web scale.

## Key results

- Measured (abstract): multi-way parallel machine translation dominates translations in lower-resource languages and is a large share of their total web content.

## Methods and models

Mining of multi-way parallel sentences from web crawls and quality analysis. Abstract read only.

## Limitations and open questions

Detects machine translation, not LLM generation per se. Abstract depth.

## Relevance to us

Structural redundancy (the same content mirrored across many outlets) as the detection signal, the same idea as near-duplicate clustering in [[hao-2025-do]].
