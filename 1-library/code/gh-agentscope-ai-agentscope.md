---
id: gh-agentscope-ai-agentscope
type: code
title: "AgentScope: Alibaba's production agent framework (v2.0), pipelines, A2A, realtime voice; earlier versions advertised large-scale multi-agent simulation"
repo: agentscope-ai/agentscope
url: https://github.com/agentscope-ai/agentscope
authors: ["Alibaba Tongyi Lab / ModelScope"]
year: 2024
language: Python
license: "Apache-2.0"
stars: 32719
last_commit: 2026-09-30
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulation model: none specific in v2.0; it is a general agent framework with message passing between agents, pipelines (fixed-order, team leader delegation), SOPs, MCP/A2A and model routing. Scale: the current README does not claim simulation scale. LLM-native: yes, many providers. Adversarial hooks: none. Weight: Python 3.11+, `uv pip install agentscope`. The repo moved from modelscope/agentscope (the old path redirects).

## What it can do for us

Only as an orchestration layer if we wanted distributed actor-style agents; for a sim environment the purpose-built tools in this lane are a better fit. Samples live in agentscope-ai/agentscope-samples.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code.

## Limitations

Fast-moving 2.0 API; the 2024 large-scale simulation features are not described in the current README, so check the docs before relying on them.
