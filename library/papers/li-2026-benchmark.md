---
id: li-2026-benchmark
type: paper
title: A Benchmark and Diagnostic Study of Epistemic Admission in Shared Agent Memory
authors:
- Xiaoyang Li
- Yiqi Wang
- Chencheng Zhu
- KE XU
- Wencheng Yang
- Zequn Sun
- Pingan Song
- Yiqun Duan
- Taotao Cai
year: 2026
venue: arXiv
url: https://arxiv.org/html/2609.30813v1
doi: null
arxiv: '2609.30813'
cite: Li, Xiaoyang; Wang, Yiqi; Zhu, Chencheng; XU, KE; Yang, Wencheng; Sun, Zequn;
  Song, Pingan; Duan, Yiqun; Cai, Taotao. (2026). A Benchmark and Diagnostic Study
  of Epistemic Admission in Shared Agent Memory. arXiv:2609.30813.
topics:
- llm-agent-swarms
- sybil-resistance
- fork-merge-security
added_by: dmarz/preflight
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

CPB compares policies for admitting claims into shared agent memory. Its static component scores authored decisions; its live component measures downstream use in synthetic teams. Rejecting repeated evidence can also discard useful truths.

## Contribution

Connects admission decisions with logged retrieval and consumer answers.

## Key results

Live episodes use six agents over six rounds; results are descriptive.

## Methods and models

Skimmed introduction, methods, results, Figure 1 and Appendix S in v1.

## Limitations and open questions

Input lineage is authored; generated derivation relies on declarations. No compared policy exercises correction. Not deployment prevalence.

## Relevance to us

Closest prior for quorum and recovery; compare [[li-2026-memtx]].
