---
id: gh-google-research-camel-prompt-injection
type: code
title: 'CaMeL: reference implementation of capability-based prompt-injection defence for agents'
repo: google-research/camel-prompt-injection
url: https://github.com/google-research/camel-prompt-injection
authors: [Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel Fabian, Christoph Kern, Chongyang Shi, Florian Tramèr]
year: 2025
language: Python (repo labelled Jupyter Notebook)
license: Apache-2.0
stars: 399
last_commit: 2025-06-20
topics: [fork-merge-security]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [debenedetti-2025-defeating]
---

## Summary

Research artifact from Google, Google DeepMind and ETH Zurich that reproduces the CaMeL paper [[debenedetti-2025-defeating]]. A privileged LLM writes restricted Python; a custom interpreter executes it, calls a quarantined LLM for parsing untrusted data, tracks a dependency graph, and attaches capabilities (frozen sets of sources plus a readers set, defaulting to User source and Public readers, per src/camel/capabilities/capabilities.py) to every value. Security policies are Python functions checked before each tool call. Runs against AgentDojo [[debenedetti-2024-agentdojo]].

## What it can do for us

A working provenance-tracking interpreter: a starting point for a merge-time controller that tags every value a returning sub-agent hands back with its source (which child, which domain) and enforces per-tool policies on it.

## Run notes

Not run. README: install uv, copy .env.example to .env with API keys, then `uv run --env-file .env main.py MODEL_NAME [--run-attack] [--replay-with-policies] ...`. Requires commercial model API keys.

## Limitations

README warns the interpreter "likely contains bugs" and "might not be fully secure", is not a Google product, and will not be maintained. Last push June 2025.
