---
id: deng-2024-oedipus
type: paper
title: "Oedipus: LLM-enchanced Reasoning CAPTCHA Solver"
authors: ["Gelei Deng", "Haoran Ou", "Yi Liu", "Jie Zhang", "Tianwei Zhang", "Yang Liu"]
year: 2024
venue: "ACM CCS 2025 (arXiv preprint)"
url: https://arxiv.org/abs/2405.07496
doi: "10.1145/3719027.3744872"
arxiv: "2405.07496"
cite: "Deng, G., Ou, H., Liu, Y., Zhang, J., Zhang, T., & Liu, Y. (2024). Oedipus: LLM-enchanced Reasoning CAPTCHA Solver. arXiv preprint arXiv:2405.07496. Published version DOI 10.1145/3719027.3744872."
topics: ["swarm-detection", "sybil-resistance"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: "34 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Deng, Ou, Liu, Zhang, Zhang and Liu first find that multimodal LLMs struggle with reasoning CAPTCHAs (human-easy, AI-hard puzzles). Oedipus breaks each puzzle into simple, LLM-solvable sub-steps written in a CAPTCHA domain-specific language and solves them with chain-of-thought. It averages 63.5% success and adapts to designs released in late 2023 that were not in the initial study.

## Contribution

Early demonstration that task decomposition lets LLMs solve reasoning CAPTCHAs designed against them.

## Key results

- Measured (abstract): Oedipus 63.5% average success on reasoning CAPTCHAs.
- Measured (abstract): bare MLLMs struggle on the same CAPTCHAs.

## Methods and models

Empirical study of MLLM failure modes, DSL for sub-step generation, CoT execution. Abstract only.

## Limitations and open questions

Abstract only. 2024 models. The published-version DOI 10.1145/3719027.3744872 (ACM CCS 2025 proceedings) was found via Semantic Scholar and its title and authors confirmed on Crossref; I did not open the publisher page.

## Relevance to us

Part of the CAPTCHA-solver line that ends with agent-native solvers ([[chen-2026-captcha]], [[salman-2026-captchas]]).
