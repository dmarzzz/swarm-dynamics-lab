---
id: korzhyk-2011-stackelberg
type: paper
title: 'Stackelberg vs. Nash in Security Games: An Extended Investigation of Interchangeability, Equivalence, and Uniqueness'
authors:
- Dmytro Korzhyk
- Zhengyu Yin
- Christopher Kiekintveld
- Vincent Conitzer
- Milind Tambe
year: 2011
venue: Journal of Artificial Intelligence Research, 41, 297-327
url: https://arxiv.org/abs/1401.3888
doi: 10.1613/jair.3269
arxiv: '1401.3888'
cite: 'Korzhyk, D., Yin, Z., Kiekintveld, C., Conitzer, V., & Tambe, M. (2011). Stackelberg vs. Nash in Security Games: An Extended Investigation of Interchangeability, Equivalence, and Uniqueness. Journal of Artificial Intelligence Research, 41, 297-327.'
topics:
- fork-merge-security
- collective-decision
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: 145 (Crossref, 2026-10-03); 294 citing papers in Semantic Scholar
code: []
---

## Summary

Studies a defender who does not know whether the attacker can observe its randomised strategy. In security games (payoffs depend only on which target is attacked and whether it is covered), Nash equilibria are interchangeable, and under a restriction on schedules (subsets of schedules are schedules) every Strong Stackelberg strategy is also a Nash strategy, unique in an ARMOR-like class. When the attacker can hit several targets at once, these properties fail. Experiments show the Stackelberg strategy is usually still Nash outside the restriction, but not with multiple attacker resources. I read the abstract, introduction, section list and summary.

## Contribution

Resolves the defender's dilemma about observability for single-target attackers: one strategy is optimal whether or not the attacker watches.

## Key results

- Interchangeability of Nash equilibria in security games (proved).
- Under the schedule restriction, Stackelberg strategies are Nash strategies; uniqueness in a restricted class (proved).
- With multiple attacker resources the equivalences break (proved by example and shown experimentally).
- Proposes an extensive-form model with explicit uncertainty about the attacker's ability to observe.

## Methods and models

Two-player general-sum security games, Strong Stackelberg Equilibrium, minimax analysis, random-game experiments.

## Limitations and open questions

Single defender, rational attacker, tie-breaking in the defender's favour.

## Relevance to us

- Q1: if the attacker corrupts one child, the parent can choose one randomised audit or reintegration policy that is right whether or not the attacker can watch the merge protocol, so hiding the policy itself buys nothing extra; only the draw must stay secret.
- Q2: the equivalence fails when the attacker controls several resources, which is exactly the k-of-n corruption setting. A threshold merge protocol therefore needs its own analysis; the single-attacker guarantees do not transfer.
Related: [[avenhaus-2002-inspection]], [[conitzer-2006-computing]], [[an-2012-security]], [[leslie-2015-threshold]].
