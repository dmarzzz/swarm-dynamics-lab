---
id: gao-2026-distribution
type: paper
title: Distribution-Free Uncertainty Quantification for Continuous AI Agent Evaluation
authors:
- Yuxuan Gao
- Megan Wang
- Yi Ling Yu
year: 2026
arxiv: '2605.19779'
doi: null
url: https://arxiv.org/abs/2605.19779
venue: arXiv
cite: Yuxuan Gao; Megan Wang; Yi Ling Yu (2026). Distribution-Free Uncertainty Quantification for Continuous AI Agent Evaluation. arXiv:2605.19779.
topics:
- criticality-measurement
- llm-agent-swarms
added_by: vishesh/codex-methods
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

This paper applies conformal methods to forecasting agent quality scores and ranking abstention. It also studies uncertainty propagation in simulated pipelines, separating individual score intervals from decisions about whether rankings are distinguishable.

## Contribution

Split conformal prediction, adaptive conformal inference, pipeline simulation and multiple-testing corrections.

## Key results

The abstract reports calibration error below 0.02 at a 24-hour horizon and studies 50 agents through 18 signals.

## Methods and models

Assessment based on the source sections specified below; no implementation was run.

## Limitations and open questions

Abstract only. Quality-score signals are not ground-truth task success. Coverage assumptions and dependence must be checked before applying any guarantee.

## Relevance to us

A methodological lead for SOC-38 selection and SOC-31 uncertainty; no guarantee for our adaptive agents is inferred.
