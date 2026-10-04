---
id: gh-sleeeepeer-poisonedrag
type: code
title: 'PoisonedRAG: official code for knowledge corruption attacks on RAG'
repo: sleeepeer/PoisonedRAG
url: https://github.com/sleeepeer/PoisonedRAG
authors: [Wei Zou, Runpeng Geng, Binghui Wang, Jinyuan Jia]
year: 2024
language: Python
license: MIT
stars: 302
last_commit: 2026-01-27
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [zou-2024-poisonedrag]
---

## Summary

The official implementation of PoisonedRAG [[zou-2024-poisonedrag]] (USENIX Security 2025). It crafts a small number of malicious texts per target question so that a RAG pipeline retrieves them and outputs an attacker-chosen answer. It supports a black-box LLM-targeted method and a white-box HotFlip method over BEIR datasets (NQ, HotpotQA, MS-MARCO) with a Contriever retriever. It reuses model wrappers from Open-Prompt-Injection ([[liu-2023-formalizing]]) and code from princeton-nlp corpus-poisoning.

## What it can do for us

It generates targeted false-fact poison for a retrieval-merged memory, which gives a ready attack for testing Q2 merge thresholds. The configurable `adv_per_query` (default 5) maps onto "how many poisoned records a corrupted sub-agent brings home per topic".

## Run notes

Not run. The README specifies conda Python 3.10, torch 1.13.0+cu117 (CUDA, so a GPU is expected for local models), beir, openai and google-generativeai, and `python run.py` with parameters in run.py. API keys go in model_configs.

## Limitations

Pinned to an old CUDA 11.7 torch. PaLM 2 support is dated. It is a static-corpus attack and does not model agents writing their own memory. GitHub API metadata read 2026-10-03.
