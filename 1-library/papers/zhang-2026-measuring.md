---
id: zhang-2026-measuring
type: paper
title: Measuring Real-World Prompt Injection Attacks in LLM-based Resume Screening
authors:
- Mohan Zhang
- Yuqi Jia
- Zhen Tan
- Steven Jiang
- Neil Zhenqiang Gong
- Tianlong Chen
- Dawn Song
year: 2026
venue: USENIX Security Symposium 2026
url: https://arxiv.org/abs/2605.28999
doi: null
arxiv: '2605.28999'
cite: Zhang, M., Jia, Y., Tan, Z., Jiang, S., Gong, N. Z., Chen, T., & Song, D. (2026). Measuring Real-World Prompt Injection Attacks in LLM-based Resume Screening. In USENIX Security Symposium 2026. arXiv:2605.28999.
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Builds detectors for hidden prompt injections in resumes and applies them to about 200,000 real resumes collected by hireEZ over several years. About 1% of resumes contain hidden prompt injections; prevalence has risen noticeably over the past one to two years; and more than 90% of injected prompts use no explicit instruction.

## Contribution

The first large-scale, in-the-wild prevalence measurement of text planted for LLM readers, the mirror image of planting canaries for LLM agents.

## Key results

- About 1% of roughly 200K resumes contain hidden injections; rising over 1-2 years; over 90% implicit (measured).

## Methods and models

Tailored injection detectors validated manually on a small set, then applied at scale. Abstract-level read.

## Limitations and open questions

Abstract only; one application domain.

## Relevance to us

Base-rate evidence that humans already seed documents for AI readers at about 1%, so a canary-based detector must expect background injected text it did not plant. Related: [[lin-2025-hidden]], [[rao-2025-detecting]].
