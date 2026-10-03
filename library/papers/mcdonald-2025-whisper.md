---
id: mcdonald-2025-whisper
type: paper
title: "Whisper Leak: a side-channel attack on Large Language Models"
authors: ["Geoff McDonald", "Jonathan Bar Or"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2511.03675
doi: null
arxiv: "2511.03675"
cite: "McDonald, G., & Or, J. B. (2025). Whisper Leak: a side-channel attack on Large Language Models. arXiv:2511.03675."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Whisper Leak infers user prompt topics from encrypted streaming LLM traffic using packet sizes and timing. Across 28 popular LLMs from major providers it reaches near-perfect classification (often above 98% AUPRC) and high precision at 10,000:1 noise-to-target ratio, with 100% precision for some sensitive topics while recovering 5-20% of target conversations. Random padding, token batching and packet injection each reduce but do not remove the leak.

## Contribution

Industry-scale measurement (Microsoft) of metadata leakage from streaming LLM APIs, with disclosure to providers.

## Key results

- Often above 98% AUPRC across 28 LLMs (abstract).
- 100% precision for sensitive topics such as money laundering at 5-20% recall, 10,000:1 imbalance (abstract).
- No evaluated mitigation gives complete protection (abstract).

## Methods and models

Traffic capture of streaming responses; classifiers on packet size and inter-arrival sequences.

## Limitations and open questions

Topic inference, not model identity; abstract-only reading.

## Relevance to us

A network vantage point (ISP, enterprise proxy) sees enough metadata to classify LLM traffic; extending to "which model and which agent" is shown by [[pouryousef-2026-large]] and [[zhang-2025-exposing]].
