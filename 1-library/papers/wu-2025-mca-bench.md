---
id: wu-2025-mca-bench
type: paper
title: "MCA-Bench: A Multimodal Benchmark for Evaluating CAPTCHA Robustness Against VLM-based Attacks"
authors: ["Zonglin Wu", "Yule Xue", "Yaoyao Feng", "Xiaolong Wang", "Yiren Song"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2506.05982
doi: "10.48550/arXiv.2506.05982"
arxiv: "2506.05982"
cite: "Wu, Z., Xue, Y., Feng, Y., Wang, X., & Song, Y. (2025). MCA-Bench: A Multimodal Benchmark for Evaluating CAPTCHA Robustness Against VLM-based Attacks. arXiv preprint arXiv:2506.05982."
topics: ["swarm-detection", "sybil-resistance"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Wu, Xue, Feng, Wang and Song assemble MCA-Bench, a single protocol covering text, image, click, slider and logic CAPTCHAs, and fine-tune a specialised cracking agent per category on a shared vision-language backbone. They map vulnerability across designs, quantify how challenge complexity, interaction depth and model solvability relate, and propose three design principles for hardening.

## Contribution

Unified multimodal benchmark for CAPTCHA robustness against fine-tuned VLM attackers.

## Key results

- Measured (abstract): vulnerability spectrum across modalities; specific success rates not in the abstract.

## Methods and models

Shared VLM backbone, per-category fine-tuned crackers, unified evaluation. Abstract only.

## Limitations and open questions

Abstract only.

## Relevance to us

Background for the CAPTCHA branch; see [[wang-2025-cognition]] for cost and latency numbers.
