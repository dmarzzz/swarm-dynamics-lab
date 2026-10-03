---
id: abdelnabi-2025-firewalls
type: paper
title: Firewalls to Secure Dynamic LLM Agentic Networks
authors: [Sahar Abdelnabi, Amr Gomaa, Eugene Bagdasarian, Per Ola Kristensson, Reza Shokri]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2502.01822
doi: null
arxiv: '2502.01822'
cite: 'Abdelnabi, S., Gomaa, A., Bagdasarian, E., Kristensson, P. O., & Shokri, R. (2025). Firewalls to Secure Dynamic LLM Agentic Networks. arXiv:2502.01822.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

A dual-firewall architecture for agent-to-agent communication on behalf of users, built on the principle that each task defines a context and both sides carry far more information than that context needs. The Language Converter Firewall projects incoming messages from an external agent onto a closed, domain-specific structured protocol: the message becomes validated fields, and persuasive framing, urgency and embedded instructions have no channel through which to arrive. The Data Abstraction Firewall projects outgoing data onto the granularity the task needs instead of binary disclose-or-redact. Both run in a trusted environment isolated from external input and use domain rules learned from demonstrations. Measured (abstract, current arXiv version): across 864 attacks in three domains of the ConVerse benchmark, privacy attack success falls (for example from 84% to 10% for GPT-5) and security attack success from 60% to 3%, while task quality is maintained or improved.

## Contribution

Replaces "resist every manipulation" with a structural guarantee: the inbound channel cannot express manipulation.

## Key results

- Privacy attacks 84% to 10% (GPT-5), security attacks 60% to 3% (abstract).
- Task completion quality maintained or improved (abstract).

## Methods and models

Two firewalls; rules learned automatically from demonstrations; ConVerse benchmark.

## Limitations and open questions

Abstract-level reading. The abstract I read is the current arXiv version; earlier versions may report different numbers. Needs a closed protocol per domain, which an exploring sub-agent's open-ended findings may not fit.

## Relevance to us

The closest existing design to a merge firewall.
- Q2/Q3: a parent that accepts a returning child's report only as fields of a closed schema, validated deterministically, removes the channel that a memory-overwrite injection needs. The cost is that a child exploring an unfamiliar domain may find things the schema cannot express.
- Q1: the outbound Data Abstraction Firewall is the matching control on what a parent reveals to children it sends out, which limits what a captured child can tell an attacker about the parent.
Related: [[beurer-kellner-2025-design]], [[costa-2025-securing]], [[debenedetti-2025-defeating]].
