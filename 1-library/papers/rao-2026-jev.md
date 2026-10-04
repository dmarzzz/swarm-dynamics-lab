---
id: rao-2026-jev
type: paper
title: 'JEV vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places'
authors: ['Delip Rao', 'Chris Callison-Burch']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2609.29769
doi: null
arxiv: '2609.29769'
cite: 'Rao, D., & Callison-Burch, C. (2026). JEV vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places. arXiv:2609.29769.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Compares a calibrated classifier-style decision model (Jev) with three flash-tier LLM judges on nine panels from seven benchmarks with human judgments. Accuracy differs significantly in at most 8 of 27 paired comparisons per setup, but the judges err alike: on Jev most confident errors about 96% of LLM verdicts repeat its wrong answer where independence predicts about half, and cascades with oracle thresholds never beat the best single judge by more than 2.7 points.

## Contribution

Shows that even architecturally different judges share errors, so cascades and panels add little accuracy.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Further independent evidence for the homogeneity ceiling, including across model types; compare [[kohli-2026-nine]].
