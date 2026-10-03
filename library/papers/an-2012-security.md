---
id: an-2012-security
type: paper
title: Security Games with Limited Surveillance
authors:
- Bo An
- David Kempe
- Christopher Kiekintveld
- Eric Shieh
- Satinder Singh
- Milind Tambe
- Yevgeniy Vorobeychik
year: 2012
venue: Proceedings of the AAAI Conference on Artificial Intelligence, 26(1), 1241-1248
url: https://ojs.aaai.org/index.php/AAAI/article/view/8236
doi: 10.1609/aaai.v26i1.8236
arxiv: null
cite: An, B., Kempe, D., Kiekintveld, C., Shieh, E., Singh, S., Tambe, M., & Vorobeychik, Y. (2012). Security Games with Limited Surveillance. Proceedings of the AAAI Conference on Artificial Intelligence, 26(1), 1241-1248.
topics:
- fork-merge-security
- collective-decision
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Drops the assumption that the attacker knows the defender's mixed strategy exactly. The attacker observes a limited number of the defender's actions, forms or updates a belief, and best-responds. The paper gives mathematical programs for optimal attacker and defender strategies at a fixed observation duration and shows how to use them to estimate observation duration. Experiments report that accounting for limited surveillance gives the defender a significant gain in expected utility (magnitude not in the abstract).

## Contribution

Models the observation channel between Stackelberg commitment and Nash play.

## Key results

- Optimal strategies for a fixed number of attacker observations (abstract).
- Significant defender gains from modelling limited surveillance (abstract; not quantified).

## Methods and models

Bayesian belief updating by the attacker, mathematical programming.

## Limitations and open questions

Abstract only.

## Relevance to us

- Q1: the question a parent should ask is how many merge rounds an attacker gets to observe before it must commit to corrupting a child. If it sees few rounds, the parent can exploit the attacker's noisy estimate; if many, the Stackelberg answer of [[korzhyk-2011-stackelberg]] applies.
Related: [[avenhaus-2002-inspection]], [[gans-2026-when-does]].
