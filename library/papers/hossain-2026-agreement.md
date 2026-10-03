---
id: hossain-2026-agreement
type: paper
title: 'Agreement Overstates Evidence: Error Dependence in LLM Judge Consensus'
authors: [Elias Hossain, Niloofar Yousefi, Ser-Nam Lim]
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2609.22512
doi: null
arxiv: '2609.22512'
cite: 'Hossain, E., Yousefi, N., & Lim, S.-N. (2026). Agreement Overstates Evidence: Error Dependence in LLM Judge Consensus. arXiv:2609.22512.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Measures error dependence among open-weight and frontier LLM judges. In the main bank of ten judges, mean pairwise error correlation is 0.21, so ten judges carry about as much information as 3.5 independent ones. Dependence is stronger among high-accuracy frontier judges, including across providers. In up to 28% of comparisons, ignoring shared errors produces a significant system difference that disappears once dependence is accounted for. The structure of shared errors (shared by most judges versus concentrated in a subgroup) changes which voting rule is best.

## Contribution

Shows that mean correlation is not a sufficient statistic: the pattern of co-errors matters for aggregation, in line with the all-wrong-rate argument of [[chen-2026-when]].

## Key results

- Mean pairwise error correlation 0.21; effective judges about 3.5 of 10 (measured).
- Up to 28% of significance conclusions flip when dependence is modelled.

## Methods and models

Judge banks of open-weight and frontier models; correlation and effective-number estimates; comparison of voting rules. Abstract-level read.

## Limitations and open questions

Abstract only. No interaction between judges.

## Relevance to us

Fourth independent effective-N measurement; supports measuring the co-error pattern, not just rho, in any N_eff experiment.
