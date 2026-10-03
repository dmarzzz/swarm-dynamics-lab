---
id: wang-2026-oep
type: paper
title: 'OEP: Poisoning Self-Evolving LLM Agents via Locally Correct but Non-Transferable Experiences'
authors: [Kaixiang Wang, Jiong Lou, Zhaojiacheng Zhou, Jie Li]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.18930
doi: null
arxiv: '2605.18930'
cite: 'Wang, K., Lou, J., Zhou, Z., & Li, J. (2026). OEP: Poisoning Self-Evolving LLM Agents via Locally Correct but Non-Transferable Experiences. arXiv preprint arXiv:2605.18930.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: 10  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

Obsessive Experience Poisoning (OEP) is a low-privilege, black-box attack on reflective, self-evolving agents. It needs no access to the system prompt or the memory store, and its content is not explicitly malicious. The attacker induces the agent to work through "clean edge cases" that combine a locally correct solution, a method that does not transfer, and severe but plausible hypothetical consequences. During reflection and memory consolidation the agent over-trusts its own reflections and distils these local experiences into high-priority, over-generalised, risk-averse rules, which then cause failures on later tasks. Measured (abstract): ASR above 50% with GPT-4o agents across three domains, and better than existing attacks under an LLM-auditing defence.

## Contribution

A poison that contains no false fact and no instruction, only a correct but unrepresentative experience whose damage comes from the agent's own generalisation.

## Key results

- ASR above 50% with GPT-4o across three domains (abstract).
- Outperforms prior memory attacks when an LLM auditor is deployed (abstract).

## Methods and models

Black-box. Targets reflection and consolidation. Domains and agents not read beyond the abstract.

## Limitations and open questions

Abstract only. Effects on non-reflective memory designs are not stated.

## Relevance to us

For Q3 this is perhaps the most natural attack on a sub-agent sent to explore an unusual domain, because the "locally correct but non-transferable" experience is exactly what such a domain produces even without an adversary. An adversary only has to curate edge cases with severe stakes. When the sub-agent's lessons are merged and the parent consolidates them, the over-generalised rules become parent-wide policy. That is corruption without injection, and content audits do not catch it (the abstract reports LLM auditing is beaten). For Q2 it suggests that a merge rule should require a lesson to be corroborated by sub-agents working in other domains before it is promoted to a global rule, a cross-domain version of k-of-n (inferred). Compare [[zhan-2026-when]] (authority collapse at consolidation), [[srivastava-2025-memorygraft]] (fake successful experiences) and [[ying-2026-skilljack]].
