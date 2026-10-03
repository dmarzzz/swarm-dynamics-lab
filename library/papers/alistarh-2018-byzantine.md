---
id: alistarh-2018-byzantine
type: paper
title: Byzantine Stochastic Gradient Descent
authors:
- Dan Alistarh
- Zeyuan Allen-Zhu
- Jerry Li
year: 2018
venue: arXiv preprint
url: https://arxiv.org/abs/1803.08917
doi: null
arxiv: '1803.08917'
cite: 'Alistarh, D., Allen-Zhu, Z., & Li, J. (2018). Byzantine Stochastic Gradient Descent. arXiv preprint arXiv:1803.08917.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Studies distributed stochastic optimisation where an alpha-fraction of m machines are Byzantine. Gives an SGD variant that finds epsilon-approximate minimisers of convex functions in T = O~(1/(epsilon^2 m) + alpha^2/epsilon^2) iterations, compared with O(1/(epsilon^2 m)) for ordinary mini-batch SGD which tolerates no Byzantine machines. A matching lower bound shows the algorithm is information-theoretically optimal in sample and time complexity up to log factors.

## Contribution

A tight price of Byzantine robustness: the extra cost scales with alpha^2, and the lower bound says no algorithm can do better.

## Key results

- Proved (per abstract): upper bound T = O~(1/(epsilon^2 m) + alpha^2/epsilon^2).
- Proved (per abstract): matching lower bound up to logarithmic factors.
- Inferred from the bound: once alpha is constant, adding machines stops helping, since the alpha^2/epsilon^2 term does not shrink with m.

## Methods and models

Convex setting with an alpha-fraction of Byzantine machines among m. Only the abstract was read; the algorithm details were not checked.

## Limitations and open questions

Convex losses only; non-convex follow-up is [[allen-zhu-2020-byzantine]].

## Relevance to us

Q2. A quantitative answer to "can more forks buy safety": with a fixed corrupted fraction, the error floor set by the adversary does not fall as n grows, so a parent cannot outvote a constant fraction of corrupted sub-agents by spawning more. Robustness has to come from lowering alpha (harder corruption, diversity, hiding which parts return) rather than raising n. Survey context: [[guerraoui-2024-byzantine]].
