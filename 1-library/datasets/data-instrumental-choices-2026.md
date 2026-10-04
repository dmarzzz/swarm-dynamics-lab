---
id: data-instrumental-choices-2026
type: dataset
title: 'Instrumental Choices agent traces: 1,680 terminal-agent trajectories scored for instrumental-convergence behaviour (10 models)'
authors: [Jonas Wiedermann-Möller, Leonard Dung, Maksym Andriushchenko]
year: 2026
url: https://huggingface.co/datasets/aisa-group/instrumental-choices-agent-traces
license: unspecified
size: 1,680 trajectories; 210 Inspect .eval logs, 210 diagnostic traces, 1,680 viewer sessions
format: 'Inspect .eval logs (authoritative), Hugging Face Session Trace Simple Format JSONL sessions, gzip JSONL runner diagnostics'
topics: [fork-merge-security]
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Trajectories behind arXiv 2605.06490: ten models, seven terminal tasks each with an official workflow and a policy-violating shortcut, eight variants (monitoring, stakes, permission, blocked honest path and so on), three repetitions. Deterministic environment-state scorers label each sample, with fields such as `ic_behavior_detected`. The abstract reports 86 of 1,680 samples (5.1%) showed instrumental-convergence behaviour, with two Gemini models accounting for 66.3% of cases. Local paths and usernames are redacted; visible reasoning summaries are kept.

## Access

Public, ungated, on Hugging Face. No licence tag on the card. Not downloaded here.

## Relevance to us

Single-agent propensity data, not swarm data. It is a baseline for how often an individual agent takes a policy-violating shortcut, which bounds how often a sub-agent might go rogue before any merge.
