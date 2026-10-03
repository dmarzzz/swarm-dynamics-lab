---
id: chen-2026-token
type: paper
title: "Token Counts Are Not Model Lineage: A Frozen-Threshold Holdout Study of Black-Box LLM API Fingerprinting"
authors: ["Bo Chen"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.29930
doi: null
arxiv: "2608.29930"
cite: "Chen, B. (2026). Token Counts Are Not Model Lineage: A Frozen-Threshold Holdout Study of Black-Box LLM API Fingerprinting. arXiv:2608.29930."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Tests whether prompt-token counts returned by OpenAI-compatible endpoints can attribute relay or reseller APIs to a model family. A shift-invariant exact-match score perfectly separates 12 development endpoint pairs (frozen threshold 0.725), but on 12 untouched holdout pairs only 6 are eligible and balanced accuracy is 0.75 with sensitivity 0.50; two same-family pairs fall below threshold. Token counts fingerprint a shared tokenisation stack, not model lineage.

## Contribution

A pre-registered, frozen-threshold holdout study that rejects a tempting cheap attribution signal: a clean negative result.

## Key results

- Development: perfect separation of 12 pairs, frozen threshold 0.725 (abstract).
- Holdout: 6 of 12 pairs eligible; balanced accuracy 0.75, sensitivity 0.50 (95% Wilson 0.15-0.85), specificity 1.00 (0.342-1.00).
- Qwen 3.8 and DeepSeek V4 same-family pairs fall below threshold.
- 4,320 API calls; holdout had 189 non-200 responses and 157 successful responses lacking token usage.

## Methods and models

24 labelled endpoint pairs split into development and holdout; three temporal repeats and 30 controlled texts per pair; validity-gated result contract that separates dissimilarity from missing data.

## Limitations and open questions

Small sample; single author. Shows the measurement-validity problems (missing usage fields, rate limits) any API-side attribution faces.

## Relevance to us

Methodological model for our lane: freeze thresholds, hold out, report ineligible measurements. Cautions against using cheap metadata as lineage proof. Contrast [[bruckner-2026-one]], [[zhang-2026-which]].
