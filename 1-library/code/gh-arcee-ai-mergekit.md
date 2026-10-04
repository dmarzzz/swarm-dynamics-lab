---
id: gh-arcee-ai-mergekit
type: code
title: 'mergekit: toolkit for merging pretrained LLM weights (linear, SLERP, task arithmetic, TIES, DARE, DELLA, MoE)'
repo: arcee-ai/mergekit
url: https://github.com/arcee-ai/mergekit
authors: [Arcee AI, Charles Goddard]
year: 2023
language: Python
license: LGPL-3.0
stars: 7387
last_commit: 2026-09-12
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [ilharco-2023-editing]
---

## Summary

mergekit is the most widely used open tool for merging LLM checkpoints in weight space, maintained by Arcee AI. It runs out of core so merges fit on CPU or 8 GB of VRAM. The README's method table lists linear averaging, SLERP, NuSLERP, Multi-SLERP, Karcher mean, task arithmetic (task vectors relative to a base, [[ilharco-2023-editing]]), TIES (sparsify plus sign consensus), DARE (random pruning and rescaling), DELLA, Model Breadcrumbs (drop small and large outliers), SCE, Model Stock, Nearswap, Arcee Fusion and passthrough, plus LoRA extraction, mixture-of-experts assembly, evolutionary merge search and multi-stage merges. Merges are specified as YAML with per-model weights and an optional base model.

## What it can do for us

Q2: this is the "merge back" operator for parametric children in practice, so it defines what an attacker is up against. Several methods contain primitive robustness steps (TIES sign election is a per-coordinate majority vote; Breadcrumbs removes the largest deltas, which resembles trimming), yet measured attacks reach near-100% success through them with one malicious model ([[gh-aojiaosaiban-merge-hijacking]] vendors mergekit for exactly this). An experiment could add a Byzantine-robust merge method (coordinate median or trimmed mean of task vectors, as in [[gh-lpd-epfl-byzfl]]) to mergekit's method registry and test whether it raises the number of malicious models needed. That is an open question I did not find answered in this lane's sources.

## Run notes

Not run. Install from the repository with pip; merges via `mergekit-yaml config.yml ./output`. CPU-only works for small models.

## Limitations

LGPL-3.0. Merging assumes compatible architectures and usually a shared base model, which a fork-merge design satisfies by construction. The README describes no security checks on input checkpoints.
