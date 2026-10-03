---
id: gh-anthropics-claude-agent-sdk-python
type: code
title: "Claude Agent SDK for Python: programmatic access to the Claude Code agent loop with tools, hooks and subagents"
repo: anthropics/claude-agent-sdk-python
url: https://github.com/anthropics/claude-agent-sdk-python
authors: ["Anthropic"]
year: 2025
language: Python
license: "MIT"
stars: 8209
last_commit: 2026-10-02
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Coordination model: a single Claude Code agent per query() or client, with bundled CLI, custom tools (in-process MCP servers), hooks and permission control; multi-agent structure comes from Claude Code's own subagent (Task) mechanism and from running many clients. MIT, 8.2k stars, active. The hackathon's own agents (this repo's AGENTS.md workflow) are built on this class of harness.

## What it can do for us

The path of least resistance for spinning up N Claude agents that share a filesystem or git repo as their 'board', which is structurally close to the wiki incident (shared mutable store, no direct messaging).

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Costs scale with N; no built-in population tooling or metrics.
