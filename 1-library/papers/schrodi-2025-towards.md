---
id: schrodi-2025-towards
type: paper
title: "Towards Understanding Subliminal Learning: When and How Hidden Biases Transfer"
authors: ["Simon Schrodi", "Elias Kempf", "Fazl Barez", "Thomas Brox"]
year: 2025
venue: "arXiv preprint (listed as ICLR 2026 in the arXiv comment)"
url: https://arxiv.org/abs/2509.23886
doi: null
arxiv: "2509.23886"
cite: "Schrodi, S., Kempf, E., Barez, F., & Brox, T. (2025). Towards Understanding Subliminal Learning: When and How Hidden Biases Transfer. arXiv preprint arXiv:2509.23886. ICLR 2026."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "30 (Semantic Scholar, via Subliminal Learning citation list, 2026-10-03)"
code: []
---

## Summary

Controlled experiments and mechanistic analysis of when subliminal learning happens under hard distillation (student sees only sampled tokens). Transfer does not require global token entanglement or logit leakage; it is carried by a small set of 'divergence tokens', positions where teachers with different biases would predict different tokens. Masking these tokens mostly removes the transfer. Early layers are critical, and fine-tuning a single early layer suffices. Transfer is fragile: small changes such as paraphrasing the prompts usually suppress it.

## Contribution

Turns subliminal learning from a black-box observation into a localised mechanism with a cheap mitigation.

## Key results

- Abstract-level: masking divergence tokens mostly removes hidden bias transfer.
- Abstract-level: fine-tuning one early layer is sufficient for subliminal learning.
- Abstract-level: prompt paraphrasing usually suppresses transfer.

## Methods and models

Teacher-student distillation with controlled biases; token-level and layer-level ablations (details not read).

## Limitations and open questions

Abstract only. Fragility to paraphrasing is measured for their setups; [[cloud-2025-subliminal]] and later work report transmission through code and chain-of-thought.

## Relevance to us

Q2 and Q3 defence. Paraphrasing a returning sub-agent's outputs through a different model before the parent trains on them is a concrete, cheap merge-time filter suggested by this result. Related: [[cloud-2025-subliminal]], [[blank-2026-subliminal]].
