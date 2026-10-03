---
id: margalit-2026-governed
type: paper
title: 'Governed Shared Memory for Multi-Agent LLM Systems'
authors: [Yanki Margalit, Nurit Cohen-Inger, Erni Avram, Ran Taig, Oded Margalit]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.24535
doi: null
arxiv: '2606.24535'
cite: 'Margalit, Y., Cohen-Inger, N., Avram, E., Taig, R., & Margalit, O. (2026). Governed Shared Memory for Multi-Agent LLM Systems. arXiv preprint arXiv:2606.24535.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 9  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

The paper formalises the "fleet-memory problem" for multi-agent LLM systems and names four failure modes: unauthorised leakage, stale propagation, contradiction persistence and provenance collapse. It defines primitives against them (scoped retrieval, temporal supersession, provenance tracking, policy-governed propagation) and implements them in MemClaw, a production multi-tenant memory service. It then measures the live service with a harness called ArgusFleet. Measured (abstract): depth-four derivation chains were reconstructed with the correct writer identity in 100% of cases at sub-second per-hop latency. There was zero cross-fleet leakage. Two production bugs were found. Sub-tenant scope could be bypassed on direct get-by-id requests (disclosed and fixed during the study). And a synchronous near-duplicate gate rejected contradictory writes before the asynchronous contradiction detector could evaluate them.

## Contribution

A systems-level account, measured on a live service, of what governed shared memory needs, including negative results.

## Key results

- 100% reconstruction of depth-four provenance chains (abstract).
- Zero cross-fleet leakage, but a sub-tenant scope bypass existed (abstract).
- A pipeline-ordering conflict between deduplication and contradiction detection (abstract).

## Methods and models

Measurement of a live production service. No baseline comparison, by design.

## Limitations and open questions

Abstract only. It is not an adversarial poisoning evaluation, and it is authored around the authors' own product.

## Relevance to us

For Q2, the pipeline-ordering finding is a concrete merge hazard. If a parent deduplicates incoming sub-agent memories before checking for contradictions, a corrupted sub-agent that writes first can block honest contradicting reports as "near duplicates". Write order then becomes an attack surface (inferred from the reported failure). Provenance chains with writer identity are the bookkeeping that any k-of-n merge rule needs. Related: [[zhan-2026-when]], [[xiong-2026-maple]], [[ravindran-2026-portable]].
