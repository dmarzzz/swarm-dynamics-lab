---
id: brooks-2024-rise
type: paper
title: The Rise of AI-Generated Content in Wikipedia
authors:
- Creston Brooks
- Samuel Eggert
- Denis Peskoff
year: 2024
venue: Proceedings of the First Workshop on Advancing NLP for Wikipedia (WikiNLP 2024)
url: https://arxiv.org/abs/2410.08044
doi: 10.18653/v1/2024.wikinlp-1.12
arxiv: '2410.08044'
cite: Brooks, C., Eggert, S., & Peskoff, D. (2024). The Rise of AI-Generated Content in Wikipedia. In Proceedings of the First Workshop on Advancing Natural Language Processing for Wikipedia. https://doi.org/10.18653/v1/2024.wikinlp-1.12. arXiv:2410.08044.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 42 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Runs GPTZero and Binoculars over recently created Wikipedia pages, with thresholds calibrated to a 1% false-positive rate on pre-GPT-3.5 articles. Both detectors flag over 5% of newly created English Wikipedia articles as AI-generated, with lower rates for German, French and Italian. Flagged articles tend to be lower quality and often self-promotional or one-sided on controversial topics.

## Contribution

Clean calibration design (fix FPR on pre-LLM data, read the excess as a lower bound) applied to an encyclopedia, plus evidence that flagged content clusters around promotion and advocacy.

## Key results

- Measured (abstract): over 5% of new English Wikipedia articles flagged at 1% FPR; lower in German, French, Italian.
- Observed (abstract): flagged articles are lower quality and often self-promotional or partisan.

## Methods and models

Two detectors (proprietary GPTZero, open-source Binoculars) with thresholds set on pre-GPT-3.5 pages. Abstract read only.

## Limitations and open questions

Lower bound only; Wikipedia editing and new-page patrol already remove some machine text before it is sampled (not checked). Abstract depth.

## Relevance to us

The self-promotional and partisan skew of flagged pages is the signature of instrumental, possibly coordinated, machine text rather than casual assistance. Same calibration logic as [[hao-2025-do]]. See also [[huang-2025-wikipedia]].
