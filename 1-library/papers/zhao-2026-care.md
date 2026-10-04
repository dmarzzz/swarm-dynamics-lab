---
id: zhao-2026-care
type: paper
title: 'CARE: Confounder-Aware Aggregation for Reliable LLM Evaluation'
authors: ['Jitian Zhao', 'Changho Shin', 'Tzu-Heng Huang', 'Satya Sai Srinath Namburi GNVV', 'Frederic Sala']
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2603.00039
doi: null
arxiv: '2603.00039'
cite: 'Zhao, J., Shin, C., Huang, T.-H., Namburi GNVV, S. S. S., & Sala, F. (2026). CARE: Confounder-Aware Aggregation for Reliable LLM Evaluation. arXiv:2603.00039.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Models LLM judge scores as a latent true-quality signal plus shared confounders (verbosity, style, training artefacts) that make majority vote or averaging give little gain or amplify systematic error. CARE separates quality from confounders without labels, with identifiability and finite-sample guarantees, and reduces aggregation error by up to 26.8% across 12 benchmarks. Code: github.com/SprocketLab/CARE (not opened).

## Contribution

A latent-confounder model of correlated judge errors with label-free recovery.

## Key results

- Numbers as given in the summary, taken from the arXiv abstract (not checked against the full text).

## Methods and models

Abstract-level read of the arXiv export record on 2026-10-03; methods not read.

## Limitations and open questions

Abstract only. Found in the correlated-errors / ensemble-aggregation search rounds run for the llm-agent-swarms survey review (item D12).

## Relevance to us

Aggregation-side remedy for correlated errors, beside [[ai-2025-beyond]] and [[onofri-2026-raim]].
