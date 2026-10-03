---
id: chen-2024-are
type: paper
title: Are More LLM Calls All You Need? Towards Scaling Laws of Compound Inference Systems
authors:
- Lingjiao Chen
- Jared Quincy Davis
- Boris Hanin
- Peter Bailis
- Ion Stoica
- Matei Zaharia
- James Zou
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2403.02419
doi: null
arxiv: '2403.02419'
cite: Chen, L., Davis, J. Q., Hanin, B., Bailis, P., Stoica, I., Zaharia, M., & Zou, J. (2024). Are More LLM Calls All You Need? Towards Scaling Laws of Compound Inference Systems. arXiv preprint arXiv:2403.02419.
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 5 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Studies how the number of LM calls affects compound systems that aggregate responses by majority vote (Vote) or by filtering with an LM judge and then voting (Filter-Vote). Surprisingly, performance can first rise and then fall as the number of calls increases. The theory attributes this non-monotonicity to heterogeneous query difficulty within a task: more calls help on easy queries and hurt on hard ones, and a mix produces an interior optimum. This yields an analytical scaling model that, fitted from a small number of samples, predicts Vote and Filter-Vote performance and the optimal number of calls.

## Contribution

An early analytic scaling law for "more agents" via voting, contrasting with the monotone gains reported by [[li-2024-more]]; foundational for later independence-based analyses such as [[fortuna-2026-multi-agent]].

## Key results

- Measured: non-monotone accuracy vs number of calls on several language tasks.
- Theory: easy/hard query mixture explains non-monotonicity; analytical model predicts optimum.

## Methods and models

Vote and Filter-Vote compound systems; theoretical analysis with per-query difficulty; experiments across language tasks (models not checked).

## Limitations and open questions

Abstract-level read; agents do not interact (ensemble only).

## Relevance to us

A baseline null model: any LLM-swarm gain should be compared with simple voting at equal calls. Related: [[tran-2026-single]], [[qian-2025-scaling]].
