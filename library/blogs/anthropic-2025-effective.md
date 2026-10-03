---
id: anthropic-2025-effective
type: blog
title: Effective context engineering for AI agents
authors:
- Prithvi Rajasekaran
- Ethan Dixon
- Carly Ryan
- Jeremy Hadfield
year: 2025
url: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
site: Anthropic
topics:
- llm-agent-swarms
- agent-budgets
added_by: vishesh/codex-methods
accessed: '2026-10-03'
read_depth: skim
relevance: 4
---

## Summary

The post describes managing finite context through selective retrieval, compaction, persistent notes and separate agent contexts. It explains practical tradeoffs between retaining details and reducing context burden, including the risk that summaries discard facts needed later.

## Key claims

Persistent references and notes support selective reloading; aggressive compaction can remove critical details.

## Evidence quality

First-party practitioner guidance with examples and linked research. Introduction, technique sections and conclusion skimmed; no controlled general performance claim adopted.

## Relevance to us

Implementation baselines for SOC-21 and SOC-31; compare [[xu-2025-everything]] and measure correction survival separately.
