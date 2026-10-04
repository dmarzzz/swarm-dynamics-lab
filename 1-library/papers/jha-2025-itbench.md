---
id: jha-2025-itbench
type: paper
title: 'ITBench: Evaluating AI Agents across Diverse Real-World IT Automation Tasks'
authors:
- Saurabh Jha
- Rohan Arora
- Yuji Watanabe
- Takumi Yanagawa
- Yinfang Chen
- Jackson Clark
- Bhavya Bhavya
- Mudit Verma
- Harshit Kumar
- Hirokuni Kitahara
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2502.05352
doi: null
arxiv: '2502.05352'
cite: 'Jha, S., Arora, R., Watanabe, Y., Yanagawa, T., Chen, Y., Clark, J., Bhavya,
  B., Verma, M., Kumar, H., Kitahara, H., et al. (2025). ITBench: Evaluating AI Agents
  across Diverse Real-World IT Automation Tasks. arXiv:2502.05352.'
topics:
- llm-agent-swarms
- decision-models
added_by: vishesh/codex-pi-review
accessed: '2026-10-04'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

ITBench defines executable IT automation scenarios with separate environment, triggers, ground truth and desired outcomes. Its initial 94 scenarios cover SRE, compliance and cost management. Agents interact with partially observed systems; evaluation distinguishes diagnosis from mitigation.

## Contribution

Operational task construction with machine-checkable system outcomes rather than plausible textual diagnoses alone.

## Key results

Scenario coverage is 42 SRE, 50 compliance and two cost-management cases. These are the benchmark's counts, not our samples.

## Methods and models

Read abstract and HTML sections 1–3 through baseline-agent design. Conservatively classified abstract: figures, conclusions and full evaluation were not audited. Author list stores first ten; citation explicitly uses et al.

## Limitations and open questions

Uneven domain coverage; no local reproduction. A lightweight simulation inspired by its schema is not an ITBench replication.

## Relevance to us

Immune Response should distinguish alert clearance, actual recovery, unnecessary changes and collateral service loss. Borrow scenario semantics before expensive orchestration infrastructure.
