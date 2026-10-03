---
id: gh-mesa-mesa-llm
type: code
title: "Mesa-LLM: LLM-driven agents for Mesa models (reasoning modules, memory, tools, parallel async stepping)"
repo: mesa/mesa-llm
url: https://github.com/mesa/mesa-llm
authors: ["Mesa project contributors"]
year: 2025
language: Python
license: "Apache-2.0"
stars: 75
last_commit: 2026-09-16
topics: [llm-agent-swarms, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

One line: Mesa ABM where each LLMAgent observes neighbours within a vision radius, reasons with a pluggable module (CoT, ReAct, ReWOO), keeps short/long-term or episodic memory, and acts through decorated tool functions (spatial, environment, social-query tools); no throughput figures (each step is one or more LLM calls, run concurrently via asyncio or threads in parallel_stepping.py); LLM-driven by design through litellm (OpenAI, Anthropic, xAI, Hugging Face, Ollama, OpenRouter, Novita, Gemini); adversarial agents are just LLMAgents with a different system prompt or internal_state (no dedicated hooks); light to run except for API cost.

Official Mesa extension, under active development; the README warns the API may change significantly. Examples include Epstein civil violence, negotiation and a Sugarscape variant. A recording module (simulation_recorder, agent_analysis) logs agent events for later analysis.

## What it can do for us

The most direct starting point for an LLM-agent swarm inside a classic ABM: Mesa spaces and schedulers for the physical layer, LLMAgent for decisions, and a recorder for traces. A Sybil experiment would be a set of LLMAgents sharing one operator prompt and memory store, mixed with honest agents, with detection run on the recorded traces.

## Run notes

Not run. Skimmed mesa_llm/llm_agent.py (LLMAgent with vision, internal_state, plan/act/choose_action), module_llm.py (litellm completion with tenacity retries) and parallel_stepping.py (asyncio or threading).

## Limitations

Pre-release API. LLM cost and latency dominate; no batching across agents beyond concurrent calls. Inherits Mesa's per-agent Python overhead for the non-LLM parts.
