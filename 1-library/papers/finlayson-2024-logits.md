---
id: finlayson-2024-logits
type: paper
title: "Logits of API-Protected LLMs Leak Proprietary Information"
authors: ["Matthew Finlayson", "Xiang Ren", "Swabha Swayamdipta"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2403.09539
doi: null
arxiv: "2403.09539"
cite: "Finlayson, M., Ren, X., & Swayamdipta, S. (2024). Logits of API-Protected LLMs Leak Proprietary Information. arXiv:2403.09539."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Exploits the softmax bottleneck: a transformer's logits lie in a low-dimensional linear subspace (the model image), which acts as a signature. With a modest number of API queries (under 1,000 USD for gpt-3.5-turbo) one can obtain full-vocabulary outputs, detect model updates, identify the source LLM from a single full output, and estimate the hidden size, about 4,096 for gpt-3.5-turbo.

## Contribution

A mathematically grounded model signature that identifies the source model from one full-vocabulary output when logit access exists.

## Key results

- Estimated gpt-3.5-turbo embedding size of about 4,096 (abstract).
- Source-model identification from a single full LLM output (abstract).
- Cost under 1,000 USD for gpt-3.5-turbo (abstract).

## Methods and models

Collect logit or logprob vectors via the API, recover the output subspace, test membership.

## Limitations and open questions

Needs logprob or logit-bias access, which most providers have since restricted; [[ellis-2026-black]] shows partial recovery remains possible under restrictive APIs.

## Relevance to us

Strong attribution if a swarm exposes logprobs (rare in the wild). Mostly useful as the high-access reference point against which black-box methods like [[pasquini-2024-llmmap]] are judged.
