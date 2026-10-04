---
id: qian-2026-nous
type: paper
title: 'Nous: An Attempt to Extract and Inject the Cognition Behind Prediction-Market Behavior'
authors: ['Haowei Qian']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2606.13038
doi: null
arxiv: '2606.13038'
cite: 'Qian, H. (2026). Nous: An Attempt to Extract and Inject the Cognition Behind Prediction-Market Behavior. arXiv:2606.13038.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Extracts eight-dimension behavioural profiles from 100 Polymarket wallets (8 of 14 parameters temporally stable, wallets identifiable at 17 to 22% top-1 vs 1% chance) and injects them into LLM agents by prompt. Injection does not measurably transmit the profile: it shows no advantage over a length-matched control and the induced diversity neither lowers ensemble error correlation nor improves Brier score, across temperatures, profile diversity and difficulty. Code and outputs released (github.com/WillChienT/nous-paper, not opened).

## Contribution

A null result for prompt-level persona diversity as a decorrelator.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Against "role prompts decorrelate": contrast [[begin-2026-preference]] (role diversity lowered rho) and [[patel-2026-representational]].
