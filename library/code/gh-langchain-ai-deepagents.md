---
id: gh-langchain-ai-deepagents
type: code
title: "Deep Agents: opinionated agent harness on LangGraph with subagents, filesystem, shell, memory and skills"
repo: langchain-ai/deepagents
url: https://github.com/langchain-ai/deepagents
authors: ["LangChain"]
year: 2025
language: Python
license: "MIT"
stars: 29923
last_commit: 2026-10-03
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Coordination model: orchestrator with subagents in isolated context windows, plus pluggable filesystem (local, sandboxed or remote), shell access, context summarisation, persistent memory, human approval of tool calls and loadable skills. Model-agnostic. Built on LangGraph so inherits checkpoints and tracing. MIT, 29.9k stars, very active.

## What it can do for us

Fast way to get a Claude-Code-like agent with subagents for our own analysis work (e.g. running the audit bench), rather than for simulating swarms.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Single principal agent delegating down; no shared-world or many-peer mode.
