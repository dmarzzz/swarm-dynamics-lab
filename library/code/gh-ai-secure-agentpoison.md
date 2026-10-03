---
id: gh-ai-secure-agentpoison
type: code
title: 'AgentPoison: official implementation of memory and knowledge-base backdoor poisoning for LLM agents'
repo: AI-secure/AgentPoison
url: https://github.com/AI-secure/AgentPoison
authors: [Zhaorun Chen, Zhen Xiang, Chaowei Xiao, Dawn Song, Bo Li]
year: 2024
language: Python
license: MIT
stars: 244
last_commit: 2026-10-03
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: [chen-2024-agentpoison]
---

## Summary

The official NeurIPS 2024 implementation of AgentPoison [[chen-2024-agentpoison]], as described by the repository description. It optimises backdoor triggers so that triggered queries retrieve poisoned demonstrations from an agent's memory or knowledge base. A-MemGuard ([[gh-tangciuyueng-amemguard]]) is built on this codebase.

## What it can do for us

A reference attack environment for trigger-keyed memory poisoning, with driving, QA and EHR agents according to the paper. Usable as the "dormant backdoor carried home by a sub-agent" attack in Q3 experiments.

## Run notes

Not run. Only the GitHub API metadata (description, stars, licence, last push) was read, not the README.

## Limitations

Read depth is limited to the repository description. Last push 2026-10-03 per the GitHub API.
