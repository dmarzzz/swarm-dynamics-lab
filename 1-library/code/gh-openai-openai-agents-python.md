---
id: gh-openai-openai-agents-python
type: code
title: "OpenAI Agents SDK: production multi-agent workflows with handoffs, agents-as-tools, guardrails, sessions, tracing and sandbox agents"
repo: openai/openai-agents-python
url: https://github.com/openai/openai-agents-python
authors: ["OpenAI"]
year: 2025
language: Python
license: "MIT"
stars: 29825
last_commit: 2026-10-02
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Coordination model: handoffs and agents-as-tools inside a single run loop, with guardrails on input/output, human-in-the-loop, sessions for conversation history, built-in tracing, MCP tools, realtime and voice agents, and (new in the README) sandbox agents preconfigured to work in a container over long horizons. Provider-agnostic (Responses, Chat Completions, 100+ other models). The successor to openai/swarm. Active, MIT, 29.8k stars.

## What it can do for us

A well-instrumented harness if we need a few cooperating agents with traces; the sandbox-agent mode is the closest OpenAI-sanctioned analogue to the long-horizon containerised agents in the incident. Not designed for hundreds of agents sharing an environment.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Hierarchical, orchestrator-centric; no notion of a shared world or peer discovery, which is what the incident dynamics need.
