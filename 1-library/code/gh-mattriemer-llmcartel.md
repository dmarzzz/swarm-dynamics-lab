---
id: gh-mattriemer-llmcartel
type: code
title: "LLMCartel: Bertrand duopoly and triopoly LLM collusion experiments with prompt variants and activation steering"
repo: mattriemer/LLMCartel
url: https://github.com/mattriemer/LLMCartel
authors: ["Matthew Riemer"]
year: 2026
language: Python
license: "none stated"
stars: 4
last_commit: 2026-05-28
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [riemer-2026-position]
---

## Summary

Reproduction code for [[riemer-2026-position]]: Bertrand game engines (environment/oligopoly.py for duopoly, multiprompt_oligopoly.py for triopoly with per-agent prompts), prompt prefixes (P0 profit-max, PI implicit and PC explicit collusion, AC/CD/AP anti-collusion, MD/NPA/NPB alternative objectives), steering-vector training and full and partial steering experiments, and LLM-as-judge scoring. Uses vllm and transformers. 4 stars, no licence file, last commit 2026-05-28.

## What it can do for us

A compact reference implementation of LLM oligopoly with per-firm prompts and steering, useful for the market layer and for steering-based Sybil or collusion conditions.

## Run notes

Not run. README read via GitHub API. Needs local GPU inference through vllm.

## Limitations

No licence (all rights reserved by default); tiny repo; Bertrand only.
