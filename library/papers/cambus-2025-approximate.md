---
id: cambus-2025-approximate
type: paper
title: Approximate Agreement Algorithms for Byzantine Collaborative Learning
authors:
- Melanie Cambus
- Darya Melnyk
- Tijana Milentijevic
- Stefan Schmid
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2504.01504
doi: null
arxiv: '2504.01504'
cite: 'Cambus, M., Melnyk, D., Milentijevic, T., & Schmid, S. (2025). Approximate Agreement Algorithms for Byzantine Collaborative Learning. arXiv preprint arXiv:2504.01504.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

In peer-to-peer Byzantine collaborative learning there is no central server, so Byzantine clients can make honest clients see different sets of gradients; aggregation must therefore be combined with an approximate agreement subroutine. The authors show known approaches give no guarantee on convergence or gradient quality inside that subroutine for the geometric median rule, propose a hyperbox algorithm that does, and report that geometric-median-based aggregation tolerates sign-flip attacks on non-i.i.d. data better than mean-based methods, in centralized and decentralized settings.

## Contribution

Connects the classical approximate agreement problem [[dolev-1986-reaching]] to robust aggregation rules from Byzantine ML such as the geometric median.

## Key results

- Reported in abstract: existing approaches lack guarantees in the agreement subroutine for geometric median aggregation.
- Reported in abstract: hyperbox algorithm restores guarantees; geometric median beats mean-based methods under sign-flip attacks.

## Methods and models

Hyperbox approximate agreement over vectors; experiments on non-i.i.d. data. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; numbers not checked.

## Relevance to us

Q2, for the decentralised case. If sibling sub-agents must agree among themselves on what to merge before the parent sees it (no trusted merger), the problem becomes multidimensional approximate agreement, with the thresholds of [[dolev-1986-reaching]] rather than those of a trusted aggregator like [[blanchard-2017-byzantine]].
