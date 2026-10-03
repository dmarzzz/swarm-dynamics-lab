---
id: denisov-blanch-2026-consensus
type: paper
title: 'Consensus is Not Verification: Why Crowd Wisdom Strategies Fail for LLM Truthfulness'
authors:
- Yegor Denisov-Blanch
- Joshua Kazdan
- Jessica Chudnovsky
- Rylan Schaeffer
- Sheng Guan
- Soji Adeshina
- Sanmi Koyejo
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2603.06612
doi: null
arxiv: '2603.06612'
cite: 'Denisov-Blanch, Y., Kazdan, J., Chudnovsky, J., Schaeffer, R., Guan, S., Adeshina, S., & Koyejo, S. (2026). Consensus is Not Verification: Why Crowd Wisdom Strategies Fail for LLM Truthfulness. arXiv preprint arXiv:2603.06612.'
topics:
- fork-merge-security
- llm-agent-swarms
- collective-decision
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Asks whether scaling inference compute by sampling and aggregating can raise truthfulness where no external verifier exists. Across five benchmarks and several models, polling-style aggregation gives no consistent accuracy gain over single samples even at 25 times the inference cost, and often amplifies shared misconceptions. Models predict what other models will say better than they identify what is true. Different models produce correlated outputs even when conditioned on out-of-distribution random strings and asked for pseudo-random outputs. Confidence weighting does not help because self-reported confidence does not separate correct from incorrect answers.

## Contribution

A boundary for crowd-style aggregation of LLMs: it works where a verifier filters candidates, not where consensus is used as the verifier.

## Key results

- Measured (per abstract): no consistent gain from polling aggregation at up to 25x compute across five benchmarks.
- Measured (per abstract): cross-model output correlation persists on random-string prompts.
- Measured (per abstract): self-reported confidence fails to separate correct from incorrect answers.

## Methods and models

Sampling and polling aggregation, confidence weighting, random-string correlation probes. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; natural errors only.

## Relevance to us

Q2. A parent cannot treat agreement among returning sub-agents as verification of what they bring back from an unverifiable domain (news, foreign web, social claims); agreement there reflects shared priors more than truth. Confidence weighting is no fix, consistent with the falsified-confidence attack in [[lee-2026-robust]] and [[zheng-2025-rethinking]]. Verification has to come from a check the sub-agents do not share. Related: [[kim-2025-correlated]], [[liu-2026-consensus]].
