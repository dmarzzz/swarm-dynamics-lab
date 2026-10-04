---
id: ouyang-2026-memlineage
type: paper
title: 'MemLineage: Lineage-Guided Enforcement for LLM Agent Memory'
authors:
- Ciyan Ouyang
- Rui Hou
year: 2026
venue: arXiv
url: https://arxiv.org/html/2605.14421v1
doi: null
arxiv: '2605.14421'
cite: 'Ouyang, Ciyan; Hou, Rui. (2026). MemLineage: Lineage-Guided Enforcement for
  LLM Agent Memory. arXiv:2605.14421.'
topics:
- llm-agent-swarms
- fork-merge-security
added_by: dmarz/preflight
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

MemLineage combines signed memory entries with derivation tracking and enforcement at sensitive actions. The work separates recording authentic origins from tracking how untrusted content influences later entries, using controlled memory-poisoning evaluations.

## Contribution

Carries source trust through derived memory.

## Key results

An intentionally vulnerable AgentDojo profile tests six banking pairs.

## Methods and models

Skimmed introduction, trust model, evaluation, recovery discussion and conclusion in v1.

## Limitations and open questions

Trust propagation depends on attributed edges. Denying an action alone need not restore task utility; recovery uses additional authority assumptions.

## Relevance to us

Baseline for incomplete-lineage research beside [[li-2026-memtx]].
