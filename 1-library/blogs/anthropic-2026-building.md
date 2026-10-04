---
id: anthropic-2026-building
type: blog
title: "Building a C compiler with a team of parallel Claudes"
authors: ["Nicholas Carlini"]
year: 2026
url: https://www.anthropic.com/engineering/building-c-compiler
site: Anthropic
topics: [llm-agent-swarms]
added_by: vishesh/codex-swarm-background
accessed: 2026-10-04
read_depth: skim
relevance: 3
---

## Summary

Carlini describes an experimental team of Claude instances working on a shared compiler codebase. Agents select tasks, claim them using repository files, merge changes and release claims. The author explicitly reports using no orchestration agent. The account illustrates coordination through a shared environment, while emphasizing the importance of a testing harness and the limitations of autonomous engineering.

## Key claims

- Agents choose work rather than receiving every task from a lead agent.
- Repository task locks discourage duplicate work; synchronization exposes conflicting claims.
- Shared code and running documents communicate progress and unresolved problems.

## Evidence quality

Vendor engineering account, skimmed through its retrieved opening and coordination description in this session. No independent run or full source-code audit performed. The architecture description supports a concrete example, not a controlled comparison proving decentralized coordination is superior. Performance and scale numbers are intentionally not used in the background brief.

## Relevance to us

Contrasts distributed task selection with the lead-plus-subagent Research architecture in [[anthropic-2025-how]]. The background brief interprets this as swarm-like coordination, not as a formal classification supplied by the author.
