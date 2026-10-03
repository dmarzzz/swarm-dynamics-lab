---
id: liang-2025-widespread
type: paper
title: The Widespread Adoption of Large Language Model-Assisted Writing Across Society
authors:
- Weixin Liang
- Yaohui Zhang
- Mihai Codreanu
- Jiayu Wang
- Hancheng Cao
- James Zou
year: 2025
venue: Patterns 6 (2025)
url: https://arxiv.org/abs/2502.09747
doi: 10.1016/j.patter.2025.101366
arxiv: '2502.09747'
cite: Liang, W., Zhang, Y., Codreanu, M., Wang, J., Cao, H., & Zou, J. (2025). The Widespread Adoption of Large Language Model-Assisted Writing Across Society. Patterns, 6. https://doi.org/10.1016/j.patter.2025.101366. arXiv:2502.09747.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 89 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Uses the same population-level estimator on four non-academic corpora from Jan 2022 to Sep 2024: 687,241 US financial consumer complaints, 537,413 corporate press releases, 304.3 million job postings and 15,919 UN press releases. LLM-assisted text surged after ChatGPT and then plateaued in 2024: about 18% of complaint text, up to 24% of press-release text, just under 10% of job postings at small firms, and nearly 14% of UN press releases.

## Contribution

The broadest measured base rate of LLM-assisted writing outside science, showing that society-wide adoption plateaued by 2024 (or became harder to see).

## Key results

- Measured (abstract): about 18% of consumer complaint text LLM-assisted by late 2024, slightly higher in urban areas.
- Measured (abstract): up to 24% of corporate press-release text; just under 10% of job postings in small firms, higher in younger firms; nearly 14% of UN press releases.
- Observed: growth stabilised in 2024; the authors cannot distinguish saturation from more subtle, harder-to-detect models.

## Methods and models

Distributional mixture estimation per domain and month, as in [[liang-2024-monitoring]]. Abstract read only.

## Limitations and open questions

The plateau is ambiguous: it may be real saturation or detector blindness to newer models, which is exactly the failure mode that matters for adversarial use. Abstract depth.

## Relevance to us

Base rates for non-adversarial LLM writing in high-volume public text streams. A swarm hiding in such streams would be one part of an already 10-25% machine-assisted background, so per-item "is it AI" flags cannot single it out; coordination signals have to carry the weight (see [[hao-2025-do]] for adversarial mail).
