---
id: yokoo-2007-making
type: paper
title: "Making VCG More Robust in Combinatorial Auctions via Submodular Approximation"
authors: [Makoto Yokoo, Atsushi Iwasaki]
year: 2007
venue: Proceedings of the Twenty-Second AAAI Conference on Artificial Intelligence (AAAI-07), Vancouver, NECTAR track, pp. 1679-1682
url: https://cdn.aaai.org/AAAI/2007/AAAI07-272.pdf
doi: null
arxiv: null
cite: "Yokoo, M., & Iwasaki, A. (2007). Making VCG More Robust in Combinatorial Auctions via Submodular Approximation. In Proceedings of the Twenty-Second AAAI Conference on Artificial Intelligence (AAAI-07), pp. 1679-1682. AAAI Press. https://aaai.org/papers/01679-aaai07-272-making-vcg-more-robust-in-combinatorial-auctions-via-submodular-approximation/"
topics: [sybil-resistance, collective-decision, agent-budgets]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: full
relevance: 3
citations: "not indexed by Crossref (no DOI); 2 on the Exa index, 2026-10-03"
code: []
---

## Summary

Four-page NECTAR-track digest of the authors' AAMAS 2006 protocol, the Groves Mechanism with SubModular Approximation (GM-SMA), written for a general AI audience. The problem: the VCG mechanism for combinatorial auctions is strategy-proof but (a) is not false-name-proof (a bidder gains by splitting one bid across several fake identities, the auction-theory name for a Sybil attack), (b) losers can collude to lower winners' prices, and (c) the outcome can fall outside the core. Ausubel and Milgrom showed these defects vanish when bidder valuations are submodular (no complementarities), but complementarity is the whole reason for combinatorial auctions. GM-SMA keeps the VCG payment form but computes a winner's price against a submodular over-approximation U* of the other bidders' valuations: p = U*(M, others) minus V*(M minus B, others), and the winner may decline if the price exceeds its value, so Pareto efficiency is not guaranteed. The paper restates the earlier results (Yokoo, Sakurai and Matsubara 2004) that false-name-proofness and Pareto efficiency cannot coexist, so efficiency must be sacrificed, and defines false-name-proofness as truthful bidding under a single identifier being dominant. Worked three-bidder, two-good examples show how a false-name split or a loser coalition that is profitable under VCG becomes unprofitable under GM-SMA (the splitter must pay 4 + 4 = 8, equal to its value). Claimed properties: (1) false-name-proof, (2) every winner is part of some Pareto-efficient allocation, (3) when the allocation is Pareto efficient, robust to loser collusion and in the core; GM-SMA is the first protocol with all three. Discussion admits efficiency and revenue depend on the quality of the submodular approximation, which the existing heuristics do poorly, and lists computational efficiency and procurement auctions as open problems. No new experiments; a positioning paper.

## Contribution

A readable statement of why Sybil-style false-name bidding breaks VCG and how approximating valuations by a submodular function restores robustness, plus a short map of open problems. The technical results belong to [[yokoo-2006-false]]; this paper's added value is the exposition and the open-problem list.

## Key results

- False-name-proof plus Pareto efficient is impossible (restated impossibility from 2004).
- GM-SMA payments: p_B,i = U*(M, Theta_N minus i) minus V*(M minus B, Theta_N minus i); winner may refuse.
- Examples: VCG lets bidder 1 split into two identities to win both goods for 3 + 2 = 5 against a value of 8; under GM-SMA the same split costs 8 and yields zero utility (Examples 1 to 3).
- Open problems named: better submodular approximations, polynomial-time false-name-proof protocols (submodular winner determination is polynomial per Lehmann et al. 2002), procurement variants.

## Methods and models

Quasi-linear private-value combinatorial auction with free disposal; dominant-strategy incentive compatibility extended to multiple identifiers; submodular approximation U* built by inflating per-bundle valuations v' >= v until submodularity holds. Theory and worked examples only.

## Limitations and open questions

No evaluation of how much efficiency or revenue is lost in practice; the authors concede the known approximation heuristics are unsatisfactory. Dominant-strategy analysis assumes the auctioneer can verify nothing about identity, which is the right Sybil model but also means the protocol pays for robustness in every instance, not only when attacked. Not a DOI-bearing publication, so CI cannot verify it; metadata copied from the AAAI page and PDF.

## Relevance to us

Part of the false-name-proof mechanism design thread that the sybil-resistance survey should treat as the economics counterpart of Douceur: [[yokoo-2004-effect]] (the attack), [[yokoo-2006-false]] (this protocol in full), [[conitzer-2010-using]], [[todo-2013-false]], [[pan-2024-sybil]]. For agent swarms that allocate tasks or resources by auction among agents that can spawn identities freely, the lesson is that any VCG-like allocator is exploitable unless valuations are forced into a submodular shape, at a known efficiency cost.
