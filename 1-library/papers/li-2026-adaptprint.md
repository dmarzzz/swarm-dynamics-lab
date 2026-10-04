---
id: li-2026-adaptprint
type: paper
title: "AdaptPrint: Response-Adaptive Fingerprinting of Black-Box LLM Services"
authors: ["Yilin Li", "Yifei Zhang", "Guozhu Meng"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.22213
doi: null
arxiv: "2608.22213"
cite: "Li, Y., Zhang, Y., & Meng, G. (2026). AdaptPrint: Response-Adaptive Fingerprinting of Black-Box LLM Services. arXiv:2608.22213."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

AdaptPrint fingerprints black-box LLM services adaptively instead of with a fixed query set, using three progressive response-consistency probing strategies (direct, continuation and follow-up probing) and similarity matching against candidate models. Among 27 candidate models it reports Top-1, Top-3 and Top-5 accuracy of 80.6%, 90.3% and 92.1%, and robustness to defence strategies and decoding parameters.

## Contribution

Adaptive multi-step probing for services with system prompts and sampling settings that defeat fixed queries.

## Key results

- Top-1 80.6%, Top-3 90.3%, Top-5 92.1% over 27 candidates (abstract).

## Methods and models

Progressive probing (direct, continuation, follow-up) plus candidate similarity matching.

## Limitations and open questions

Abstract-only reading; closed candidate set.

## Relevance to us

An alternative to [[pasquini-2024-llmmap]] when a target deployment hides behind heavy system prompts, as swarm personas typically do.
