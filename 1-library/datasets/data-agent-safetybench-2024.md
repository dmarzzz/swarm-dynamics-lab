---
id: data-agent-safetybench-2024
type: dataset
title: 'Agent-SafetyBench: 2,000 test cases over 349 interaction environments for LLM agent safety'
authors: [Zhexin Zhang, Shiyao Cui, Yida Lu, Jingzhuo Zhou, Junxiao Yang, Hongning Wang, Minlie Huang]
year: 2024
url: https://huggingface.co/datasets/thu-coai/Agent-SafetyBench
license: MIT
size: 2,000 test cases, 349 environments (one file, released_data.json)
format: JSON (released_data.json)
topics: [fork-merge-security]
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Benchmark data for Agent-SafetyBench (arXiv 2412.14470, Tsinghua CoAI; HF upload 2025-08-11). Per the abstract it has 349 interaction environments and 2,000 test cases covering 8 categories of safety risk and 10 failure modes. Evaluating 16 popular LLM agents, none scored above 60% on safety; the authors name lack of robustness and lack of risk awareness as the two main defects and find defence prompts alone insufficient. The card itself is short and points to the GitHub repo for evaluation code.

## Access

Public, ungated, on Hugging Face. MIT. Not downloaded here.

## Relevance to us

Single-agent safety benchmark; background for which unsafe actions a lone agent takes before we add swarms. See [[data-dtap-bench-2026]] for a larger, newer suite.
