---
id: kang-2026-whose
type: paper
title: "Whose Agent Are You? Multi-Layer Fingerprinting and Attribution of Autonomous Web Agents"
authors: ["Dayeon Kang", "Hyejun Jeong", "Jade Sheffey", "Pubali Datta", "Amir Houmansadr"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.20910
doi: null
arxiv: "2606.20910"
cite: "Kang, D., Jeong, H., Sheffey, J., Datta, P., & Houmansadr, A. (2026). Whose Agent Are You? Multi-Layer Fingerprinting and Attribution of Autonomous Web Agents. arXiv:2606.20910."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Builds a multi-layer fingerprint from network characteristics (TLS, HTTP) and browser interaction behaviour to distinguish AI web agents from humans and traditional crawlers, deployed as a logging framework on an instrumented domain. Analysing AutoGen, Browser Use, Claude, Gemini, Operator and Skyvern, a decision tree reaches 97% accuracy in isolating agent architectures and separating agent traffic from human and legacy-crawler baselines.

## Contribution

Cross-layer attribution of agent frameworks rather than base models.

## Key results

- 97% accuracy over six agent frameworks plus human and crawler baselines (abstract).

## Methods and models

Instrumented live domain; TLS/HTTP request assembly features plus browser action features; decision tree.

## Limitations and open questions

Framework-level labels; evasion claims rest on cross-layer redundancy, not adaptive attacks. Abstract-only reading.

## Relevance to us

Complements model-level attribution from UI traces ([[lugoloobi-2026-known]]). Overlaps with the web-agents lane; included because it attributes, not only detects.
