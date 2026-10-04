---
id: bertalanic-2026-cost
type: paper
title: 'The Cost of Consensus: Isolated Self-Correction Prevails Over Unguided Homogeneous Multi-Agent Debate'
authors: ['Blaž Bertalanič', 'Carolina Fortuna']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2605.00914
doi: null
arxiv: '2605.00914'
cite: 'Bertalanič, B., & Fortuna, C. (2026). The Cost of Consensus: Isolated Self-Correction Prevails Over Unguided Homogeneous Multi-Agent Debate. arXiv:2605.00914.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Teams of N = 10 homogeneous agents (Qwen2.5-7B, Llama-3.1-8B, Ministral-3-8B) debate for 3 rounds on GSM-Hard and MMLU-Hard, against isolated self-correction and a noise control that injects rationales from unrelated problems. Debate failure splits into sycophantic conformity (modal adoption up to 85.5%), contextual fragility (correct reasoning destabilised, up to 70.0%) and consensus collapse (plurality voting discards correct answers present in the pool, oracle gap up to 32.3 points). Conformity is already high at K = 2 peers and grows with initial diversity; debate costs 2.1 to 3.4 times the tokens of self-correction for equal or lower accuracy.

## Contribution

Same authors as [[bertalanic-2026-ringelmann]]; a failure decomposition of homogeneous debate at fixed N = 10.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Same group as the Ringelmann paper, so not an independent replication of the ceiling; useful for its failure pathways and the noise control.
