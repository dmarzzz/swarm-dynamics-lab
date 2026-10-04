---
id: papachristou-2025-network
type: paper
title: Network formation and dynamics among multi-LLMs
authors:
- Marios Papachristou
- Yuan Yuan
year: 2025
venue: PNAS Nexus
url: https://arxiv.org/abs/2402.10659
doi: 10.1093/pnasnexus/pgaf317
arxiv: '2402.10659'
cite: Papachristou, M., & Yuan, Y. (2025). Network formation and dynamics among multi-LLMs. PNAS Nexus, 4(12), pgaf317. https://doi.org/10.1093/pnasnexus/pgaf317
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 6 (OpenAlex, journal record, 2026-10-03); 45 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Builds a framework in which multiple LLM agents decide whom to link to, and benchmarks the resulting network formation against human decisions. In synthetic and real-world settings (friendship, telecommunication and employment networks) LLMs reproduce micro-level link-formation principles (preferential attachment, triadic closure, homophily) and macro-level properties (community structure, small-world effects). The weighting of principles adapts to context: LLMs favour homophily in friendship networks but heterophily in organisational settings. A controlled human-subject survey shows strong alignment between LLM and human link-formation decisions.

## Contribution

Shows that LLM populations self-organise interaction networks with familiar complex-network statistics, which matters for any swarm model where topology is endogenous rather than fixed. Cited by [[de-marzo-2024-ai]].

## Key results

- Claimed: preferential attachment, triadic closure and homophily reproduced; community structure and small-world effects emerge.
- Claimed: context-dependent homophily vs heterophily.
- Claimed: strong agreement with human survey responses on link formation.

## Methods and models

Sequential link-formation prompts over synthetic and real network data; comparison with network-formation models and a human survey. Models and statistics not checked.

## Limitations and open questions

Abstract-level read. Network formation is decided from summarised node attributes, not from repeated interaction dynamics.

## Relevance to us

Background for adaptive-topology swarm experiments (agents choose neighbours). Related: [[de-marzo-2026-collective]], [[yang-2024-oasis]].
