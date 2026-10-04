---
id: gh-aaronrose227-narcbench
type: code
title: "NARCBench: activation-probe pipeline for detecting collusion among LLM agents"
repo: aaronrose227/narcbench
url: https://github.com/aaronrose227/narcbench
authors: ["Aaron Rose"]
year: 2026
language: Python
license: "MIT"
stars: 23
last_commit: 2026-05-08
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [rose-2026-detecting]
---

## Summary

Code for [[rose-2026-detecting]]: generates multi-agent scenarios in three tiers (Core, Transfer, Stego), extracts hidden-state activations from an open-weight model, trains five probing techniques on a learned deception direction, and reports collusion-detection AUROC in and out of distribution. Preconfigured for Qwen3-32B-AWQ, Llama-3.1-70B-Instruct-AWQ-INT4, DeepSeek-R1-Distill-Qwen-32B and gpt-oss-20b; dataset on Hugging Face. 23 stars, MIT, last commit 2026-05-08.

## What it can do for us

A white-box collusion detector we could run over open-weight firm agents in the swarm factory, complementing market-structure signals.

## Run notes

Not run. README read via GitHub API. CUDA GPU required for generation and extraction (Llama-70B needs 2x48 GB); probes run on CPU.

## Limitations

Only works with open-weight models exposing hidden states; scenarios are not market games, so transfer to pricing or quantity collusion is untested.
