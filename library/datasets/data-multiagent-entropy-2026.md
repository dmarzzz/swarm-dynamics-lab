---
id: data-multiagent-entropy-2026
type: dataset
title: 'Raw data for "When Does Multi-Agent Collaboration Help? An Entropy Perspective": token-entropy metrics across 7 MAS architectures'
authors:
- Yuxuan Zhao
- Sijia Chen
- Ningxin Su
year: 2026
url: https://huggingface.co/datasets/AgenticFinLab/multiagent-entropy-rawdata
license: MIT
size: ~5 GB, 237 files; merged_datasets/master.csv has 44,781 rows and 254 columns
format: 'CSV (aggregated per-sample metrics) and JSON (entropy distributions, evaluation metrics)'
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Evaluation outputs behind arXiv 2602.04234 (AgenticFinLab). Compares single-agent solving with six multi-agent architectures (sequential, centralized, decentralized, fully decentralized, debate, hybrid) using Qwen3 0.6B to 14B, Llama-3.2-3B and Llama-3.1-8B, and RL-tuned variants, on GSM8K, AIME 2024/2025, MMLU, HumanEval, Math500, GAIA and Finance Agent Benchmark. Per-sample columns cover token-level entropy statistics per agent and per round, correctness, and the single-agent baseline. Raw traces (stage 1) are not included.

## Access

Public on Hugging Face, not gated, MIT; underlying benchmarks keep their own licences. Code at github.com/AgenticFinLab/multiagent-entropy.

## Relevance to us

Background on when topology helps or hurts small open-model collectives; no adversarial or identity signal.
