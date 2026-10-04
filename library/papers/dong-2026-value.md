---
id: dong-2026-value
type: paper
title: 'Value of Information: A Framework for Human-Agent Communication'
authors:
- Yijiang River Dong
- Tiancheng Hu
- Zheng Hui
- Caiqi Zhang
- Ivan Vulić
- Andreea Bobu
- Nigel Collier
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2601.06407
doi: null
arxiv: '2601.06407'
cite: 'Dong, Y. R., Hu, T., Hui, Z., Zhang, C., Vulić, I., Bobu, A., & Collier, N.
  (2026). Value of Information: A Framework for Human-Agent Communication. arXiv:2601.06407.'
topics:
- agent-budgets
- decision-models
added_by: vishesh/codex-pi-review
accessed: '2026-10-04'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

The authors frame clarification as purchasing information: ask when its expected decision benefit exceeds interaction cost. They compare this approach with fixed-round and confidence-threshold methods on decision tasks with different stakes and ambiguity.

## Contribution

Connects information acquisition to downstream utility, instead of optimizing uncertainty reduction alone.

## Key results

The abstract reports competitive or improved utility across four domains. This pass does not endorse medical deployment or reproduce those results.

## Methods and models

Abstract plus HTML introduction, formulation and calibration subsection inspected; conservatively abstract depth. Beliefs and possible user responses are model-estimated.

## Limitations and open questions

The calibration section lacks ground-truth distributions and uses argmax calibration as a proxy; do not treat estimated beliefs as known probabilities. Domain counts in the abstract and displayed setup deserve full-text reconciliation before quantitative reuse.

## Relevance to us

Phantom's next worthwhile question may concern acquiring uncertain reliability evidence. Use a Bayesian controller with the same observations; keep true-calibration oracle separate.
