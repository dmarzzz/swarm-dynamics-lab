---
id: elgammal-2026-evolution
type: paper
title: "Evolution of Deep Learning Models for Misinformation Detection in Social Media Textual Data: Background, Architectures, Datasets, and Emerging LLM Applications"
authors: [Ziad Elgammal, Reda Alhajj]
year: 2026
venue: Social Science Computer Review
url: https://doi.org/10.1177/08944393261432625
doi: 10.1177/08944393261432625
arxiv: null
cite: "Elgammal, Z., & Alhajj, R. (2026). Evolution of Deep Learning Models for Misinformation Detection in Social Media Textual Data: Background, Architectures, Datasets, and Emerging LLM Applications. Social Science Computer Review. https://doi.org/10.1177/08944393261432625"
topics: [swarm-detection]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: abstract
relevance: 1
citations: null  # Semantic Scholar rate-limited at access time
code: []
---

## Summary

Survey of more than 70 recent papers on LLM-based (mostly transformer-based) misinformation detection in social media text. Findings per the abstract: BERT-family models appear in about 85% of studies, with domain-specific variants such as CT-BERT doing best in specialised settings like COVID-19 misinformation; the authors compare architectures, implementation strategies and reported metrics across domains, analyse seven commonly used datasets for characteristics and limitations, and discuss linguistic nuance, interpretability and ethics. Their conclusion is that reported accuracies are high but cross-domain generalisation and real-time detection remain unsolved, and they recommend more robust evaluation frameworks. Abstract-only read via Crossref.

## Contribution

A consolidated map of the transformer-era misinformation-detection literature, its datasets and its generalisation failures; no new method.

## Key results

- 70+ papers reviewed; BERT-based models in roughly 85%.
- Domain-specific pretrained variants outperform general ones within their domain.
- Seven major datasets characterised; cross-domain generalisation and real-time operation identified as the main gaps.

## Methods and models

Literature survey with architecture and dataset comparison tables (not read).

## Limitations and open questions

Abstract-only. Content-classification focus: it is about whether a text is misinformation, not about who or what produced it or whether producers coordinate. The generalisation gap the authors flag is precisely what adversarially generated content widens.

## Relevance to us

Marginal. Included because it was in the batch; useful only as a pointer to the dataset landscape and to the observation that content classifiers do not generalise across domains, which is one more reason swarm-detection should lean on behavioural and structural signals ([[guo-2026-text]], [[wang-2026-botchf]]) rather than text classification.
