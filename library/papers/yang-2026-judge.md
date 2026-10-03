---
id: yang-2026-judge
type: paper
title: 'When the Judge Changes, So Does the Measurement: Auditing LLM-as-Judge Reliability'
authors: ['Zongyou Yang', 'Yinghan Hou', 'Xiaokun Yang']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2607.08535
doi: null
arxiv: '2607.08535'
cite: 'Yang, Z., Hou, Y., & Yang, X. (2026). When the Judge Changes, So Does the Measurement: Auditing LLM-as-Judge Reliability. arXiv:2607.08535.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 1
citations: null
code: []
---

## Summary

Across four judgment datasets, compares scaling Qwen3 judges (1.7B to 32B) with moving across MiniMax API releases; judge upgrades are not interchangeable, stronger judges reduce but do not remove position and verbosity bias, repeated-sample juries add little when errors are correlated, and debate shifts decisions in ways that cannot be attributed without protocol logs.

## Contribution

A measurement-validity audit of judges including correlated-error juries.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Background; supports reporting error-dependence estimates for any panel or board.
