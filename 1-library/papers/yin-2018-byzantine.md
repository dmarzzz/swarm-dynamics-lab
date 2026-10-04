---
id: yin-2018-byzantine
type: paper
title: 'Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates'
authors:
- Dong Yin
- Yudong Chen
- Kannan Ramchandran
- Peter Bartlett
year: 2018
venue: ICML 2018 (arXiv preprint)
url: https://arxiv.org/abs/1803.01498
doi: null
arxiv: '1803.01498'
cite: 'Yin, D., Chen, Y., Ramchandran, K., & Bartlett, P. (2018). Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates. arXiv preprint arXiv:1803.01498.'
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

Analyses two robust distributed gradient descent algorithms that aggregate worker gradients by coordinate-wise median and by coordinate-wise trimmed mean, when some workers are Byzantine. The authors prove statistical error rates for strongly convex, non-strongly convex and smooth non-convex losses, and show the rates are order-optimal for strongly convex losses. For communication efficiency they also give a one-round median-based algorithm that matches the optimal rate for strongly convex quadratic losses.

## Contribution

Puts robust statistics (median and trimmed mean, descendants of [[huber-1964-robust]]) on a sharp statistical footing for Byzantine distributed learning.

## Key results

- Proved (per abstract): error rates for median and trimmed mean GD across three loss classes, order-optimal for strongly convex losses.
- Proved (per abstract): a one-round median algorithm with the same optimal rate for strongly convex quadratics.
- Not checked: the exact dependence on the Byzantine fraction alpha (stated in the paper body).

## Methods and models

Coordinate-wise median and beta-trimmed mean aggregation; statistical analysis under data split across machines. Only the abstract was read.

## Limitations and open questions

Coordinate-wise rules are the targets of [[xie-2019-fall]]; analysis assumes honest data drawn i.i.d.

## Relevance to us

Q2. The trimmed mean is the simplest k-of-n style merge rule: drop the most extreme fraction of each coordinate on each side, average the rest. It gives a known tolerance for a Byzantine fraction below one half, and an error that grows with that fraction, which is the shape of guarantee a parent could hope for when merging numeric state from sub-agents. It has no obvious analogue for merging free-text memories. Related: [[blanchard-2017-byzantine]], [[leblanc-2013-resilient]] (W-MSR uses the same trimming idea in consensus).
