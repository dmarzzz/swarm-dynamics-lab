---
id: carlini-2024-remote
type: paper
title: "Remote Timing Attacks on Efficient Language Model Inference"
authors: ["Nicholas Carlini", "Milad Nasr"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2410.17175
doi: null
arxiv: "2410.17175"
cite: "Carlini, N., & Nasr, M. (2024). Remote Timing Attacks on Efficient Language Model Inference. arXiv:2410.17175."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "16 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Shows that efficient inference techniques (speculative decoding and similar) create data-dependent timing that leaks through encrypted traffic. A passive network observer can infer conversation topic on open-source systems with over 90% precision, and on ChatGPT and Claude can distinguish specific messages or infer the user's language. An active adversary can use a boosting attack to recover PII such as phone or card numbers on open-source systems.

## Contribution

Establishes response timing as a remote side channel on LLM services.

## Key results

- Topic inference over 90% precision on open-source systems (abstract).
- Distinguish specific messages and infer language on ChatGPT and Claude (abstract).
- Boosting attack recovers PII on open-source systems (abstract).

## Methods and models

Monitoring encrypted traffic timing between victim and remote LM; experiments on open-source and production systems.

## Limitations and open questions

Aimed at user privacy, not agent identification. Abstract-only reading.

## Relevance to us

Timing channels that leak content probably also leak which model or serving stack an agent uses; [[pouryousef-2026-large]] measures model fingerprinting from traffic directly. Related: [[mcdonald-2025-whisper]].
