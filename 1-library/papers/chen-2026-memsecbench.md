---
id: chen-2026-memsecbench
title: 'MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence
  and Repair'
authors:
- Xuanze Chen
- Xukang Xie
- Wentao Fu
- Jiajun Zhou
- Shanqing Yu
- Qi Xuan
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.27080
doi: null
arxiv: '2607.27080'
type: paper
topics:
- fork-merge-security
- llm-agent-swarms
added_by: shadow/sol-g74
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
cite: 'Xuanze Chen; Xukang Xie; Wentao Fu; Jiajun Zhou; Shanqing Yu; Qi Xuan. (2026).
  MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and
  Repair. arXiv preprint. arXiv:2607.27080.'
---

## Summary

MemSecBench evaluates the lifecycle from malicious memory admission to later action and selective repair. It compares exact harness, memory-backend and model configurations and distinguishes whether contamination persists from whether it produces a consequential action.

## Contribution

Analysis of propagation, lifecycle security, containment or trust-boundary assessment.

## Key results

The abstract reports 310 cases from 48 contexts and 24 configurations. Memory persistence is 84.2% and end-to-end success 50.3%; among successfully poisoned cases, 59.6% complete the execution chain and 56.1% achieve selective repair. These denominators differ.

## Methods and models

Primary arXiv abstract and metadata read.

## Limitations and open questions

Full methods and uncertainties were not checked; do not infer cross-agent infection merely from persistent memory compromise.

## Relevance to us

Relevant benchmark for tracking a returning child memory beyond the initial merge. Compare [[zha-2026-autonomous]] and [[lin-2026-survey]].
