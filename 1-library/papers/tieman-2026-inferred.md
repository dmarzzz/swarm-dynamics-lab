---
id: tieman-2026-inferred
type: paper
title: Inferred Generative-Process Diversity Predicts Correlated Failure Across Language Models
authors:
- Ross Tieman
- Evan Markou
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.03422
doi: null
arxiv: '2609.03422'
cite: 'Tieman, R., & Markou, E. (2026). Inferred Generative-Process Diversity Predicts Correlated Failure Across Language Models. arXiv preprint arXiv:2609.03422.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 0  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

Argues that the diversity that protects multi-model systems is generative-process diversity (differences between the processes that could have produced the outputs), not semantic diversity of outputs. Measures it with Normalised Compression Distance between raw model outputs, residualised against a permutation control. Across 38 language models, this measure finds population structure that semantic similarity misses and predicts cross-task variation in chance-corrected correlated failure across ten benchmark families, beyond semantic similarity and capability (partial rank association -0.216, 95 percent CI -0.309 to -0.122, negative on all ten).

## Contribution

A cheap, output-only diversity measure that predicts which model pairs fail together.

## Key results

- Measured (per abstract): partial rank association between inferred generative-process diversity and correlated failure of -0.216 (CI -0.309 to -0.122), negative on all ten benchmark families.

## Methods and models

Normalised Compression Distance on raw outputs with a permutation control; 38 models; ten benchmark families. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; effect size is moderate.

## Relevance to us

Q2. If a parent wants its k-of-n merge to approximate independence, it needs a way to choose sub-agent configurations that fail differently. This gives a measurable proxy for that choice from outputs alone. Related: [[kim-2025-correlated]], [[chen-2026-when]], [[avizienis-1985-n-version]].
