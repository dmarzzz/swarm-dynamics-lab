---
id: liu-2026-contagion
title: 'Contagion Networks: Evaluator Preference Propagation in Multi-Agent LLM Systems'
authors:
- Zewen Liu
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.20493
doi: null
arxiv: '2606.20493'
type: paper
topics:
- fork-merge-security
- llm-agent-swarms
added_by: shadow/sol-g74
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
cite: 'Zewen Liu. (2026). Contagion Networks: Evaluator Preference Propagation in
  Multi-Agent LLM Systems. arXiv preprint. arXiv:2606.20493.'
---

## Summary

This framework measures how evaluator preferences, including shared model priors, propagate through agent interactions. A controlled three-agent experiment and topology/committee comparisons suggest evaluator-induced preferences can cascade without an adversarial worm.

## Contribution

Analysis of propagation, lifecycle security, containment or trust-boundary assessment.

## Key results

The abstract reports cross-agent coefficients 0.157-0.352 and a 68.9% +/- 14.1% decrease in effective contagion when evaluator committee size increases from one to three, using four seeds. This is preference propagation, not malicious-code execution or an adversarial threshold proof.

## Methods and models

Primary arXiv abstract and metadata read.

## Limitations and open questions

Full methods and uncertainties were not checked; do not infer cross-agent infection merely from persistent memory compromise.

## Relevance to us

Important comparator for separating benign shared bias from hostile contagion in a parent aggregator. Compare [[ebrahimi-2025-adversary]] and [[niu-2026-reliability-contagion]].
