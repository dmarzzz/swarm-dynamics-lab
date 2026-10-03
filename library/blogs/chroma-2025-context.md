---
id: chroma-2025-context
type: blog
title: 'Context Rot: How Increasing Input Tokens Impacts LLM Performance'
authors:
- Kelly Hong
- Anton Troynikov
- Jeff Huber
year: 2025
url: https://www.trychroma.com/research/context-rot
site: Chroma
topics:
- llm-agent-swarms
- criticality-measurement
added_by: vishesh/codex-methods
accessed: '2026-10-03'
read_depth: skim
relevance: 4
---

## Summary

This technical report evaluates how context length and presentation affect retrieval and repetition tasks. Across 18 models it reports nonuniform long-context behavior and studies lexical similarity, distractors and document structure rather than treating nominal context capacity as reliable performance.

## Key claims

Changing context structure and similarity changes results; the report cautions that two topical haystacks cannot establish a general similarity rule.

## Evidence quality

First-party experiments with released code. Introduction, selected results and figure descriptions, limitations and conclusion skimmed; all figures and methods were not fully audited.

## Relevance to us

Useful for SOC-21 and SOC-31 controls. Context length, repetition and ordering must be varied separately. See [[modarressi-2025-nolima]].
