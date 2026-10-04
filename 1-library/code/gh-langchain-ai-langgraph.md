---
id: gh-langchain-ai-langgraph
type: code
title: "LangGraph: low-level stateful graph orchestration for long-running agents (durable execution, checkpoints, human-in-the-loop)"
repo: langchain-ai/langgraph
url: https://github.com/langchain-ai/langgraph
authors: ["LangChain"]
year: 2023
language: Python
license: "MIT"
stars: 42671
last_commit: 2026-10-03
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Coordination model: explicit state graph. Nodes are functions or agents, edges (including conditional) define control flow, state is checkpointed so runs survive failures and can be resumed or inspected mid-run; supports subgraphs, parallel branches (fan-out/fan-in), human interrupts and LangSmith tracing. Multi-agent patterns (supervisor, swarm-style handoff, hierarchical) are built on top. MIT, 42.7k stars, commits daily.

## What it can do for us

The right tool if an experiment needs a deterministic, replayable control graph around N agents with checkpoints at every step, which makes post-hoc analysis easy. Deep Agents (below) adds subagents and a filesystem on top.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Graph must be declared up front; emergent peer-to-peer structure has to be simulated inside a node or via a shared store.
