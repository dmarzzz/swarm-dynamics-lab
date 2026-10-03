---
id: data-agent-ipi-structured-2026
type: dataset
title: 'Agent-IPI Structured Interaction Datasets v2: clean/attacked tool-calling inputs for indirect prompt injection (249,648 pairs)'
authors: [Z-Edgar]
year: 2026
url: https://huggingface.co/datasets/Z-Edgar/Agent-IPI-Structured-Interaction-Datasets-v2
license: unspecified
size: 249,648 clean/attacked pairs (train 246,648; test 3,000) across 12 JSON files
format: 'JSON arrays of {clean, attacked} objects, split by train/test, JSON/XML input format and difficulty (no_attack, easy, hard)'
topics: [fork-merge-security]
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Synthetic training and test data for defending tool-calling LLMs against instruction hijacking. Clean tool-calling inputs in JSON or XML are paired with attacked versions, balanced across no_attack, easy (value-level or structure-level injection) and hard (structure-destroying or combined) buckets. Seven attack templates (ignore-previous, to-do prefix, important-message, naive, cosplay, nested override, fake user message) carry 32 attack goals extended from arXiv 2504.18575 (the WASP paper, [[gh-facebookresearch-wasp]]). Clean data is deduplicated from existing tool-calling datasets plus synthetic examples.

## Access

Public, ungated, on Hugging Face. No licence tag on the card. Not downloaded here.

## Relevance to us

Usable as a training set for an injection filter on messages that sub-agents return to a parent. It is single-agent and synthetic, so it is a classifier corpus, not evidence about agent collectives.
