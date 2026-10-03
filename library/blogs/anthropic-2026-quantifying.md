---
id: anthropic-2026-quantifying
type: blog
title: Quantifying infrastructure noise in agentic coding evals
authors:
- Gian Segato
year: 2026
url: https://www.anthropic.com/engineering/infrastructure-noise
site: Anthropic
topics:
- meta
- agent-budgets
- llm-agent-swarms
added_by: vishesh/codex-methods
accessed: '2026-10-03'
read_depth: skim
relevance: 4
---

## Summary

Anthropic reports experiments varying resource enforcement while holding the model, harness and task set fixed. The post distinguishes fewer infrastructure failures from extra resources enabling different problem-solving strategies, showing why agent scores need explicit execution-environment context.

## Key claims

In Terminal-Bench, infrastructure errors fell from 5.8% to 2.1% at 3x headroom, while the corresponding score change was not significant (p=0.40).

## Evidence quality

First-party engineering measurements; introduction, result sections and recommendations skimmed. Not an independent replication or universal 3x recommendation.

## Relevance to us

For SOC-32 and BUD-17, separately record resource guarantees, hard limits, timeouts and completion.
