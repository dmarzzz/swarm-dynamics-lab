---
id: hu-2025-fingerprinting
type: paper
title: "Fingerprinting LLMs via Prompt Injection"
authors: ["Yuepeng Hu", "Zhengyuan Jiang", "Mengyuan Li", "Osama Ahmed", "Zhicong Huang", "Cheng Hong", "Neil Gong"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2509.25448
doi: null
arxiv: "2509.25448"
cite: "Hu, Y., Jiang, Z., Li, M., Ahmed, O., Huang, Z., Hong, C., & Gong, N. (2025). Fingerprinting LLMs via Prompt Injection. arXiv:2509.25448."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

LLMPrint builds model-provenance fingerprints by optimising prompt-injection-style fingerprint prompts that enforce consistent token preferences unique to a base model and robust to post-training and quantisation. A unified verification procedure covers gray-box and black-box settings with statistical guarantees. Over five base models and about 700 post-trained or quantised variants it reports high true-positive rates with false positives near zero.

## Contribution

Uses prompt-injection susceptibility as a provenance fingerprint.

## Key results

- High TPR with near-zero FPR over about 700 derivatives of 5 base models (abstract).

## Methods and models

Optimised fingerprint prompts; statistical verification.

## Limitations and open questions

Base-model provenance, not deployment identification; abstract-only reading.

## Relevance to us

Shows injection prompts double as identity probes, as in [[pasquini-2024-llmmap]] and the honeypot of [[reworr-2024-llm]].
