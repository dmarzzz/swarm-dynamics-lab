---
id: shu-2026-blind
type: paper
title: 'Blind to the Pivotal Vote: Aggregate Independence Metrics Miss Where Verification Actually Helps'
authors: ['Yang Shu']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2608.06940
doi: null
arxiv: '2608.06940'
cite: 'Shu, Y. (2026). Blind to the Pivotal Vote: Aggregate Independence Metrics Miss Where Verification Actually Helps. arXiv:2608.06940.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Starting from the reported nine-judges-two-effective-votes result, adds an execution-based signal (test suites) to code-judging panels. The panel effective-vote count does not change detectably (-0.04, CI -0.10 to +0.02), yet the whole accuracy gain concentrates on one-vote-margin queries (+10.4 to +23.3 points) and is zero elsewhere, across three code benchmarks and four panel sizes.

## Contribution

Shows aggregate n_eff is the wrong statistic for where an independent signal helps; margin-stratified utility is complementary.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search round run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Caution for N_eff experiments: report margin-stratified effects, not only rho or n_eff. Builds on [[kohli-2026-nine]].
