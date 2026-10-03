---
id: borysenko-2026-developer
type: paper
title: "Developer Experience with AI Coding Agents: HTTP Behavioral Signatures in Documentation Portals"
authors: ["Oleksii Borysenko"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2604.02544
doi: "10.48550/arXiv.2604.02544"
arxiv: "2604.02544"
cite: "Borysenko, O. (2026). Developer Experience with AI Coding Agents: HTTP Behavioral Signatures in Documentation Portals. arXiv preprint arXiv:2604.02544."
topics: ["swarm-detection", "llm-agent-swarms"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "1 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Borysenko records HTTP request fingerprints when nine AI coding agents (Aider, Antigravity, Claude Code, Cline, Cursor, Junie, OpenCode, GitHub Copilot agent mode, Windsurf) and six assistant services (ChatGPT, Claude, Gemini, NotebookLM, Mistral, Perplexity) fetch a live documentation endpoint. Each leaves identifiable signatures in runtime environment, prefetch strategy, User-Agent and header patterns. Agent access collapses multi-page navigation into one or two requests, so session depth, time-on-page and bounce rate stop meaning anything.

## Contribution

Extends agent fingerprinting from browser agents to coding agents and assistant fetchers, from the publisher's analytics viewpoint.

## Key results

- Measured (abstract): 15 agents/services each show identifiable HTTP signatures.
- Observed (abstract): agent visits compress navigation to one or two requests, breaking engagement metrics.

## Methods and models

Live documentation endpoint, HTTP request logging and comparison across clients. Abstract only.

## Limitations and open questions

Abstract only; no classifier accuracy reported in the abstract; single site.

## Relevance to us

Coding agents are a large share of agent traffic and use plain HTTP clients, so they are easier to fingerprint than browser agents. Adds to the per-product signature catalogue alongside [[kang-2026-whose]].
