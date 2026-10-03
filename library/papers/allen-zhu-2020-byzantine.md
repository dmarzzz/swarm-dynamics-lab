---
id: allen-zhu-2020-byzantine
type: paper
title: Byzantine-Resilient Non-Convex Stochastic Gradient Descent
authors:
- Zeyuan Allen-Zhu
- Faeze Ebrahimian
- Jerry Li
- Dan Alistarh
year: 2020
venue: arXiv preprint
url: https://arxiv.org/abs/2012.14368
doi: null
arxiv: '2012.14368'
cite: 'Allen-Zhu, Z., Ebrahimian, F., Li, J., & Alistarh, D. (2020). Byzantine-Resilient Non-Convex Stochastic Gradient Descent. arXiv preprint arXiv:2012.14368.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Extends Byzantine-resilient distributed SGD to non-convex objectives with an alpha-fraction of Byzantine machines. SafeguardSGD uses a concentration-based filtering technique to escape saddle points and find approximate local minima, with sample and time complexity matching the best known bounds for the Byzantine-free stochastic distributed setting. The authors report it beats prior methods when training deep networks and is the first method to withstand two recently proposed Byzantine attacks.

## Contribution

Non-convex counterpart of [[alistarh-2018-byzantine]], using filtering over accumulated history rather than per-round robust aggregation.

## Key results

- Proved (per abstract): escapes saddle points and finds approximate local minima with complexity matching Byzantine-free bounds.
- Measured (per abstract): withstands two recent attacks (likely [[baruch-2019-little]] and [[xie-2019-fall]]; not checked in the body).

## Methods and models

Concentration filtering of machines over time. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; the identity of the two attacks is inferred.

## Relevance to us

Q2. The design idea that transfers is history-based filtering: track each sub-agent's cumulative contributions and drop those whose accumulated behaviour deviates beyond a concentration bound, rather than judging each merge alone. That requires persistent sub-agent identities across merges, which pulls against the Q1 idea of hiding which part returns. Related: [[karimireddy-2020-learning]].
