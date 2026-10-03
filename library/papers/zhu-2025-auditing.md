---
id: zhu-2025-auditing
type: paper
title: "Auditing Black-Box LLM APIs with a Rank-Based Uniformity Test"
authors: ["Xiaoyuan Zhu", "Yaowen Ye", "Tianyi Qiu", "Hanlin Zhu", "Sijun Tan", "Ajraf Mannan", "Jonathan Michala", "Raluca Ada Popa", "Willie Neiswanger"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2506.06975
doi: null
arxiv: "2506.06975"
cite: "Zhu, X., Ye, Y., Qiu, T., Zhu, H., Tan, S., Mannan, A., Michala, J., Popa, R. A., & Neiswanger, W. (2025). Auditing Black-Box LLM APIs with a Rank-Based Uniformity Test. arXiv:2506.06975."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "22 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Proposes a rank-based uniformity test that checks whether a black-box LLM API behaves identically to a locally deployed authentic model, using only sampled outputs. The method is query-efficient and avoids query patterns that a provider could detect and route around. It is evaluated against quantisation, harmful fine-tuning, jailbreak prompts and full model substitution, and reports higher statistical power than prior methods under constrained query budgets.

## Contribution

Adds evasion-aware design (no detectable audit pattern) to the model-equality line started by [[gao-2024-model]].

## Key results

- Consistently higher statistical power than prior methods under constrained query budgets across quantisation, harmful fine-tuning, jailbreak and substitution scenarios (abstract; no numbers in the abstract).

## Methods and models

Rank statistics of API outputs relative to samples from a local reference model; uniformity test under the null of equality.

## Limitations and open questions

Needs the authentic model locally. Abstract-only reading.

## Relevance to us

Audit-evasion matters for swarms too: an operator who detects probes can switch models. The idea of probes indistinguishable from normal traffic carries over to covert swarm screening, as in [[white-2026-black]].
