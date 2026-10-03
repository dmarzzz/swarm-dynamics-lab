---
id: lip-2025-factor
type: paper
title: 'Factor(U,T): Controlling Untrusted AI by Monitoring their Plans'
authors: [Edward Lue Chee Lip, Anthony Channg, Diana Kim, Aaron Sandoval, Kevin Zhu]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2512.14745
doi: null
arxiv: '2512.14745'
cite: 'Lip, E. L. C., Channg, A., Kim, D., Sandoval, A., & Zhu, K. (2025). Factor(U,T): Controlling Untrusted AI by Monitoring their Plans. arXiv:2512.14745.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 0 (Semantic Scholar citing list, 2026-10-03)
code: []
---

## Summary

Factored cognition protocols split a task into child tasks: one model decomposes, others implement children in isolation. Factor(U,T) lets an untrusted strong model decompose while trusted models implement. Measured on BigCodeBench control evaluations (abstract): monitors judging only the natural-language decompositions separate malicious from honest ones barely above chance (AUROC 0.52), while monitors judging complete Python solutions reach AUROC 0.96. Factor(D,U), with a trusted decomposer and monitoring of the concrete child solutions, achieves AUROC 0.96 and 1.2% attack success.

## Contribution

Shows that malicious intent is hard to see in a plan but easy to see in its implementation, for this task family.

## Key results

- Plan-only monitoring AUROC 0.52 vs solution monitoring AUROC 0.96 (abstract).
- Trusted decomposer plus solution monitoring: 1.2% attack success (abstract).

## Methods and models

BigCodeBench; red-teamed decomposition attacks; protocol names follow Factor(decomposer, implementer).

## Limitations and open questions

Abstract-level reading; one coding benchmark.

## Relevance to us

The fork step is a decomposition. A parent that splits into sub-agents is a decomposer; the children are implementers.
- Q2/Q3: if the parent itself is the untrusted party (corrupted before splitting), monitoring its task split is nearly useless; if the children are untrusted, monitoring their concrete outputs works. For merge-back this argues for checking what each child actually produced, not the child's summary of what it did.
Related: [[makins-2026-multi]], [[greenblatt-2023-ai]], [[beurer-kellner-2025-design]].
