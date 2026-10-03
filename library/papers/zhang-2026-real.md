---
id: zhang-2026-real
type: paper
title: "Real Money, Fake Models: Deceptive Model Claims in Shadow APIs"
authors: ["Yage Zhang", "Yukun Jiang", "Zeyuan Chen", "Michael Backes", "Xinyue Shen", "Yang Zhang"]
year: 2026
venue: "ACM Conference on Computer and Communications Security (CCS 2026, accepted); arXiv preprint"
url: https://arxiv.org/abs/2603.01919
doi: null
arxiv: "2603.01919"
cite: "Zhang, Y., Jiang, Y., Chen, Z., Backes, M., Shen, X., & Zhang, Y. (2026). Real Money, Fake Models: Deceptive Model Claims in Shadow APIs. ACM CCS 2026. arXiv:2603.01919."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

First systematic audit of shadow APIs, third-party services claiming access to official frontier models. The authors find 17 shadow APIs used in 187 academic papers (the most popular with over 5,900 citations and 58,000 GitHub stars by December 2025). Auditing three representative services shows performance divergence up to 47.21%, unpredictable safety behaviour, and identity verification failures in 45.83% of fingerprint tests, consistent with deceptive model claims. Four of the 17 providers had shut down by writing.

## Contribution

An in-the-wild measurement where fingerprinting exposes misattributed models at scale.

## Key results

- 17 shadow APIs used in 187 papers (abstract).
- Performance divergence up to 47.21% (abstract).
- Identity verification failures in 45.83% of fingerprint tests (abstract).

## Methods and models

Utility, safety and model-verification audits including fingerprint tests; literature census of shadow-API use.

## Limitations and open questions

Three services audited in depth; abstract-only reading.

## Relevance to us

Real-world evidence that claimed model identity is often false, so swarm attribution should verify rather than trust self-reports (compare banner-grabbing failures in [[pasquini-2024-llmmap]]). Related: [[bruckner-2026-one]].
