---
id: geng-2024-is
type: paper
title: Is ChatGPT Transforming Academics' Writing Style?
authors:
- Mingmeng Geng
- Roberto Trotta
year: 2024
venue: Next Generation of AI Safety Workshop, ICML 2024 (as cited by Kobak et al.); arXiv preprint
url: https://arxiv.org/abs/2404.08627
doi: null
arxiv: '2404.08627'
cite: Geng, M., & Trotta, R. (2024). Is ChatGPT Transforming Academics' Writing Style?. arXiv:2404.08627.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 41 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Estimates the density of ChatGPT style in about one million arXiv abstracts (May 2018 to Jan 2024) from word-frequency shifts, with a model calibrated on mixtures of real abstracts and abstracts revised by ChatGPT. Uses adaptive word sets including words whose frequency falls. Estimates about 35% of computer-science abstracts are LLM-style, taking GPT-3.5's response to "revise the following sentences" as the baseline.

## Contribution

A word-frequency mixture estimator that uses both increasing and decreasing words and is calibrated on simulated revision, a different reference than [[liang-2024-monitoring]].

## Key results

- Measured (abstract): about 35% LLM-style abstracts in computer science by early 2024 under the stated baseline prompt.

## Methods and models

Statistical analysis of word-frequency change, calibrated and validated on simulated mixtures after a noise analysis. Abstract read only.

## Limitations and open questions

The estimate is relative to one prompt ("revise the following sentences"); a different usage pattern changes the scale. Abstract depth.

## Relevance to us

Another population-level estimator; together with [[kobak-2024-delving]] and [[liang-2024-mapping]] it shows estimates of 13-35% depending on reference assumptions, a useful caution about absolute numbers.
