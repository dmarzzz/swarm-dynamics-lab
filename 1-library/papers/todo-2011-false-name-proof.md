---
id: todo-2011-false-name-proof
type: paper
title: "False-name-proof mechanism design without money"
authors: [Taiki Todo, Atsushi Iwasaki, Makoto Yokoo]
year: 2011
venue: Proceedings of the 10th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2011), Taipei, pp. 651-658
url: https://www.ifaamas.org/Proceedings/aamas2011/papers/B5_G62.pdf
doi: null
arxiv: null
cite: "Todo, T., Iwasaki, A., & Yokoo, M. (2011). False-name-proof mechanism design without money. In Proceedings of the 10th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2011), pp. 651-658. IFAAMAS. https://dl.acm.org/doi/10.5555/2031678.2031710"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "not available (ACM DL id 10.5555/2031678.2031710 is not a Crossref DOI; batch metadata lists 35)"
code: []
---

## Summary

Studies false-name manipulation where payments are impossible, in the canonical money-free setting of facility location on a line: n agents report locations x_i, a mechanism places one facility, each agent's cost is its distance to it. Without false names Moulin's generalised medians (Theorem 1) characterise strategy-proof rules and the plain median is optimal for social cost. Theorem 2 (main characterisation): a mechanism is false-name-proof, Pareto efficient and anonymous iff there is a fixed real alpha such that f(x) = med(x_1, ..., x_n, alpha, ..., alpha) with n-1 copies of alpha, i.e. a single fixed "phantom" location replicated to outweigh any coalition of reports, which effectively makes the outcome move toward alpha as reports pile up on one side. The price is steep: Theorem 3, any deterministic false-name-proof mechanism has approximation ratio Omega(n) for social cost (proof: two agents at 0 and 1 vs n-1 agents at 0 and one at 1, false-name-proofness forces the same distance), and Theorem 4 shows the leftmost mechanism (alpha = -infinity) achieves n-1, so the bound is tight; for maximum cost the ratio is 2, matching the strategy-proof bound (Theorem 5, with the left-right-middle mechanism in Theorem 6). Theorem 7: randomisation does not help, Omega(n) for social cost persists. Theorem 8 extends the characterisation to tree metrics; Theorem 9 covers a Pareto-efficiency relaxation. Table 1 summarises SP vs FNP ratios (social cost 1 vs Theta(n); max cost 2 vs 2). Read: abstract, introduction, model, Theorems 1-7 with proofs, Table 1, tree extension statement, conclusion.

## Contribution

First false-name-proofness results for mechanism design without money: a clean characterisation (fixed-phantom medians) and a tight impossibility showing that social-cost efficiency collapses linearly in population when identities are free and transfers are unavailable.

## Key results

- FNP + PE + anonymous iff f(x) = med(x, alpha x (n-1)) (Theorem 2).
- Deterministic and randomised FNP mechanisms: Omega(n) approximation for social cost, tight at n-1 (Theorems 3, 4, 7).
- Max cost: FNP achieves 2, same as strategy-proof (Theorems 5, 6).
- Extension to trees (Theorem 8).

## Methods and models

Single-facility location on R and on trees, false-name-proofness defined over identifier sets, approximation-ratio analysis, constructive mechanisms.

## Limitations and open questions

Single facility, one dimension or trees; identities costless; results are worst-case ratios so average-case may be benign; two-facility and other money-free domains left open.

## Relevance to us

The sharpest statement in the library of what free agent identities cost in payment-free collective choice: any Sybil-proof aggregation of agent reports on a line (think parameter setting, scheduling a shared time, choosing a configuration) must sacrifice a factor linear in population in social cost, or impose identity costs. Companion to the voting result in [[wagman-2008-optimal]] (costly identities restore responsiveness), the matching result in [[todo-2013-false]], the auction characterisations [[yokoo-2003-characterization]] and [[todo-2009-characterizing]], and the framework [[yokoo-2000-effect]]. Root: [[douceur-2002-sybil]].
