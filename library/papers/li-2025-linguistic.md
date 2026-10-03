---
id: li-2025-linguistic
type: paper
title: "Linguistic Differences Between AI and Human Comments in Weibo: Detect AI-Generated Text Through Stylometric Features"
authors: [Ziqi Li, Qi Zhang]
year: 2025
venue: "Chinese Computational Linguistics (CCL 2025), Lecture Notes in Computer Science, Springer"
url: https://link.springer.com/chapter/10.1007/978-981-95-2725-0_3
doi: 10.1007/978-981-95-2725-0_3
arxiv: null
cite: "Li, Z., & Zhang, Q. (2025). Linguistic Differences Between AI and Human Comments in Weibo: Detect AI-Generated Text Through Stylometric Features. In Chinese Computational Linguistics, Lecture Notes in Computer Science, pp. 31-42. Springer. https://doi.org/10.1007/978-981-95-2725-0_3"
topics: [swarm-detection]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "2 (Crossref, 2026-10-03)"
code: []
---

## Summary

Detection of AI-generated short comments on Weibo, framed around "LLM-Bots" (LLM-enhanced social bots). Per the abstract: they build a dataset of 463,382 Weibo comments meant to capture real interactions between LLM-bots and human users (not purely synthetic), design a stylometric feature set for Chinese social media, compare human and AI comments on those features, and train a lightweight stylometric-feature self-attention classifier (SFSC) that reaches F1 = 91.8% on short Chinese comments at low compute cost, with feature-importance analysis for interpretability. Only the abstract was read; how the AI-written comments were identified in the real-world data is not stated there and is the key question.

## Contribution

A real-platform (rather than synthetic) dataset and an interpretable, cheap text-level detector for short AI-written comments in Chinese.

## Key results

- 463,382 Weibo comments dataset (abstract).
- SFSC F1 of 91.8% on short AI-generated comments (abstract).

## Methods and models

Hand-designed stylometric features for Chinese, self-attention over feature vectors, feature-importance analysis.

## Limitations and open questions

Not assessed beyond the abstract. Ground-truth labelling of AI comments in real data is unexplained in the abstract; text-level detectors of this kind are generally expected to degrade on newer models and under paraphrase (our expectation, not tested here).

## Relevance to us

Content-level complement to behaviour-level swarm detection. For agent swarms, per-message stylometry is likely the weakest signal; coordination and timing evidence ([[pacheco-2021-uncovering]], [[li-2025-temporal]]) is harder to evade. Real-world LLM botnet for contrast: [[yang-2023-anatomy]].
