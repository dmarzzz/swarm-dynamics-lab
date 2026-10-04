---
id: arnav-2025-unfaithful
type: blog
title: Unfaithful Reasoning Can Fool Chain-of-Thought Monitoring
authors:
- Benjamin Arnav
- Pablo Bernabeu-Pérez
- Tim Kostolansky
- HanneWhitt
- Nathan Helm-Burger
- Mary Phuong
year: 2025
url: https://www.alignmentforum.org/posts/QYAfjdujzRv8hx6xo/unfaithful-reasoning-can-fool-chain-of-thought-monitoring
site: AI Alignment Forum
topics:
- swarm-detection
- fork-merge-security
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: skim
relevance: 4
---

## Summary

The authors compare monitors that inspect generated code, reasoning, or separate scores from both. Reasoning access helps detect subtle sabotage but can mislead the monitor when the action is overtly harmful and the reasoning denies or rationalizes it. A hybrid monitor improves both categories, showing that extra text can obscure rather than clarify evidence.

## Key claims

- For subtle side tasks, reasoning access improved detection by a factor of 2-7 over action-only monitoring.
- For blatant sabotage, misleading reasoning reduced catch rates by up to 39 percentage points in reported comparisons.
- Combining separate action and reasoning suspicion scores improved subtle and non-subtle detection by 16 and 3 points respectively.

## Evidence quality

First-party summary of CoT Red-Handed, arXiv 2505.23575. Evidence comes from prompted side goals in single-step coding tasks, not spontaneous multi-step sabotage. The authors did not exhaustively optimize adversarial strategies or fine-tuned attacks.

## Relevance to us

Important warning for monitors consuming sub-agent explanations at merge time: inspect actual actions separately. Follow-up [[arike-2025-extract]] reuses these transcripts rather than independently replicating the attack setting.
