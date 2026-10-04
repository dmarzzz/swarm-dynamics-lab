---
id: ren-2026-sepal
type: paper
title: 'SEPAL: Separated Expert Pairs with Answer-Level Fusion for Reliable LLM Collaboration'
authors: ['Weijie Ren', 'Yanwen Zhang', 'Hao Li', 'Zhuolin Qi', 'Hengyi Zhang', 'Naibo Wang']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2609.39645
doi: null
arxiv: '2609.39645'
cite: 'Ren, W., Zhang, Y., Li, H., Qi, Z., Zhang, H., & Wang, N. (2026). SEPAL: Separated Expert Pairs with Answer-Level Fusion for Reliable LLM Collaboration. arXiv:2609.39645.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Argues shared discussion couples correction with exposure to the same mistakes and erodes the diversity voting needs. SEPAL keeps three private actor-critic teams (direct reasoning, evidence grounding, verification) separate until a final majority vote over answers only. Across five open-weight backbones and five QA benchmarks it improves mean accuracy by 1.81 points over a matched single actor-critic pair. Code: github.com/zhansan114514/SEPAL (not opened).

## Contribution

Isolation before aggregation as a design against interaction-induced correlation.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Design-side evidence that keeping agents apart until the vote preserves diversity, matching [[bertalanic-2026-cost]] and [[choi-2025-debate]].
