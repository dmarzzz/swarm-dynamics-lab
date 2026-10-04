---
id: data-mast-2025
type: dataset
title: 'MAD: Multi-Agent System Traces Dataset, 1,642 MAS execution traces annotated with the 14 MAST failure modes'
authors:
- Mert Cemri
- Melissa Z. Pan
- Shuyi Yang
- Lakshya A. Agrawal
- Bhavya Chopra
- Rishabh Tiwari
- Kurt Keutzer
- Aditya Parameswaran
- Dan Klein
- Kannan Ramchandran
- Matei Zaharia
- Joseph E. Gonzalez
- Ion Stoica
year: 2025
url: https://huggingface.co/datasets/mcemri/MAST-Data
license: CC-BY-4.0
size: 1,661 rows (1,642 annotated traces plus 19 inter-annotator rows), 191,460,395 bytes
format: 'JSON: MAD_full_dataset.json and MAD_human_labelled_dataset.json; fields mas_name, llm_name, benchmark_name, trace_id, trace, mast_annotation'
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers:
- cemri-2025-why
---

## Summary

Execution traces released with [[cemri-2025-why]] (NeurIPS 2025). 1,642 traces from 7 multi-agent frameworks (AG2, MetaGPT, ChatDev, Magentic, AppWorld, HyperAgent, OpenManus) across 8 benchmarks (ProgramDev, GSM, Olympiad, GAIA, MMLU, SWE-Bench-Lite and others) and 5 LLMs (GPT-4o, GPT-4o-mini, Claude, Qwen, CodeLlama). Each trace carries binary labels for 14 failure modes in three groups: specification, inter-agent misalignment, task verification. The card states the labels come from an LLM judge; a separate 19-row file holds the three-annotator agreement study.

## Access

Public on Hugging Face, no gating, CC-BY-4.0. Code at github.com/multi-agent-systems-failure-taxonomy/MAST.

## Relevance to us

The largest labelled corpus of multi-agent LLM failures, with inter-agent misalignment codes (information withholding, ignored input) that resemble what a corrupted sub-agent would look like. Pairs with [[data-who-and-when-2025]] for attribution.
