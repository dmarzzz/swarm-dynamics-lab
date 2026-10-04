---
id: gray-2024-chatgpt
type: paper
title: 'ChatGPT "contamination": estimating the prevalence of LLMs in the scholarly literature'
authors:
- Andrew Gray
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2403.16887
doi: null
arxiv: '2403.16887'
cite: 'Gray, A. (2024). ChatGPT "contamination": estimating the prevalence of LLMs in the scholarly literature. arXiv:2403.16887.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 81 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Counts keywords that LLMs over-use (for example "intricate", "meticulously", "commendable") across the 2023 scholarly literature indexed by Dimensions and compares with earlier years. Several keywords rise disproportionately, alone and in combination, giving an estimate that at least 60,000 papers (slightly over 1% of all 2023 articles) were LLM-assisted.

## Contribution

An early, simple marker-word lower bound on LLM-assisted scholarly writing; the precursor to the systematic excess-vocabulary method of [[kobak-2024-delving]].

## Key results

- Measured (abstract): at least 60,000 LLM-assisted papers in 2023, slightly over 1% of all articles; stated as a floor.

## Methods and models

Keyword frequency trends in a bibliographic full-text index, with the excess over prior years taken as LLM-assisted. Abstract read only.

## Limitations and open questions

Hand-picked marker words, so the bound depends on which words were chosen and decays once authors learn them ([[geng-2025-human]]). 2023 is early in adoption. Abstract depth.

## Relevance to us

Cheapest prevalence estimator; useful as a baseline when no reference corpus or detector exists. Updated by the same author in [[gray-2025-estimating]].
