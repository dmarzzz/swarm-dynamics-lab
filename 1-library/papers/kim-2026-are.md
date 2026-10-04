---
id: kim-2026-are
type: paper
title: Are Diversity Metrics Measuring Diversity? A Capability-Controlled Audit of Majority-Vote Gain in LLM Ensembles
authors: [Donghwan Kim]
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2607.20768
doi: null
arxiv: '2607.20768'
cite: Kim, D. (2026). Are Diversity Metrics Measuring Diversity? A Capability-Controlled Audit of Majority-Vote Gain in LLM Ensembles. arXiv:2607.20768.
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Audits five ensemble diversity measures as predictors of majority-vote gain over the best member, across 31,900 subsets of 30 LLMs on MMLU-Pro (29 on TruthfulQA), with explicit capability controls. Oracle gain is positive in 100% of subsets, but simple voting beats the strongest member in only 9.98% of size-3 subsets (18.71% with held-out best selection) and 1.27% pooled over sizes 2 to 4. A joint-correctness "strict diversity" proxy is nearly collinear with one minus mean accuracy (size-3 Spearman 0.991 / 0.988), so raw diversity-gain associations largely re-express capability.

## Contribution

A caution for the "diversity is the lever" claim: many diversity metrics are capability in disguise, and voting rarely beats the best member.

## Key results

- Voting beats the best member in 9.98% of size-3 subsets (measured).
- Strict diversity vs 1 - mean accuracy Spearman about 0.99 (measured).

## Methods and models

Precomputed answers from 30 LLMs, subset enumeration, capability-controlled regressions. Abstract-level read.

## Limitations and open questions

Abstract only; no interaction between models.

## Relevance to us

Qualifies the diversity bullet: cross-family mixing lowers correlation ([[begin-2026-preference]], [[bertalanic-2026-ringelmann]]) but a diversity metric must be capability-controlled before it is credited with a gain.
