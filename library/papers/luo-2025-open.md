---
id: luo-2025-open
type: paper
title: "Open CaptchaWorld: A Comprehensive Web-based Platform for Testing and Benchmarking Multimodal LLM Agents"
authors: ["Yaxin Luo", "Zhaoyi Li", "Jiacheng Liu", "Jiacheng Cui", "Xiaohan Zhao", "Zhiqiang Shen"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2505.24878
doi: "10.48550/arXiv.2505.24878"
arxiv: "2505.24878"
cite: "Luo, Y., Li, Z., Liu, J., Cui, J., Zhao, X., & Shen, Z. (2025). Open CaptchaWorld: A Comprehensive Web-based Platform for Testing and Benchmarking Multimodal LLM Agents. arXiv preprint arXiv:2505.24878."
topics: ["swarm-detection", "sybil-resistance", "llm-agent-swarms"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: "17 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Luo, Li, Liu, Cui, Zhao and Shen built Open CaptchaWorld, a web platform of 225 interactive CAPTCHAs across 20 modern types, each annotated with a 'CAPTCHA Reasoning Depth' that counts the cognitive and motor steps needed. Humans score 93.3%; the best multimodal agent tested (Browser-Use with OpenAI o3) reaches 40.0%.

## Contribution

First web-based interactive benchmark for agent CAPTCHA solving; the baseline cited by the 2026 CAPTCHA-vs-agent papers.

## Key results

- Measured (abstract): humans 93.3% vs best agent 40.0% (Browser-Use + o3), mid-2025.
- Benchmark (abstract): 20 CAPTCHA types, 225 instances.

## Methods and models

Web platform, agents interact through browsers; reasoning-depth metric. Abstract only.

## Limitations and open questions

Abstract only. Snapshot: [[liu-2026-next-gen]] (same group) reports pass rates as high as 90% on some puzzles with late-2025 models.

## Relevance to us

A measured human-agent gap in mid-2025 that closed within months; use it as a dated baseline, not a stable separator.
