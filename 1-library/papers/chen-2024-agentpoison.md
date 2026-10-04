---
id: chen-2024-agentpoison
type: paper
title: 'AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases'
authors: [Zhaorun Chen, Zhen Xiang, Chaowei Xiao, Dawn Song, Bo Li]
year: 2024
venue: Advances in Neural Information Processing Systems (NeurIPS 2024); arXiv preprint
url: https://arxiv.org/abs/2407.12784
doi: null
arxiv: '2407.12784'
cite: 'Chen, Z., Xiang, Z., Xiao, C., Song, D., & Li, B. (2024). AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases. Advances in Neural Information Processing Systems 37 (NeurIPS 2024). arXiv:2407.12784.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: null
code: [gh-ai-secure-agentpoison]
---

## Summary

AgentPoison is a backdoor attack on agents that retrieve demonstrations or knowledge from long-term memory or a RAG store. The attacker inserts a few malicious demonstrations into the memory and optimises a trigger phrase, by constrained optimisation over the embedding space, so that any user instruction containing the trigger retrieves those demonstrations with high probability. Benign instructions retrieve normal records. No model training or fine-tuning is needed. Measured (abstract): average attack success above 80% on a RAG-based autonomous-driving agent, a knowledge-intensive QA agent and EHRAgent, with under 1% benign performance loss at a poison rate below 0.1%.

## Contribution

It established memory and knowledge-base poisoning as a distinct agent attack class with a retrieval-targeting optimisation. Its threat model assumes the attacker can write into the memory directly.

## Key results

- ASR above 80% on average across three agents (abstract).
- Under 1% benign degradation at a poison rate under 0.1% (abstract).
- Triggers transfer across retrievers and stay coherent in context (abstract claim; not checked in the body).
- [[sharma-2026-smsr]] cites AgentPoison as reaching 62.6% end-to-end success with a single poisoned entry in a database of about 23k entries. That is a secondary report and was not checked here.

## Methods and models

Trigger optimisation maps triggered queries to a compact, distinct region of embedding space. It is evaluated on driving, QA and EHR agents. Details were not read beyond the abstract.

## Limitations and open questions

It requires write access to the memory or knowledge base, which [[dong-2025-memory]] relaxes to query-only access. It also requires the victim's query to contain the trigger.

## Relevance to us

For Q3, AgentPoison is the backdoor variant of the merge attack. A corrupted sub-agent could carry trigger-keyed records back to the parent that stay dormant until the parent's own later queries contain the trigger. Clean-behaviour audits of the merged memory would then miss them (under 1% benign change). For Q2, a trigger concentrates retrieval on the attacker's records, so a merge rule that caps how many retrieved records can come from any single returning sub-agent would limit it (inferred, compare the occupancy-bound proposal in [[karunanidhi-2026-utility]]). The defences evaluated against it include [[wei-2025-amemguard]] and [[xiong-2026-maple]]. Code is at [[gh-ai-secure-agentpoison]].
