---
id: pouryousef-2026-large
type: paper
title: "A Large-Scale Benchmark and Risk Assessment of Traffic Analysis Attacks on Cloud LLM Services"
authors: ["Shahrooz Pouryousef", "Jesus Lopez", "Saeefa Rubaiyat Nowmi", "Md Mahmuduzzaman Kamol", "Moinul Hossain", "Muoi Tran", "Mohammad Saidur Rahman"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.31877
doi: null
arxiv: "2609.31877"
cite: "Pouryousef, S., Lopez, J., Nowmi, S. R., Kamol, M. M., Hossain, M., Tran, M., & Rahman, M. S. (2026). A Large-Scale Benchmark and Risk Assessment of Traffic Analysis Attacks on Cloud LLM Services. arXiv:2609.31877."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Unified measurement study and public benchmark of encrypted LLM traffic: 60,000 user-LLM interactions across 10 models and 6 prompt categories plus 2,838 multi-agent executions over 10 task categories and two coordination topologies. From packet sizes, directions, timing and bursts alone, model fingerprinting reaches 97.7% balanced accuracy, prompt category 76.7%, and multi-agent task fingerprinting up to 90.7%. Prompt reformulation weakens but does not remove model leakage, and task fingerprints survive from a single agent's traffic.

## Contribution

Benchmark showing a passive network observer can name the serving model and the multi-agent task.

## Key results

- Model fingerprinting 97.7% balanced accuracy from encrypted metadata (abstract).
- Prompt-category fingerprinting 76.7% mean accuracy (abstract).
- Multi-agent task fingerprinting up to 90.7%, detectable from one agent's traffic (abstract).

## Methods and models

Traffic capture across 10 models; multi-agent executions with two topologies; robustness to reformulation, temperature, larger candidate sets, partial observation.

## Limitations and open questions

Lab traffic; abstract-only reading.

## Relevance to us

The strongest evidence in this lane that network metadata identifies models and even multi-agent coordination tasks, a vantage point for detecting swarms at the network edge. Related: [[zhang-2025-exposing]], [[mcdonald-2025-whisper]].
