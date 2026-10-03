---
id: nogueira-2026-systematic
type: paper
title: A Systematic Methodology for Evaluating Failure Independence in LLM-Generated Code
authors:
- Rodrigo Pato Nogueira
- Karthik Pattabiraman
- Marco Vieira
- Joao R. Campos
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.02808
doi: null
arxiv: '2607.02808'
cite: 'Nogueira, R. P., Pattabiraman, K., Vieira, M., & Campos, J. R. (2026). A Systematic Methodology for Evaluating Failure Independence in LLM-Generated Code. arXiv preprint arXiv:2607.02808.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Proposes a methodology for testing whether LLM-generated implementations fail independently, as N-version programming requires, and applies it to 224 problems across twelve models, five languages and three prompting strategies. Implementations from the same model are structurally very similar; different models are more diverse but still fail on the same tests far more often than independence predicts. Three- and five-version majority ensembles realise only 0.43 and 0.44 of the reliability gain that independence would give, and below 0.3 when built from a single model.

## Contribution

A quantitative "fraction of the independent-failure gain actually realised" for LLM N-version ensembles, separating same-model from cross-model ensembles.

## Key results

- Reported in abstract: 3-version and 5-version ensembles realise 0.43 and 0.44 of the independence gain.
- Reported in abstract: below 0.3 when all versions come from the same model.
- Reported in abstract: manual analysis finds that even different failure patterns often share root causes.

## Methods and models

Structural diversity (code similarity) and behavioural diversity (co-failure on tests), N-version reliability under majority voting, manual fault inspection. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; benign errors only.

## Relevance to us

Q2. Gives the closest available number for a self-forking parent: replicas of one model realise under 30 percent of the gain a k-of-n vote would give with independent failures, even with no attacker. Moving from 3 to 5 versions adds almost nothing (0.43 to 0.44), which suggests raising n is a poor substitute for raising diversity. Pairs with [[ron-2026-n-version]], [[kim-2025-correlated]], [[knight-1986-experimental]].
