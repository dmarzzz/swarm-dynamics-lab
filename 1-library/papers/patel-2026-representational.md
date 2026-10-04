---
id: patel-2026-representational
type: paper
title: 'Representational Collapse in Multi-Agent LLM Committees: Measurement and Diversity-Aware Consensus'
authors: ['Dipkumar Patel']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2604.03809
doi: null
arxiv: '2604.03809'
cite: 'Patel, D. (2026). Representational Collapse in Multi-Agent LLM Committees: Measurement and Diversity-Aware Consensus. arXiv:2604.03809.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Three Qwen2.5-14B agents with different role prompts answer 100 GSM8K questions; embedded chain-of-thought rationales have mean cosine similarity 0.888 and effective rank 2.17 of 3 (representational collapse). A diversity-weighted consensus reaches 87% versus 84% for self-consistency at 26% lower token cost, with 1 to 3 points of run-to-run variance.

## Contribution

An embedding-based measure of how little role prompting decorrelates same-model agents.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Small single study; supports the same-model ceiling of [[bertalanic-2026-ringelmann]] with a representation-level metric.
