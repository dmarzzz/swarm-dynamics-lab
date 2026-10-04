---
id: gh-asago-ai-midojo
type: code
title: 'MiDojo: man-in-the-middle prompt injection testing for sandboxed agents, after AgentDojo'
repo: asago-ai/midojo
url: https://github.com/asago-ai/midojo
authors: [asago-ai]
year: 2026
language: Python
license: Apache-2.0
stars: 15
last_commit: 2026-10-02
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [debenedetti-2024-agentdojo]
---

## Summary

MiDojo, inspired by AgentDojo ([[gh-ethz-spylab-agentdojo]]), places itself between an agent and its tools so it can plant prompt injections in prompts, workspace files or tool responses, then judges both task completion and attack success from answers, recorded tool calls, environment changes and sandbox evidence (file changes, processes, network activity). Each evaluation runs in a fresh NVIDIA OpenShell sandbox on Podman or Docker; an "unmanaged" runtime and a session-forwarding example connect external agents, including an A2A agent in the minibank suite. Suites shipped: a weather reference suite with a fake MCP server, a document assistant, and minibank (unauthorized transfers, data leaks, policy bypass). The README reports security as attack success rate, lower is better.

## What it can do for us

Q1 and Q3: the man-in-the-middle position MiDojo takes is the position of an adversary who controls the channel a child uses in a foreign domain, or the channel back to the parent. Its A2A forwarding example means a parent and child running as separate agents could be wired through it, with the injection placed on the return path, which is a direct test of whether a parent accepts a tampered report. Sandbox evidence (what the agent did, not what it said) is the right ground truth for deciding whether a merge actually changed the parent's behaviour.

## Run notes

Not run. Requires OpenShell v0.1.2 gateway (Linux or Apple silicon macOS via Homebrew), Podman or Docker, uv, Python 3.12+, and an OpenAI-compatible model endpoint with tool calling; build the example image and run with uv per README.

## Limitations

New (created April 2026), 15 stars, single organisation with no paper. Tied to OpenShell 0.1.x. No published results beyond the README's example card.
