---
id: gafni-2020-vcg
type: paper
title: "VCG under Sybil (False-Name) Attacks - A Bayesian Analysis"
authors: [Yotam Gafni, Ron Lavi, Moshe Tennenholtz]
year: 2020
venue: Proceedings of the 34th AAAI Conference on Artificial Intelligence (AAAI-20), New York, vol. 34, no. 2, pp. 1966-1973
url: https://arxiv.org/abs/1911.07210
doi: 10.1609/aaai.v34i02.5567
arxiv: "1911.07210"
cite: "Gafni, Y., Lavi, R., & Tennenholtz, M. (2020). VCG under Sybil (False-Name) Attacks - A Bayesian Analysis. In Proceedings of the 34th AAAI Conference on Artificial Intelligence (AAAI-20), 34(2), pp. 1966-1973. AAAI Press. https://doi.org/10.1609/aaai.v34i02.5567"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "5 (Crossref, 2026-10-03)"
code: []
---

## Summary

Revisits VCG's false-name vulnerability from a Bayesian rather than dominant-strategy angle. The bare-minimum model: two identical items, n single-minded bidders, each bidder with probability q wants a single item (value drawn from F) and with probability 1 - q wants the pair (value drawn from the matching two-item distribution); q = 1 recovers the single-item Vickrey auction, which is false-name-proof. Instead of designing a new mechanism (which, per the authors, always costs social welfare), they ask when truthful bidding is a Bayesian Nash equilibrium of VCG despite the option to split a pair bid into two single-item bids under false names. The key notion is the "granularity threshold" q*: the minimal q (share of single-minded single-item demand types) above which no false-name attack is profitable in expectation given the type distribution F, so VCG is "Bayesian resilient". Theorem 3.1: for n = 2 bidders the threshold is q* = 2/3 for any F. Theorem 4.1: for n > 2 and any q < 1 there exist an attack and a distribution F for which the attack is profitable, so no distribution-free threshold below 1 exists for larger n. Theorem 6.1: for the uniform distribution on [0,1] and any n >= 3 the threshold for the natural split attack (1, x), (1, y) is q* = 1/2, i.e. VCG remains truthful in BNE whenever at least half the demand is single-item. The paper closes with open questions on whether the split attack is always the worst case and on richer (beta, correlated) distributions. Read from the arXiv full version: abstract, introduction and positioning against false-name-proof mechanism design and against Alkalay-Houlihan and Vetta's complete-information PoA bounds, model and granularity-threshold definition, Theorems 3.1, 4.1 and 6.1 with proof overviews, conclusions; recurrences and appendices skimmed.

## Contribution

Introduces Bayesian false-name resilience and the granularity threshold, showing that VCG is often Sybil-resistant in equilibrium when enough bidders have single-item demand, without any welfare sacrifice.

## Key results

- n = 2: VCG is Bayesian resilient to false-name attacks iff q >= 2/3, for any F (Theorem 3.1).
- n > 2: no universal threshold below 1 (Theorem 4.1).
- Uniform F, n >= 3: split attack unprofitable iff q >= 1/2 (Theorem 6.1).

## Methods and models

Two-item single-minded combinatorial auction, i.i.d. Bayesian types with demand-type probability q, truthful BNE analysis of VCG under identity splitting, closed-form and recurrence-based expected-utility comparisons.

## Limitations and open questions

Minimal model (two items, single-minded, symmetric i.i.d. types); only the split attack is fully analysed for n >= 3; distribution-specific results; no cost of identities. Whether real agent populations satisfy a granularity condition is an empirical question.

## Relevance to us

Gives the swarm-lab a condition under which the simplest efficient mechanism can simply be used as-is against Sybil bidders: if most agents demand single units, splitting is not worth it in expectation. Together with [[alkalay-houlihan-2014-false-name]] (worst-case welfare bound) and the later DSL-strategies work by the same authors [[gafni-2023-optimal]], this forms the "tolerate Sybils in VCG" counterpoint to the false-name-proof design line ([[sakurai-1999-limitation]], [[iwasaki-2010-worst-case]], [[todo-2009-characterizing]]). Root: [[douceur-2002-sybil]].
