---
id: bachrach-2008-divide
type: paper
title: "Divide and Conquer: False-Name Manipulations in Weighted Voting Games"
authors: [Yoram Bachrach, Edith Elkind]
year: 2008
venue: Proceedings of the 7th International Joint Conference on Autonomous Agents and Multiagent Systems (AAMAS 2008), Estoril, pp. 975-982
url: https://www.ifaamas.org/Proceedings/aamas08/proceedings/pdf/paper/AAMAS08_0085.pdf
doi: null
arxiv: null
cite: "Bachrach, Y., & Elkind, E. (2008). Divide and Conquer: False-Name Manipulations in Weighted Voting Games. In Proceedings of the 7th International Joint Conference on Autonomous Agents and Multiagent Systems (AAMAS 2008), pp. 975-982. IFAAMAS. https://dl.acm.org/doi/10.5555/1402298.1402358"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "not available (ACM DL id 10.5555/1402298.1402358 is not a Crossref DOI; batch metadata lists 48)"
code: []
---

## Summary

Conference original of the weighted-voting false-name line (extended as [[aziz-2011-false]] in JAIR). In a weighted voting game [w_1..w_n; q] a coalition wins if its weight meets quota q, and an agent's "real power" is its Shapley-Shubik index (Shapley value of the simple game), which also governs payoff division. The paper asks what an agent gains by splitting its weight across false identities. Theorem 4: splitting into two identities cannot raise the agent's total Shapley value by more than a factor 2n/(n+1) < 2, and the bound is tight; Theorem 5: splitting can also hurt, by up to a factor (n+1)/2, again tight. So identity splitting in voting is bounded upward but can be arbitrarily costly downward, which is the opposite of the auction setting where splitting only helps under complementarities. Computationally, Theorem 12 shows that deciding whether a beneficial split exists (Beneficial Split) is NP-hard even in restricted settings, with pseudo-polynomial or randomised algorithms for special cases and a note that splits into three or more identities behave similarly. Read: abstract, introduction, preliminaries, Theorems 4-5 statements and proof sketches, hardness result, conclusion; the Banzhaf-index material and algorithms skimmed.

## Contribution

First tight bounds on the benefit and harm of false-name (Sybil) splitting in weighted voting under the Shapley-Shubik index, plus NP-hardness of finding a profitable split.

## Key results

- Max gain from a two-way split: factor 2n/(n+1) (tight).
- Max loss from a two-way split: factor (n+1)/2 (tight).
- Beneficial Split is NP-hard; tractable in restricted weight regimes.

## Methods and models

Cooperative game theory (simple games, Shapley value via permutations), combinatorial bounds, reductions from partition-type problems.

## Limitations and open questions

Shapley-Shubik only in this version (Banzhaf and merging treated in the JAIR extension); identities are free; results are about power indices, not about any specific voting protocol's outcome. The JAIR paper supersedes this one for citation purposes.

## Relevance to us

Quantifies the Sybil incentive in weighted governance: with free identities an actor can at most roughly double its Shapley power by splitting, and may lose, which is why token-weighted (plutocratic) votes are often said to be Sybil-indifferent while one-identity-one-vote schemes are not. Pairs with [[aziz-2011-false]], the auction-side results [[sakurai-1999-limitation]] and [[yokoo-2003-characterization]], and false-name-proof matching in [[todo-2013-false]]. Root: [[douceur-2002-sybil]].
