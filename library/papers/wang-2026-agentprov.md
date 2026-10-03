---
id: wang-2026-agentprov
type: paper
title: "AgentProv: Auditing Agentic LLM API Providers via Tool-use Policy Probes"
authors: ["Xun Wang", "Bihe Zhao", "Michael Backes", "Franziska Boenisch", "Adam Dziedzic"]
year: 2026
venue: "EMNLP 2026 (accepted per arXiv comment); arXiv preprint"
url: https://arxiv.org/abs/2609.00052
doi: null
arxiv: "2609.00052"
cite: "Wang, X., Zhao, B., Backes, M., Boenisch, F., & Dziedzic, A. (2026). AgentProv: Auditing Agentic LLM API Providers via Tool-use Policy Probes. EMNLP 2026. arXiv:2609.00052."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

AgentProv audits the model behind agentic LLM APIs from the categorical distribution of tool calls rather than text, testing identity with an MMD permutation test. It catches every substituted model across 630 checkpoint pairs while keeping the false-positive rate under provider-injected system prompts at 7%, versus 67% for MET and 53% for the rank-based uniformity test.

## Contribution

Tool-call behaviour as an identity channel robust to system-prompt distortion, a weakness of text-based tests.

## Key results

- 100% detection on 630 substituted checkpoint pairs (abstract).
- FPR 7% under system-prompt injection vs 67% (MET) and 53% (RUT) (abstract).

## Methods and models

Tool-use policy probes; categorical action distributions; MMD permutation test; comparison with [[gao-2024-model]] and [[zhu-2025-auditing]].

## Limitations and open questions

Abstract-only reading; requires issuing probe tasks to the agent API.

## Relevance to us

Agent swarms act through tools; this suggests tool-call distributions are a stable model signature even behind persona prompts. Related: [[wang-2026-who]], [[park-2026-cross]].
