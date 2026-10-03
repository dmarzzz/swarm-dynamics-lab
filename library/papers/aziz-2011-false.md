---
id: aziz-2011-false
type: paper
title: 'False-Name Manipulations in Weighted Voting Games'
authors:
- 'H. Aziz'
- 'Y. Bachrach'
- 'E. Elkind'
- 'M. Paterson'
year: 2011
venue: 'Journal of Artificial Intelligence Research'
url: https://api.openalex.org/works/doi:10.1613/jair.3166
doi: 10.1613/jair.3166
arxiv: null
cite: 'Aziz, H., Bachrach, Y., Elkind, E., & Paterson, M. (2011). False-Name Manipulations in Weighted Voting Games. Journal of Artificial Intelligence Research, 40, 57-93.'
topics:
- sybil-resistance
- collective-decision
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 'OpenAlex 2026-10-03: 31'
code: []
---

## Summary

In weighted voting games a coalition wins if its weight meets a quota, and power is measured by the Shapley-Shubik or Banzhaf index rather than by weight. The paper studies how much a player can change its power by splitting its weight among several identities. It gives upper and lower bounds on the effect of splitting for both indices, shows that deciding whether a beneficial split exists is NP-hard, gives algorithms for restricted cases and randomized algorithms for the general case with an experimental evaluation, and analyses annexation and merging, including a new Annexation Non-monotonicity Paradox for the Banzhaf index.

## Contribution

Quantifies Sybil splitting in weighted voting and shows that finding a profitable split is computationally hard.

## Key results

- Upper and lower bounds on power change from weight-splitting for Shapley-Shubik and Banzhaf (abstract).
- Deciding whether a beneficial split exists is NP-hard (abstract).
- Annexation Non-monotonicity Paradox for the Banzhaf index (abstract).

## Methods and models

Weighted voting games, power indices, complexity analysis, randomized algorithms and experiments.

## Limitations and open questions

Abstract-level read; specific bound values are not recorded.

## Relevance to us

Stake-weighted voting among agents (validator committees, DAO-like agent governance) is a weighted voting game; splitting stake across agents changes power non-proportionally. NP-hardness is a weak shield against LLM agents that can search or simulate. Related: [[conitzer-2010-using]], [[ohta-2008-anonymity]].
