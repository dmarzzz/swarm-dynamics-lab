---
id: ellis-2026-black
type: paper
title: "Black-Box Inference of LLM Architectural Properties with Restrictive API Access"
authors: ["Christopher Ellis", "Shreyas Chaudhari", "Mei-Yu Wang", "Leighton Barnes", "Giulia Fanti", "José M. F. Moura"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2607.01313
doi: null
arxiv: "2607.01313"
cite: "Ellis, C., Chaudhari, S., Wang, M. Y., Barnes, L., Fanti, G., & Moura, J. M. F. (2026). Black-Box Inference of LLM Architectural Properties with Restrictive API Access. arXiv:2607.01313."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

NightVision estimates hidden dimension, depth and parameter count of an LLM under today's restrictive APIs (single logprob per token, no logit bias). A common-set prompting technique exposes log probabilities for the same output tokens across prompts for spectral analysis, and time-to-first-token measurements help estimate depth and size. On 32 open models it recovers hidden dimension within 23% average relative error (9% for MoE) and depth and size within 53% for models over 3B parameters.

## Contribution

Combines logprob geometry with a timing side channel (TTFT) for architecture inference.

## Key results

- Hidden dimension within 23% average relative error over 32 models; 9% on MoE (abstract).
- Depth and parameter count within 53% for models above 3B (abstract).

## Methods and models

Common-set prompting, spectral analysis of logprobs, TTFT timing.

## Limitations and open questions

Needs logprob access; coarse estimates. Abstract-only reading.

## Relevance to us

Shows timing (TTFT) carries model-size information, a side channel a swarm observer may see. Background to [[finlayson-2024-logits]].
