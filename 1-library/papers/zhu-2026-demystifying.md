---
id: zhu-2026-demystifying
type: paper
title: 'Demystifying Multi-Agent Debate: The Role of Confidence and Diversity'
authors: ['Xiaochen Zhu', 'Caiqi Zhang', 'Yizhou Chi', 'Tom Stafford', 'Nigel Collier', 'Andreas Vlachos']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2601.19921
doi: null
arxiv: '2601.19921'
cite: 'Zhu, X., Zhang, C., Chi, Y., Stafford, T., Collier, N., & Vlachos, A. (2026). Demystifying Multi-Agent Debate: The Role of Confidence and Diversity. arXiv:2601.19921.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Starting from the result that homogeneous debate with uniform updates preserves expected correctness, adds a diversity-aware initialisation (a more diverse pool of starting answers) and confidence-modulated updates (agents state calibrated confidence and condition on others confidence). Theory: diversity raises the prior probability that the correct answer is present; confidence modulation gives drift toward truth. Both beat vanilla debate and majority vote across six reasoning QA benchmarks (reported).

## Contribution

Diversity of initial answers and calibrated confidence as the two levers missing from vanilla debate.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Independent support for the diversity lever and a second lever (confidence) beside it; qualifies "diversity is the only lever".
