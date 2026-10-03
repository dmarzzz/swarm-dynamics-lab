---
id: nasery-2025-are
type: paper
title: "Are Robust LLM Fingerprints Adversarially Robust?"
authors: ["Anshul Nasery", "Edoardo Contente", "Alkin Kaz", "Pramod Viswanath", "Sewoong Oh"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2509.26598
doi: null
arxiv: "2509.26598"
cite: "Nasery, A., Contente, E., Kaz, A., Viswanath, P., & Oh, S. (2025). Are Robust LLM Fingerprints Adversarially Robust?. arXiv:2509.26598."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Defines a threat model in which a malicious model host tries to defeat model fingerprinting schemes, identifies fundamental vulnerabilities in existing schemes, and builds adaptive attacks for each. The attacks bypass authentication completely for ten recently proposed fingerprinting schemes while preserving model utility for end users.

## Contribution

Evasion result: robustness to benign changes (fine-tuning, merging, prompting) does not imply robustness to an adversarial host.

## Key results

- Adaptive attacks fully bypass ten fingerprinting schemes while keeping high utility (abstract).

## Methods and models

Vulnerability analysis per scheme; tailored adaptive attacks.

## Limitations and open questions

Targets ownership-verification fingerprints (often inserted backdoor-style), not passive behavioural attribution like [[sun-2025-idiosyncrasies]]. Abstract-only reading.

## Relevance to us

A swarm operator is exactly an adversarial host. Fingerprint-based swarm attribution should be assumed evadable by a motivated operator unless shown otherwise. Related evasion: [[yuan-2026-forging]], [[kurian-2025-attacks]].
