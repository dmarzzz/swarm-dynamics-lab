---
id: chen-2026-do
type: paper
title: "Do System Prompts Leave Behavioral Fingerprints? A Large-Scale Empirical Study of Clone Detection via Output Similarity"
authors: ["Linghan Chen", "Yudong Gao", "Jiyao Wang", "Kaiyan Ji", "Honglong Chen"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.24461
doi: null
arxiv: "2608.24461"
cite: "Chen, L., Gao, Y., Wang, J., Ji, K., & Chen, H. (2026). Do System Prompts Leave Behavioral Fingerprints? A Large-Scale Empirical Study of Clone Detection via Output Similarity. arXiv:2608.24461."
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Asks whether a deployment that copied someone's system prompt can be detected from outputs. Black-Box Behavioral Fingerprinting registers an output signature and tests whether a suspect deployment matches it more closely than unrelated baselines. Over 4 model families, 8 benchmarks and 288,000 responses, prompt choice explains 24.4% of output variance and same-model clone detection reaches AUC 0.876; cross-model detection averages 0.725.

## Contribution

Large-scale measurement of how much a system prompt shapes outputs and how detectable a cloned prompt is, the same quantity a same-operator linker relies on.

## Key results

- Prompt choice explains 24.4% of output variance (abstract).
- Same-model clone detection AUC 0.876; cross-model AUC from 0.845 (Claude as detector) to 0.665 (Qwen), mean 0.725.
- Robust to non-adaptive paraphrasing (AUC at least 0.889), but a one-sentence formal-tone prefix collapses detection on short structured outputs (MNLI 0.978 to 0.547).
- Diagnostic Query Optimization adds 0.120 to cross-model AUC.

## Methods and models

Black-box API sampling of responses to benchmark queries under owner and suspect prompts; similarity-based hypothesis test against unrelated baselines.

## Limitations and open questions

Abstract-level reading. A trivial style prefix defeats it on short outputs, which is exactly how an operator would vary bot personas.

## Relevance to us

Quantifies the system-prompt signal that [[white-2026-black]] uses to link scam bots, and shows its main weakness. For swarm detection, prompt-level linking is fragile; model-level and tool-structure signals ([[park-2026-cross]]) may survive better.
