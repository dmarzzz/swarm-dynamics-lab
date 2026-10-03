---
id: iourovitski-2024-hide
type: paper
title: "Hide and Seek: Fingerprinting Large Language Models with Evolutionary Learning"
authors: ["Dmitri Iourovitski", "Sanat Sharma", "Rakshak Talwar"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2408.02871
doi: null
arxiv: "2408.02871"
cite: "Iourovitski, D., Sharma, S., & Talwar, R. (2024). Hide and Seek: Fingerprinting Large Language Models with Evolutionary Learning. arXiv:2408.02871."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "20 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Hide and Seek uses one LLM (Auditor) to generate discriminative prompts and another (Detective) to analyse responses, refining prompts by in-context evolutionary search to fingerprint target models. It reports 72% accuracy at identifying the model family (Llama, Mistral, Gemma and others) among a lineup.

## Contribution

LLM-driven automated probe discovery for black-box fingerprinting.

## Key results

- 72% family-identification accuracy (abstract).

## Methods and models

Auditor-Detective loop with evolutionary prompt refinement.

## Limitations and open questions

Family-level and modest accuracy; abstract-only reading.

## Relevance to us

Automated probe search could adapt honeypot questions to new models without hand design. Stronger hand-designed baseline: [[pasquini-2024-llmmap]].
