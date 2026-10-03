---
id: data-swarmbench-2025
type: dataset
title: 'SwarmBench experiment logs: LLMs as decentralised agents on five 2D-grid swarm tasks (Flocking, Pursuit, Synchronize, Foraging, Transport), 13 models'
authors:
- Kai Ruan
- Mowen Huang
- Ji-Rong Wen
- Hao Sun
year: 2025
url: https://huggingface.co/datasets/6cf/swarmbench
license: MIT
size: not reported on the card (datasets-server shows 0 rows; files are raw experiment logs)
format: Experiment log files grouped by task (v01-v05) and model; fetched with the repo's load_dataset.py
topics:
- llm-agent-swarms
- swarm-intelligence
- collective-motion
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers:
- ruan-2025-benchmarking
---

## Summary

Logs from SwarmBench ([[ruan-2025-benchmarking]], arXiv 2505.04364). LLM agents act as decentralised swarm members on a configurable 2D grid with only a local k x k view and local communication, on five tasks: Flocking, Pursuit, Synchronize, Foraging, Transport. Models: DeepSeek-V3, DeepSeek-R1, Claude 3.5 Haiku, Claude 3.7 Sonnet, Gemini 2.0 Flash, GPT-4.1, GPT-4.1-mini, GPT-4o, o3-mini, o4-mini, Llama 3.1 70B, Llama 4 Scout, QwQ-32B. The paper reports strong task-dependent variation and weak long-range planning.

## Access

https://huggingface.co/datasets/6cf/swarmbench, not gated, MIT. Code and runner at github.com/x66ccff/swarmbench.

## Relevance to us

Direct LLM-swarm behaviour logs under swarm-like constraints, so a baseline for what LLM collectives do with only local information. Pairs with [[data-swarmworld-2026]] for larger populations.
