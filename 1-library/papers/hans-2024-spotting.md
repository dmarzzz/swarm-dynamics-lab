---
id: hans-2024-spotting
type: paper
title: 'Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text'
authors:
- Abhimanyu Hans
- Avi Schwarzschild
- Valeriia Cherepanova
- Hamid Kazemi
- Aniruddha Saha
- Micah Goldblum
- Jonas Geiping
- Tom Goldstein
year: 2024
venue: ICML 2024 (pages 17519-17537 per Semantic Scholar)
url: https://arxiv.org/abs/2401.12070
doi: null
arxiv: '2401.12070'
cite: 'Hans, A., Schwarzschild, A., Cherepanova, V., Kazemi, H., Saha, A., Goldblum, M., Geiping, J., & Goldstein, T. (2024). Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text. In Proceedings of the 41st International Conference on Machine Learning (ICML 2024), 17519-17537. arXiv:2401.12070.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 387 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Binoculars scores text by contrasting two closely related pre-trained LLMs, needing no training data. Across many document types it detects over 90% of ChatGPT and other LLM generations at a 0.01% false-positive rate without ChatGPT-specific training.

## Contribution

Strong zero-shot detector with very low false-positive operating point, widely used in prevalence audits.

## Key results

- Measured (abstract): over 90% detection of generated samples at 0.01% FPR across document types.

## Methods and models

Ratio of perplexity to cross-perplexity between two related LLMs. Abstract read only.

## Limitations and open questions

Lab conditions; vulnerable to paraphrase like other zero-shot detectors ([[dugan-2024-raid]]). Abstract depth.

## Relevance to us

Detector used in [[brooks-2024-rise]] and [[ansari-2025-echoes]]; a low-FPR choice suits lower-bound prevalence designs.
