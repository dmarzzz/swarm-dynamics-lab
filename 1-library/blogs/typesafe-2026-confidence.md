---
id: typesafe-2026-confidence
type: blog
title: Confidence
authors:
- TypeSafe AI
year: 2026
url: https://docs.typesafe.ai/confidence
site: TypeSafe AI
read_depth: skim
topics:
- decision-models
- llm-agent-swarms
added_by: vishesh/codex-decision-models
accessed: '2026-10-04'
relevance: 5
---

## Summary

The vendor describes how to interpret the confidence and probability signals returned by typed decisions. These are inputs to a caller-owned policy, so a threshold and the behavior after rejection need separate task-level evaluation.

## Key claims

Interface guidance and vendor claims, not independent validation. Current docs publish the Choice and Score formulas; Noul has no separate confidence field. Do not confuse distribution concentration with validated correctness.

## Evidence quality

Primary vendor documentation; runtime behavior has not been independently reproduced.

## Relevance to us

Freeze the version, request semantics and uncertainty policy before a comparison.
