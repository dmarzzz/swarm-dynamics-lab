---
id: yokoo-2003-characterization
type: paper
title: "Characterization of Strategy/False-name Proof Combinatorial Auction Protocols: Price-oriented, Rationing-free Protocol"
authors: [Makoto Yokoo]
year: 2003
venue: Proceedings of the 18th International Joint Conference on Artificial Intelligence (IJCAI-03), Acapulco, pp. 733-739
url: https://www.ijcai.org/Proceedings/03/Papers/107.pdf
doi: null
arxiv: null
cite: "Yokoo, M. (2003). Characterization of Strategy/False-name Proof Combinatorial Auction Protocols: Price-oriented, Rationing-free Protocol. In Proceedings of the 18th International Joint Conference on Artificial Intelligence (IJCAI-03), pp. 733-739. Morgan Kaufmann."
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "not available (no DOI; OpenAlex rate-limited at access time; batch metadata lists 81)"
code: []
---

## Summary

Gives a structural characterisation of which combinatorial auction rules are strategy-proof and which are additionally false-name-proof (robust to a bidder splitting into fictitious identities). A price-oriented, rationing-free (PORF) protocol works as follows: (i) for each bidder, a price for every bundle is set independently of that bidder's own declaration (it may depend on everyone else's), (ii) the bidder is then allocated the bundle that maximises its utility at those prices, independently of the allocations to others (rationing-free), with the protocol responsible for making the resulting allocations feasible. Theorem 1: a protocol is strategy-proof if and only if it can be described as a PORF protocol, which the author presents as a new characterisation of strategy-proofness in this setting. For false-name-proofness he adds a weak anonymity/priority (WAP) condition satisfied by VCG and most known rules, and a no super-additive price increase (NSA) condition: the price a set of identities pays for a combination of bundles must be at least the price a single identity would pay for the union. Theorem 2: a PORF protocol with WAP that satisfies NSA is false-name-proof (a splitter could get the same goods cheaper as one bidder); Theorem 3: conversely, any false-name-proof PORF protocol with WAP satisfies NSA. The paper then designs a new false-name-proof protocol from the PORF recipe and discusses computational cost. Read: abstract, introduction, PORF definition and Theorem 1 statement, Section 5 (WAP, NSA, Theorems 2-3 with proofs), conclusion; the Theorem 1 proof and the new protocol's details skimmed.

## Contribution

First characterisation theorem for false-name-proof mechanisms: price-based, rationing-free rules with sub-additive-in-identities pricing are exactly the rules that identity splitting cannot game.

## Key results

- Strategy-proof iff PORF (Theorem 1).
- PORF + WAP + NSA => false-name-proof (Theorem 2); false-name-proof PORF + WAP => NSA (Theorem 3).
- Intuition: identity splitting pays off only when the mechanism offers a bundle discount to coalitions of identities; forbid that and splitting is dominated.

## Methods and models

Quasi-linear combinatorial auctions, dominant-strategy incentive compatibility extended to false-name manipulation (a bidder controls a set of identifiers), direct proofs.

## Limitations and open questions

Characterisation only for single-round direct-revelation combinatorial auctions; efficiency must still be sacrificed per the 1999 impossibility; identities are costless. Computational tractability of PORF prices is noted as a separate issue.

## Relevance to us

The cleanest design rule in the library for making an allocation mechanism immune to one operator posing as many agents: per-agent prices must not reward splitting (NSA). That transfers directly to any agent marketplace, compute auction or quadratic-style voting scheme the swarm projects might use. Lineage: [[sakurai-1999-limitation]] (impossibility), [[yokoo-2004-effect]], [[yokoo-2006-false]] (GM-SMA construction), [[conitzer-2010-using]] (overview), [[aziz-2011-false]] and [[todo-2013-false]] (voting and matching analogues). Root: [[douceur-2002-sybil]].
