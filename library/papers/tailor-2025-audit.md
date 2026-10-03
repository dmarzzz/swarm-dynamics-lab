---
id: tailor-2025-audit
type: paper
title: 'Audit the Whisper: Detecting Steganographic Collusion in Multi-Agent LLMs'
authors:
- Om Tailor
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2510.04303
doi: null
arxiv: '2510.04303'
cite: 'Tailor, O. (2025). Audit the Whisper: Detecting Steganographic Collusion in Multi-Agent LLMs. arXiv preprint arXiv:2510.04303.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 10 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Detection framework for covert coordination among LLM agents in markets, allocation and governance workflows. It includes a channel-capacity analysis showing how paraphrase, rate limiting and role permutation reduce covert capacity (measured with paired-run KL diagnostics, with finite-sample guarantees); ColludeBench-v0 covering pricing, first-price auctions, peer review and hosted Gemini and Groq APIs with configurable covert schemes; and an auditing pipeline that fuses cross-run mutual information, permutation invariance, watermark variance and fairness-aware acceptance bias, each tuned to a 10^-3 false-positive budget and validated on 10k honest runs plus an e-value martingale.

## Contribution

A detection-side counterpart to [[motwani-2024-secret]] with a benchmark and calibrated false-positive control.

## Key results

- Reported in abstract: the union meta-test reaches state-of-the-art power at fixed FPR across ColludeBench and external suites (Secret Collusion, CASE, Perfect Collusion Benchmark, SentinelAgent); fairness-driven colluders are invisible to mutual information alone.

## Methods and models

Information-theoretic capacity bounds, interventions (paraphrase, rate limit, role permutation), multi-signal auditing with e-values.

## Limitations and open questions

Abstract only; single author; power numbers not checked.

## Relevance to us

Role permutation and rate limiting as capacity penalties are cheap interventions an agent swarm could apply to blunt colluding or Sybil blocs. Related: [[nakamura-2026-colosseum]], [[fish-2024-algorithmic]].
