---
id: xiao-2026-when
type: paper
title: 'When Collaboration Becomes a Trigger: Collective Evidence-Threshold Backdoors in Multi-Agent Systems'
authors:
- Jia-Hao Xiao
- Lei Feng
- Min-Ling Zhang
year: 2026
arxiv: '2608.01085'
doi: null
url: https://arxiv.org/abs/2608.01085
venue: arXiv
cite: 'Jia-Hao Xiao; Lei Feng; Min-Ling Zhang (2026). When Collaboration Becomes a Trigger: Collective Evidence-Threshold Backdoors in Multi-Agent Systems. arXiv:2608.01085.'
topics:
- llm-agent-swarms
- fork-merge-security
added_by: vishesh/codex-methods
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

The paper studies backdoor behavior triggered by accumulated peer evidence rather than an isolated message. It proposes a collective trigger mechanism and a defense that examines latent transitions and quarantines anomalous updates using clean-only calibration.

## Contribution

BCBI collective backdoors and LATTE transition-based defense.

## Key results

The abstract reports attack and defense evaluations; effect sizes and operating points were not checked.

## Methods and models

Assessment based on the source sections specified below; no implementation was run.

## Limitations and open questions

Abstract only. This trained-backdoor threat differs from our external misinformation setting; success cannot be transferred between them.

## Relevance to us

Motivates testing history-dependent re-entry in SEC-48 and keeping model-compromise assumptions separate from [[chen-2026-memsecbench]].
