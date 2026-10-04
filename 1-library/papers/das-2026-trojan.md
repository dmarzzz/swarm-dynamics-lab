---
id: das-2026-trojan
type: paper
title: 'Trojan Hippo Bench: A Dynamic Benchmark for Persistent Memory Attacks and Defenses in LLM Agents'
authors: [Debeshee Das, Julien Piet, Darya Kaviani, Luca Beurer-Kellner, Florian Tramèr, David Wagner]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.01970
doi: null
arxiv: '2605.01970'
cite: 'Das, D., Piet, J., Kaviani, D., Beurer-Kellner, L., Tramèr, F., & Wagner, D. (2026). Trojan Hippo Bench: A Dynamic Benchmark for Persistent Memory Attacks and Defenses in LLM Agents. arXiv preprint arXiv:2605.01970.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 12  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

The "Trojan Hippo" attack plants a dormant payload in an agent's long-term memory through one untrusted tool call, such as a crafted email. The payload activates only when the user later discusses sensitive topics (finance, health, identity) and then exfiltrates personal data. The benchmark has an OpenEvolve-based adaptive red-teaming loop that keeps refining attacks against defences and memory backends, plus a capability-aware security-utility analysis. It is instantiated on an email assistant over four memory backends: explicit tool memory, agentic memory, RAG and sliding-window context. Measured (abstract): undefended ASR is 85 to 100% against frontier OpenAI and Google models, and planted memories still activate after 100 benign sessions. Four defences based on basic security principles reduce ASR to as low as 0 to 5%, at utility costs that depend on the task mix.

## Contribution

A threat model with a single untrusted write, plus adaptive, evolving attacks against memory defences.

## Key results

- 85 to 100% ASR undefended (abstract).
- Payloads activate after 100 benign sessions (abstract).
- Defences reach 0 to 5% ASR with variable utility cost (abstract).

## Methods and models

An email assistant, four memory backends, and adaptive attack generation with OpenEvolve. The specific defences were not read.

## Limitations and open questions

Abstract only. Single application domain.

## Relevance to us

For Q3, the 100-benign-session dormancy result means merged poison does not need to act right away. A parent cannot rely on a quarantine period after merge to reveal a corrupted sub-agent's contribution. Any probation window would have to be longer than the attacker's trigger condition, which the attacker chooses (inferred). The adaptive red-teaming harness is a candidate tool for testing Q2 merge thresholds against an attacker who optimises around them. Compare [[chen-2024-agentpoison]] (trigger-keyed retrieval) and [[gadgil-2026-bad]].
