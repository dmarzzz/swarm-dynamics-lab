---
id: wang-2025-cognition
type: paper
title: "COGNITION: From Evaluation to Defense against Multimodal LLM CAPTCHA Solvers"
authors: ["Junyu Wang", "Changjia Zhu", "Yuanbo Zhou", "Lingyao Li", "Xu He", "Mingkui Wei", "Junjie Xiong"]
year: 2025
venue: "USENIX Security Symposium 2026 (accepted; arXiv preprint)"
url: https://arxiv.org/abs/2512.02318
doi: "10.48550/arXiv.2512.02318"
arxiv: "2512.02318"
cite: "Wang, J., Zhu, C., Zhou, Y., Li, L., He, X., Wei, M., & Xiong, J. (2025). COGNITION: From Evaluation to Defense against Multimodal LLM CAPTCHA Solvers. Accepted at USENIX Security 2026. arXiv preprint arXiv:2512.02318."
topics: ["swarm-detection", "sybil-resistance"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "4 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Wang, Zhu, Zhou, Li, He, Wei and Xiong evaluate 7 multimodal LLMs on 18 real-world CAPTCHA types, measuring single-shot accuracy, success with limited retries, latency and cost per solve, with an adaptive attacker and prompt or few-shot variants. MLLMs reliably solve recognition and low-interaction CAPTCHAs at human-like cost and latency; tasks needing fine-grained localisation, multi-step spatial reasoning or cross-frame consistency remain hard. Hardening one vulnerable type with localisation and implicit counting drops state-of-the-art success from over 95% to 0%.

## Contribution

Systematic cost-and-latency view of MLLM CAPTCHA solving plus defence guidelines validated on one hardened type.

## Key results

- Measured (abstract): 7 MLLMs x 18 CAPTCHA types.
- Measured (abstract): recognition-oriented CAPTCHAs solved at human-like cost and latency.
- Measured (abstract): hardened CAPTCHA reduces SOTA success from over 95% to 0%.

## Methods and models

Benchmarking with retries, latency and cost; reasoning-trace analysis; proof-of-concept hardening. Code on Zenodo (10.5281/zenodo.20406852). Abstract only.

## Limitations and open questions

Abstract only; hardening tested on one type, likely to be overtaken by newer models.

## Relevance to us

Gives per-solve cost for MLLM solvers, which sets the per-identity price of passing CAPTCHAs for an agent swarm. Compare solver-service prices in [[ousat-2026-broken]].
