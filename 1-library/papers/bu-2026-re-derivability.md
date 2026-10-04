---
id: bu-2026-re-derivability
type: paper
title: Re-derivability Decides What a Staged Agent Pipeline Recovers After an Upstream Fault
authors:
- Tianqi Bu
- YuXuan Peng
- Junteng Tu
- Henghui Xiao
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.32802
doi: null
arxiv: '2609.32802'
cite: 'Bu, T., Peng, Y., Tu, J., & Xiao, H. (2026). Re-derivability Decides What a Staged Agent Pipeline Recovers After an Upstream Fault. arXiv preprint arXiv:2609.32802.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

In a staged pipeline of LLM agents, one deterministic fault is injected into the first stage, and the original problem is re-exposed to k = 0 to 3 downstream stages with everything else fixed (120 gsm_hard items per arm, temperature zero, four open-weight backbones). Accuracy under fault rises on all four backbones, by +0.233 to +0.392 (largest Holm-adjusted p = 2.1e-6). An inspector grounded in the original problem beats a blind inspector by +0.358 to +0.608 (exploratory); on two Qwen backbones the blind inspector changes nothing. Most of the gain comes from the first re-grounded stage (+0.394 matched retention for about 60 extra tokens per item on Qwen3-14B). With no fault, the pipeline loses to a single direct call on three of four backbones.

## Contribution

Identifies re-derivability, how much a stage can rebuild from the original problem, as the variable that sets how far an upstream fault propagates.

## Key results

- Measured (per abstract, confirmatory): re-exposing the original problem raises accuracy under fault by +0.233 to +0.392 on 4 of 4 backbones.
- Measured (per abstract, exploratory): grounded inspector +0.358 to +0.608 over blind inspector.
- Measured (per abstract): retention tracks the visible fraction of the original problem, from 0.221 to 0.692 on the primary backbone.
- Measured (per abstract): no decomposition reliably beats one direct call.

## Methods and models

Preregistered fault-injection design with kill tests; four open-weight backbones with thinking disabled. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; one deterministic fault type; arithmetic tasks.

## Relevance to us

Q2 and Q3. For merging, the analogue of re-derivability is whether the parent can check a returning sub-agent's claims against primary material it holds itself, rather than trusting the sub-agent's summary. A blind inspector (one that sees only the returned output) did nothing on two backbones, which argues that a merge gate must be grounded in independent evidence. It is the pipeline counterpart of [[liu-2026-consensus]], where honest agents correct corrupted ones only when they can re-derive the reasoning.
