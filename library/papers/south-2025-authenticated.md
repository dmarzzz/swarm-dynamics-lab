---
id: south-2025-authenticated
type: paper
title: Authenticated Delegation and Authorized AI Agents
authors:
- Tobin South
- Samuele Marro
- Thomas Hardjono
- Robert Mahari
- Cedric Deslandes Whitney
- Dazza Greenwood
- Alan Chan
- Alex Pentland
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2501.09674
doi: null
arxiv: '2501.09674'
cite: 'South, T., Marro, S., Hardjono, T., Mahari, R., Whitney, C. D., Greenwood, D., Chan, A., & Pentland, A. (2025). Authenticated Delegation and Authorized AI Agents. arXiv preprint arXiv:2501.09674.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 82 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Proposes a framework for authenticated, authorised and auditable delegation of authority from humans to AI agents. Users delegate and restrict an agent's permissions and scope while keeping a chain of accountability. The framework extends OAuth 2.0 and OpenID Connect with agent-specific credentials and metadata so it is compatible with existing web authentication, and adds a method for translating natural-language permissions into auditable access-control configurations.

## Contribution

A concrete protocol path for binding agents to accountable principals using deployed identity standards, rather than new infrastructure.

## Key results

- No quantitative results in the abstract; a protocol design.

## Methods and models

Extension of OAuth 2.0 and OpenID Connect; natural-language to access-control translation.

## Limitations and open questions

Abstract only. Delegation tokens say who an agent acts for, but do not by themselves stop one principal from minting many delegated agents; that bound has to come from the principal's identity (for example [[adler-2024-personhood]]) or from cost.

## Relevance to us

Gives a standards-based way to attach a swarm's agents to one accountable principal, which is the attribution step that makes Sybil swarms countable. Related: [[chan-2024-ids]], [[hu-2025-inter-agent]]. Tobin South is also a co-author of [[adler-2024-personhood]].
