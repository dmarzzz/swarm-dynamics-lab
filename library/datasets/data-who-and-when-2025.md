---
id: data-who-and-when-2025
type: dataset
title: 'Who&When: 184 multi-agent failure logs annotated with the responsible agent, the decisive error step and an explanation'
authors:
- Shaokun Zhang
- Ming Yin
- Jieyu Zhang
- Jiale Liu
- Zhiguang Han
- Jingyang Zhang
- Beibin Li
- Chi Wang
- Huazheng Wang
- Yiran Chen
year: 2025
url: https://huggingface.co/datasets/Kevin355/Who_and_When
license: unspecified
size: 184 rows, 1,895,065 bytes
format: 'Parquet, two configs: Algorithm-Generated and Hand-Crafted'
topics:
- llm-agent-swarms
- fork-merge-security
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers:
- zhang-2025-which
---

## Summary

Benchmark for automated failure attribution from [[zhang-2025-which]] (arXiv 2505.00212). 184 failed tasks from algorithm-generated agent systems built with CaptainAgent and from hand-crafted systems such as Magentic-One, on queries from GAIA and AssistantBench. Each failure is labelled with the agent responsible ("who"), the decisive error step ("when") and a natural-language explanation.

## Access

Public on Hugging Face, not gated. No licence tag on the repo, so terms are unclear.

## Relevance to us

Ground truth for "which sub-agent broke the collective and at what step", the same question a fork-merge parent must answer before reintegrating a child. Small but directly usable as an attribution eval; see also [[data-mast-2025]] and [[data-trail-2025]].
