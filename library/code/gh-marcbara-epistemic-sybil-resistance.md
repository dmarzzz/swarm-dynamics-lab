---
id: gh-marcbara-epistemic-sybil-resistance
type: code
title: 'epistemic-sybil-resistance: reproducibility package and ESB benchmark for epistemic Sybil aggregation'
repo: marcbara/epistemic-sybil-resistance
url: https://github.com/marcbara/epistemic-sybil-resistance
authors:
- Marc Bara
year: 2026
language: Python
license: MIT (code); separate LICENSE-DATA file for data
stars: 1
last_commit: '2026-09-01'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: skim
relevance: 4
papers:
- bara-2026-epistemic
---

## Summary

Code, frozen LLM outputs and analysis pipeline behind [[bara-2026-epistemic]]. It contains a synthetic-world generator, the elicitation client with exact prompts, four aggregators (naive, provenance-aware, report-space dedup, oracle), the 2x2 rationale renderer, analysis scripts, unit tests, and ESB (Epistemic Sybil Benchmark), which repackages the Grid A and Grid B evaluation data with a scoring command and baseline adapters.

## What it can do for us

Score any swarm aggregation rule on how its coverage collapses as report count rises at fixed evidence ancestry, without making model calls, since raw outputs are frozen in results/raw/*.jsonl. reproduce_paper.py regenerates all tables and figures.

## Run notes

Not run. README states reproduction needs only the frozen data; live collection scripts need API credentials (.env.example).

## Limitations

One task family (synthetic revenue memos) and one model's outputs; benchmark is single-author and new (1 star, last push 2026-09-01).
