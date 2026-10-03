---
id: li-2025-steering
type: paper
title: "Steering LLM Thinking with Budget Guidance"
authors:
- Junyan Li
- Wenshuo Zhao
- Yang Zhang
- Chuang Gan
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2506.13752
doi: null
arxiv: '2506.13752'
cite: "Li, J., Zhao, W., Zhang, Y., & Gan, C. (2025). Steering LLM Thinking with Budget Guidance. arXiv preprint arXiv:2506.13752."
topics:
- agent-budgets
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: 34 (Semantic Scholar, 2026-10-03)
code: []
---
## Summary

Controls reasoning length without fine-tuning the LLM. A small predictor estimates, at each decoding step, a Gamma distribution over how many thinking tokens remain; that estimate steers token-level generation softly so the trace ends near a target budget. Reported in the abstract: up to a 26% accuracy gain on MATH-500 under tight budgets compared with baseline methods, and accuracy competitive with the full-thinking model while using 63% of its thinking tokens. The authors also report that the method transfers to other task domains and that the predictor can estimate question difficulty.

## Contribution

A decode-time, training-free alternative to prompt-stated budgets ([[han-2024-token]]) and hard truncation ([[muennighoff-2025-s1]]): the model is nudged toward a budget by a learned estimate of remaining length.

## Key results

- Measured (abstract): up to +26% accuracy on MATH-500 under tight budgets versus baselines.
- Measured (abstract): competitive accuracy at 63% of the full-thinking model's thinking tokens.
- Claimed (abstract): generalises to broader domains; emergent difficulty estimation.

## Methods and models

Lightweight remaining-length predictor modelling a Gamma distribution, used as a soft guidance signal during decoding. Models not checked at abstract depth.

## Limitations and open questions

Abstract-level read. Requires access to decoding (logits), so it does not apply to closed API models. Single-turn reasoning only.

## Relevance to us

Background for agent budgets: it addresses reasoning length, not tool calls or money. Surveyed area: [[alomrani-2025-reasoning]]. Contrast with model-visible countdowns in [[wen-2025-budgetthinker]] and [[anthropic-2026-task]].
