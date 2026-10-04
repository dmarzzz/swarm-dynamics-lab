---
id: azouvi-2021-private
type: paper
title: Private Attacks in Longest Chain Proof-of-stake Protocols with Single Secret Leader Elections
authors: [Sarah Azouvi, Daniele Cappelletti]
year: 2021
venue: Proceedings of the 3rd ACM Conference on Advances in Financial Technologies (AFT 2021)
url: https://arxiv.org/abs/2109.07440
doi: 10.1145/3479722.3480996
arxiv: '2109.07440'
cite: Azouvi, S., & Cappelletti, D. (2021). Private attacks in longest chain proof-of-stake protocols with single secret leader elections. Proceedings of the 3rd ACM Conference on Advances in Financial Technologies (AFT '21), 170-182.
topics: [fork-merge-security, sync-consensus]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 11 (Crossref, 2026-10-03)
code: []
---

## Summary

Azouvi and Cappelletti quantify what Single Secret Leader Election buys in longest-chain proof-of-stake compared with Probabilistic Leader Election, where one leader is elected only in expectation. Against the private attack (an adversary secretly builds a competing chain), SSLE cuts settlement time by roughly 25% for a 33% or 25% adversary. Against grinding attacks, the security threshold rises from 0.26 (PLE) to 0.36 (SSLE) and settlement time falls by about 70% for a 20% adversary.

## Contribution

Turns the qualitative case for exactly-one hidden leader into numbers on settlement time and adversary thresholds.

## Key results

- Private attack: about 25% faster settlement with SSLE at 25% and 33% adversarial stake (abstract).
- Grinding: tolerated adversary fraction 0.26 to 0.36; about 70% faster settlement at 20% adversary (abstract).

## Methods and models

Probabilistic analysis of longest-chain growth under SSLE versus PLE (not read beyond the abstract).

## Limitations and open questions

Only the abstract was read; the model is specific to longest-chain PoS.

## Relevance to us

Q2, and the cost side of Q1. The paper is evidence that the choice of hidden-selection rule changes the adversary threshold itself (0.26 versus 0.36), so hiding and thresholds are not independent design axes. For a fork-merge agent, the analogue is that "exactly one hidden returner per round" versus "each part returns with some probability" changes how large a corrupted fraction the parent can tolerate. Theory: [[boneh-2020-single]]; empirical comparison: [[burianova-2025-secret]].
