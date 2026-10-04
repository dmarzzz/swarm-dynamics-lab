---
id: cook-2024-artificial
type: paper
title: 'Artificial Generational Intelligence: Cultural Accumulation in Reinforcement
  Learning'
authors:
- Jonathan Cook
- Chris Lu
- Edward Hughes
- Joel Z. Leibo
- Jakob Foerster
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2406.00392
doi: null
arxiv: '2406.00392'
cite: 'Cook, J., Lu, C., Hughes, E., Leibo, J. Z., & Foerster, J. (2024). Artificial
  Generational Intelligence: Cultural Accumulation in Reinforcement Learning. arXiv:2406.00392v2.'
topics:
- marl-emergence
- llm-agent-swarms
added_by: vishesh/codex-pi-review
accessed: '2026-10-04'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

The authors study intergenerational transmission combined with independent exploration in reinforcement learning. They report accumulation exceeding a single lifetime with matched cumulative experience, and distinguish episodic in-context transmission from training-time changes in weights.

## Contribution

A controlled distinction between accumulated learning and additional lifetime experience.

## Key results

The abstract reports improvement over the matched-experience comparator; effect sizes and replication were not audited in this pass.

## Methods and models

Episodic and train-time generations. Abstract v2 read; no implementation run.

## Limitations and open questions

RL evidence is not evidence of cultural accumulation in our LLM simulation. This pass did not inspect the full methods.

## Relevance to us

For Theseus, first demonstrate acquisition, then compare inherited information with an equal-experience individual. This is a prospective design analogy. See [[bertalanic-2026-ringelmann]] for a separate caution about nominal population size.
