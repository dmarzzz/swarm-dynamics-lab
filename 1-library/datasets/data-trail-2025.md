---
id: data-trail-2025
type: dataset
title: 'TRAIL: 148 human-annotated agent traces (GAIA and SWE-bench) for trace reasoning and agentic issue localization'
authors:
- Darshan Deshpande
- Varun Gangal
- Hersh Mehta
- Jitin Krishnan
- Anand Kannappan
- Rebecca Qian
year: 2025
url: https://huggingface.co/datasets/PatronusAI/TRAIL
license: MIT
size: 148 traces (gaia split 117, swe_bench split 31), 186,422,862 bytes (54,643,931 bytes download)
format: 'Parquet; two string columns, trace and labels'
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Patronus AI release for arXiv 2505.08638, "TRAIL: Trace Reasoning and Agentic Issue Localization". The card body is behind the gate; facts here are from the HF metadata and the arXiv abstract. 148 human-annotated traces from single and multi-agent systems on GAIA (117) and SWE-bench (31), labelled with a formal taxonomy of agentic error types. The abstract reports that the best model tested, Gemini-2.5-pro, scored 11% on trace debugging.

## Access

Gated (automatic approval) on Hugging Face; the gate asks users not to reshare outside a gated or private repo to avoid contamination. MIT tag.

## Relevance to us

A small, human-labelled error-localization benchmark for agent traces; useful as a hard eval next to [[data-who-and-when-2025]] and [[data-mast-2025]], though only part of it is multi-agent.
