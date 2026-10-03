---
id: russell-2025-ai
type: paper
title: AI use in American newspapers is widespread, uneven, and rarely disclosed
authors:
- Jenna Russell
- Marzena Karpinska
- Destiny Akinode
- Katherine Thai
- Bradley Emi
- Max Spero
- Mohit Iyyer
year: 2025
venue: ACL (camera ready; pages 14554-14580 per Semantic Scholar)
url: https://arxiv.org/abs/2510.18774
doi: null
arxiv: '2510.18774'
cite: Russell, J., Karpinska, M., Akinode, D., Thai, K., Emi, B., Spero, M., & Iyyer, M. (2025). AI use in American newspapers is widespread, uneven, and rarely disclosed. In Proceedings of the Annual Meeting of the Association for Computational Linguistics, 14554-14580. arXiv:2510.18774.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 22 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Audits 186K articles from online editions of 1.5K American newspapers published in summer 2025 with the Pangram detector: about 9% of new articles are partly or fully AI-generated, more often in small local outlets, in weather and technology topics, and in certain ownership groups. Opinion pieces in the Washington Post, New York Times and Wall Street Journal are 6.4 times more likely to contain AI text than their news articles. A manual audit of 100 flagged articles found only five disclosures.

## Contribution

A 2025 base rate for undisclosed machine text in mainstream journalism, with ownership-group clustering.

## Key results

- Measured (abstract): about 9% of 186K new articles partially or fully AI-generated.
- Measured (abstract): op-eds in three national papers 6.4x more likely to contain AI text than their news articles.
- Measured (abstract): 5 of 100 flagged articles disclosed AI use.

## Methods and models

Pangram classifier ([[emi-2024-technical]]) over newspaper articles and 45K opinion pieces; manual disclosure audit. Abstract read only.

## Limitations and open questions

Relies on one commercial detector's calibration; "partially AI" depends on its segment-level thresholds. Abstract depth.

## Relevance to us

Clustering by ownership group is an operator-level signal: shared tooling or policy across many outlets, which is the media analogue of one operator running many accounts.
