---
id: gloaguen-2024-black
type: paper
title: Black-Box Detection of Language Model Watermarks
authors:
- Thibaud Gloaguen
- Nikola Jovanović
- Robin Staab
- Martin Vechev
year: 2024
venue: ICLR 2025
url: https://arxiv.org/abs/2405.20777
doi: null
arxiv: '2405.20777'
cite: Gloaguen, T., Jovanović, N., Staab, R., & Vechev, M. (2024). Black-Box Detection of Language Model Watermarks. In International Conference on Learning Representations (ICLR 2025). arXiv:2405.20777.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 24 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Develops statistical tests that detect, from a limited number of black-box queries, whether an LLM deployment uses any of the three main watermark families, and estimate their parameters. Works across schemes and open models and is validated on real-world APIs, showing current watermarks are more detectable than believed.

## Contribution

Turns watermark presence into something third parties can audit.

## Key results

- Measured (abstract): rigorous black-box tests detect presence and parameters of all three popular watermark families; feasible on real APIs.

## Methods and models

Hypothesis tests on query responses designed per watermark family. Abstract read only.

## Limitations and open questions

Detects watermark use by a model, not watermark in arbitrary found text. Abstract depth.

## Relevance to us

Lets an auditor know which provider outputs carry watermarks before relying on them for population scans; related evasion via key theft [[jovanovic-2024-watermark]].
