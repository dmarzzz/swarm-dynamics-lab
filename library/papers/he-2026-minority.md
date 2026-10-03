---
id: he-2026-minority
type: paper
title: 'Minority Sentinel: When to Overturn Majority Voting in Multi-Agent LLM Debates'
authors: ['Chuan He', 'Zebin Chen', 'Zhengyi Yang', 'Shaobo Qiao', 'Mingchen Ju', 'Jiate Liu', 'Dong Wen', 'Guanfeng Liu']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2606.29270
doi: null
arxiv: '2606.29270'
cite: 'He, C., Chen, Z., Yang, Z., Qiao, S., Ju, M., Liu, J., Wen, D., & Liu, G. (2026). Minority Sentinel: When to Overturn Majority Voting in Multi-Agent LLM Debates. arXiv:2606.29270.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Debates among three heterogeneous LLM agents on six benchmarks show that in roughly one in four divergent cases the minority holds the correct answer, which the authors attribute to correlated errors from shared pretraining breaking the Condorcet independence assumption. That leaves a 10-point theoretical recovery margin. A LightGBM meta-classifier over a debate fingerprint decides when to overturn the majority, with flip precision 81.2%.

## Contribution

Measured minority-truth rate under majority voting in small heterogeneous debates, and a method to recover it.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search round run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Small-N (3 agents) evidence that majority aggregation suppresses correct minorities when errors correlate; context for [[choi-2025-debate]] and [[kaesberg-2025-voting]].
