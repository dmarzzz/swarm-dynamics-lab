---
id: cognition-2025-dont
type: blog
title: Don't Build Multi-Agents
authors: [Cognition]
year: 2025
url: https://cognition.ai/blog/dont-build-multi-agents
site: Cognition
topics: [llm-agent-swarms]
added_by: shadow/sol-w6
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Cognition argues against default multi-agent architectures for production agents because context fragmentation creates compounding reliability failures. Their two principles are to share full agent traces, not isolated messages, and to treat actions as implicit decisions that can conflict when made by separated subagents.

## Key claims

- Multi-agent architectures that split a task, run subagents, and merge outputs are fragile because each subtask can lose the nuance of the original multi-turn context.
- Sharing the original request is not enough. Subagents also need previous tool calls, decisions, and trace context that shaped how the task was decomposed.
- Actions carry implicit design decisions. Parallel subagents can make inconsistent choices even when each local output is plausible.
- Cognition recommends ruling out architectures that do not preserve shared context and decision visibility, unless the system has an explicit mechanism for reliable cross-agent context passing.
- A single-threaded linear agent remains the simplest reliable baseline. For long traces, Cognition suggests compressing histories of actions, events, and decisions rather than parallelizing decision makers prematurely.
- The post treats Claude Code's subagents as a constrained pattern: useful for investigation and context management, but not for parallel code-writing where conflicting assumptions would be hard to reconcile.

## Evidence quality

This is an engineering-opinion post from a production agent builder, backed by architectural reasoning and examples from Devin, Claude Code subagents, edit-apply models, OpenAI Swarm, AutoGen, and MetaGPT. It does not report a benchmark or ablation study. Its value is strongest as practitioner evidence about failure modes in long-running coding agents.

## Relevance to us

This is a high-priority counterweight to optimistic LLM-agent-swarm designs. Any hackathon hypothesis about parallel agent swarms needs to account for Cognition's objection: swarm throughput may be dominated by coordination and context-transfer failures rather than model capability.
