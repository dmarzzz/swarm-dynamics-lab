---
id: kuai-2026-statistical
type: paper
title: 'A Statistical Framework for Auditing Behavioral Dependence and Induced Bias in LLM Judges'
authors: ['Chenchen Kuai', 'Jiwan Jiang', 'Zihao Zhu', 'Hao Wang', 'Keshu Wu', 'Zihao Li', 'Yunlong Zhang', 'Chenxi Liu', 'Zhengzhong Tu', 'Zhiwen Fan', 'et al.']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2604.07650
doi: null
arxiv: '2604.07650'
cite: 'Kuai, C., Jiang, J., Zhu, Z., Wang, H., Wu, K., Li, Z., Zhang, Y., Liu, C., Tu, Z., Fan, Z., et al. (2026). A Statistical Framework for Auditing Behavioral Dependence and Induced Bias in LLM Judges. arXiv:2604.07650.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Audits behavioural entanglement among 18 black-box LLMs from six families with a difficulty-weighted entanglement index (synchronised failures on easy items) and a cumulative information gain metric (directional alignment of errors). Entanglement correlates with judge over-endorsement on MMLU-Pro (rho about 0.51) and transfers to MATH-500 (rho about 0.45); de-entangled verifier reweighting gains 3.5 points accuracy over majority voting.

## Contribution

Metrics for hidden dependence between nominally different models.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Supports measuring dependence before crediting a multi-model board with independent evidence.
