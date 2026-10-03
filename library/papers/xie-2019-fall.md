---
id: xie-2019-fall
type: paper
title: 'Fall of Empires: Breaking Byzantine-tolerant SGD by Inner Product Manipulation'
authors:
- Cong Xie
- Sanmi Koyejo
- Indranil Gupta
year: 2019
venue: arXiv preprint
url: https://arxiv.org/abs/1903.03936
doi: null
arxiv: '1903.03936'
cite: 'Xie, C., Koyejo, S., & Gupta, I. (2019). Fall of Empires: Breaking Byzantine-tolerant SGD by Inner Product Manipulation. arXiv preprint arXiv:1903.03936.'
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

Breaks two widely used Byzantine-tolerant aggregation rules for synchronous SGD, coordinate-wise median and Krum, with attacks that manipulate the inner product between the aggregated update and the true gradient. The abstract states the breaks are proved theoretically and validated empirically. Inferred, not checked in the body: the attack targets the sign of the inner product, so the aggregate can point away from the true descent direction even when it stays close to honest vectors.

## Contribution

Inner product manipulation attack against median and Krum, two of the main robust rules of the time.

## Key results

- Claimed (abstract): coordinate-wise median and Krum broken by inner product manipulation, with theory and experiments.

## Methods and models

Attack construction and analysis against median and Krum. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; attack magnitudes and settings not checked.

## Relevance to us

Q3. The merge-poisoning analogue: corrupted sub-agents need not make the parent's merged state look far from honest contributions, only push it in a chosen direction. Together with [[baruch-2019-little]] and [[el-mhamdi-2018-hidden]] it shows that "close to the majority" is a weak acceptance test for returning parts. Defends against: [[blanchard-2017-byzantine]], [[yin-2018-byzantine]].
