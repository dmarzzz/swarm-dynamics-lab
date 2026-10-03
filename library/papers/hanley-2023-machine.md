---
id: hanley-2023-machine
type: paper
title: 'Machine-Made Media: Monitoring the Mobilization of Machine-Generated Articles on Misinformation and Mainstream News Websites'
authors:
- Hans W. A. Hanley
- Zakir Durumeric
year: 2023
venue: ICWSM 2024 (pages 542-556 per Semantic Scholar)
url: https://arxiv.org/abs/2305.09820
doi: null
arxiv: '2305.09820'
cite: 'Hanley, H. W. A., & Durumeric, Z. (2023). Machine-Made Media: Monitoring the Mobilization of Machine-Generated Articles on Misinformation and Mainstream News Websites. In Proceedings of the International AAAI Conference on Web and Social Media (ICWSM 2024), 542-556. arXiv:2305.09820.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 81 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Trains a DeBERTa synthetic-news detector and classifies 15.46 million articles from 3,074 misinformation and mainstream news websites. Between 1 Jan 2022 and 1 May 2023 the relative number of synthetic articles grew 57.3% on mainstream sites and 474% on misinformation sites, driven mostly by small, less popular sites. An interrupted time series shows ChatGPT's release raised synthetic articles on small and misinformation sites but not on large mainstream sites.

## Contribution

Early large-scale measurement of machine-generated news, separating site tiers and showing the uptake concentrates in the long tail and misinformation outlets.

## Key results

- Measured (abstract): +57.3% relative growth of synthetic articles on mainstream sites and +474% on misinformation sites, Jan 2022 to May 2023.
- Measured (abstract): ChatGPT release produced a marked increase on small and misinformation sites; no corresponding increase on large mainstream sites.

## Methods and models

DeBERTa classifier trained on synthetic and human news; 15.46M articles from 3,074 sites; interrupted time-series analysis. Abstract read only.

## Limitations and open questions

Relative growth figures, not absolute shares, in the abstract; detector trained partly on pre-2022 generators. Abstract depth.

## Relevance to us

Shows machine text concentrates in low-reputation, high-volume sources, the same population where content farms and influence networks live. Later newspaper audits: [[russell-2025-ai]], [[ansari-2025-echoes]]; disinformation corpora: [[macko-2025-beyond]].
