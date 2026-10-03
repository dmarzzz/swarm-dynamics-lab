---
id: iwasaki-2010-worst-case
type: paper
title: "Worst-case efficiency ratio in false-name-proof combinatorial auction mechanisms"
authors: [Atsushi Iwasaki, Vincent Conitzer, Yoshifusa Omori, Yuko Sakurai, Taiki Todo, Mingyu Guo, Makoto Yokoo]
year: 2010
venue: Proceedings of the 9th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2010), Toronto, pp. 633-640
url: https://users.cs.duke.edu/~conitzer/worstcasefnpAAMAS10.pdf
doi: null
arxiv: null
cite: "Iwasaki, A., Conitzer, V., Omori, Y., Sakurai, Y., Todo, T., Guo, M., & Yokoo, M. (2010). Worst-case efficiency ratio in false-name-proof combinatorial auction mechanisms. In Proceedings of the 9th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2010), pp. 633-640. IFAAMAS. https://dl.acm.org/doi/10.5555/1838206.1838289"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "not available (ACM DL id 10.5555/1838206.1838289 is not a Crossref DOI; batch metadata lists 32)"
code: []
---

## Summary

Quantifies the efficiency price of Sybil-proofness in combinatorial auctions. Since no false-name-proof mechanism is always Pareto efficient, the paper asks for the worst-case efficiency ratio (fraction of the efficient surplus obtained, minimised over instances) achievable under false-name-proofness. Theorem 1: for any deterministic, symmetric, false-name-proof mechanism satisfying an "independence of irrelevant goods" (IIG) condition, with m goods and at least m+1 bidders, the worst-case ratio is at most 2/(m+1), even if all bidders are single-minded. Existing false-name-proof mechanisms do worse: Set (sell everything as one bundle) and the minimal-bundle mechanism MB get 1/m (Theorems 2-3), and the leveled division set (LDS) mechanism with any non-zero reserve gets 0 in the worst case (Theorem 4). The authors then propose the adaptive reserve price (ARP) mechanism, which sets reserve prices on single goods adaptively from the bids, prove it is false-name-proof for single-minded bidders (Theorems 5-6) and show it attains 2/(m+1), so the bound is tight. Read: abstract, introduction, model including the PORF/anonymous-pricing framing and the IIG assumption, Theorems 1-4 statements and proof sketches, ARP description and Theorems 5-6, conclusion.

## Contribution

First tight bound on how much surplus Sybil-proof combinatorial auctions must forgo: at best a 2/(m+1) fraction of the efficient surplus in the worst case, with a mechanism that achieves it.

## Key results

- Upper bound 2/(m+1) on worst-case efficiency for deterministic symmetric FNP mechanisms with IIG (Theorem 1).
- Set and MB: 1/m; LDS with reserves: 0 (Theorems 2-4).
- ARP: false-name-proof for single-minded bidders and worst-case optimal at 2/(m+1) (Theorems 5-6).

## Methods and models

Quasi-linear combinatorial auctions; PORF representation (anonymous bundle pricing, rationing-free allocation); worst-case ratio over valuation profiles; constructive mechanism design.

## Limitations and open questions

Worst-case only (average-case may be far better); ARP's FNP proof restricted to single-minded bidders; IIG and symmetry assumptions needed for the upper bound; identities costless. Multi-minded optimal mechanisms left open.

## Relevance to us

Turns "Sybil-proof auctions lose efficiency" into a number: in the worst case a Sybil-proof allocation of m resources among anonymous agents keeps only about 2/(m+1) of the achievable value. That is the cost an agent marketplace pays for not being able to tell one operator from many bidders, and a baseline for evaluating any identity-cost scheme that would relax it. Pairs with [[todo-2009-characterizing]] (which rules are implementable), [[yokoo-2003-characterization]] (PORF), [[sakurai-1999-limitation]] (impossibility), money-free analogue [[todo-2011-false-name-proof]] (Omega(n) loss), and the costly-identity escape in [[wagman-2008-optimal]]. Root: [[douceur-2002-sybil]].
