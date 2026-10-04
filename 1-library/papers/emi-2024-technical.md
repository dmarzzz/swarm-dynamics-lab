---
id: emi-2024-technical
type: paper
title: Technical Report on the Pangram AI-Generated Text Classifier
authors:
- Bradley Emi
- Max Spero
year: 2024
venue: 'arXiv technical report (vendor: Pangram Labs)'
url: https://arxiv.org/abs/2402.14873
doi: null
arxiv: '2402.14873'
cite: Emi, B., & Spero, M. (2024). Technical Report on the Pangram AI-Generated Text Classifier. arXiv:2402.14873.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 44 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Vendor technical report on Pangram Text, a transformer classifier trained with "hard negative mining with synthetic mirrors". Claims over 38 times lower error rates than zero-shot methods and leading commercial detectors on a 10-domain, 8-model benchmark, orders of magnitude lower false-positive rates in high-data domains such as reviews, no bias against non-native English writers, and generalisation to unseen domains and models.

## Contribution

Describes the commercial detector used in several recent prevalence audits; claims should be read as vendor-reported.

## Key results

- Claimed by vendor (abstract): over 38x lower error than compared tools; low FPR on reviews; no non-native bias.

## Methods and models

Supervised classifier with synthetic mirror negatives. Abstract read only.

## Limitations and open questions

Vendor self-evaluation; independent checks needed. Abstract depth.

## Relevance to us

Pangram underpins [[russell-2025-ai]]; its no-bias claim answers [[liang-2023-gpt]] but is unreplicated here.
