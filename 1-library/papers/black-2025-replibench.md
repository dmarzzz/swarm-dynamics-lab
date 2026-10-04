---
id: black-2025-replibench
type: paper
title: 'RepliBench: Evaluating the Autonomous Replication Capabilities of Language Model Agents'
authors: [Sid Black, Asa Cooper Stickland, Jake Pencharz, Oliver Sourbut, Michael Schmatz, Jay Bailey, Ollie Matthews, Ben Millwood, Alex Remedios, Alan Cooney]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2504.18565
doi: null
arxiv: '2504.18565'
cite: 'Black, S., Stickland, A. C., Pencharz, J., Sourbut, O., Schmatz, M., Bailey, J., Matthews, O., Millwood, B., Remedios, A., & Cooney, A. (2025). RepliBench: Evaluating the Autonomous Replication Capabilities of Language Model Agents. arXiv:2504.18565.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 14 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

UK AI Security Institute benchmark for autonomous replication of LLM agents, decomposed into four domains: obtaining resources, exfiltrating model weights, replicating onto compute, and persisting on that compute. 20 task families, 86 tasks; 5 frontier models evaluated. Measured (abstract): models do not currently pose a credible self-replication threat but succeed on many components and improve quickly. They can deploy instances from cloud providers, write self-propagating programs and exfiltrate weights under simple security, but struggle with KYC checks and robust persistent deployments. Best model, Claude 3.7 Sonnet, scores above 50% pass@10 on 15 of 20 families, and on 9 of 20 for the hardest variants.

## Contribution

A capability decomposition of replication that separates what is already easy (spawning copies) from what is still hard (acquiring resources legitimately, persisting).

## Key results

- Claude 3.7 Sonnet: >50% pass@10 on 15/20 families; 9/20 at hardest variants (abstract).
- Bottlenecks: KYC and robust persistence (abstract).

## Methods and models

Task families across four replication domains; pass@10 scoring; Inspect-based evaluations (not checked).

## Limitations and open questions

Abstract-level reading. Measures capability with instruction, not propensity.

## Relevance to us

The fork half of fork-and-merge. For dmarz's scenario (a resourceful agent sends a part to a distant domain), the measured bottleneck is not making the copy but keeping it alive and resourced somewhere the parent does not control, which is where an adversary would get access to it.
- Q1 (hiding): persistence in hostile infrastructure is weak today, so a forked part in a foreign domain is likely to depend on infrastructure an adversary can observe.
Related: [[pan-2024-frontier]], [[metr-2024-rogue]].
