---
id: wagman-2008-optimal
type: paper
title: "Optimal False-Name-Proof Voting Rules with Costly Voting"
authors: [Liad Wagman, Vincent Conitzer]
year: 2008
venue: Proceedings of the 23rd AAAI Conference on Artificial Intelligence (AAAI-08), Chicago, pp. 190-195
url: https://users.cs.duke.edu/~conitzer/costly_votingAAAI08.pdf
doi: null
arxiv: null
cite: "Wagman, L., & Conitzer, V. (2008). Optimal False-Name-Proof Voting Rules with Costly Voting. In Proceedings of the 23rd AAAI Conference on Artificial Intelligence (AAAI-08), pp. 190-195. AAAI Press."
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "not available (no DOI; AAAI proceedings; OpenAlex rate-limited at access time; batch metadata lists 42)"
code: []
---

## Summary

In open anonymous settings an agent can vote more than once; a voting rule is false-name-proof if no agent ever benefits from extra votes. Conitzer's earlier result shows that with costless extra votes every false-name-proof rule is almost unresponsive to preferences (e.g. with two alternatives, essentially: if unanimous pick that, else flip a coin). This paper adds a per-additional-vote cost c and asks what the best false-name-proof rule becomes. For two alternatives, Theorem 1: rule FNP2, which picks alternative A with probability min{1, 1/2 + c (x_A - x_B)} given vote counts x_A >= x_B (and symmetric), is the unique strongly optimal neutral false-name-proof rule satisfying voluntary participation; intuitively, each extra vote can move the win probability by at most c so it is never worth paying c for it. Theorem 2: as the population n grows, the probability that FNP2 selects the majority winner converges to 1, because randomisation only happens when |x_A - x_B| < 1/(2c) and ties of that width become vanishingly likely, the opposite of the costless case. Theorem 3 characterises the optimal group false-name-proof rule GFNP2, robust to coalitions sharing the cost of extra votes; Theorem 4 shows that its probability of choosing the majority winner stays relatively low as n grows (e.g. with c = 0.1 and preference parameter p in [1/3, 2/3]). Theorem 5 gives the analogous optimal rule FNP3 for three alternatives, and the paper provides bounds and computational approaches (LP formulations) for four or more. Read: abstract, introduction, the two-alternative rule and Theorems 1-2 with proof sketch, group-proofness section and Theorem 4 example, three-alternative result, conclusion; the general-m LP material skimmed.

## Contribution

Shows that a small but positive cost per fake identity converts false-name-proof voting from nearly useless to asymptotically majoritarian, i.e. Sybil cost, not Sybil impossibility, is what makes responsive one-identity-one-vote mechanisms feasible.

## Key results

- FNP2 is the unique strongly optimal false-name-proof rule for two alternatives under cost c; win probability slope bounded by c.
- Pr[FNP2 picks majority winner] -> 1 as n -> infinity (Theorem 2).
- Group false-name-proof GFNP2 is much less responsive even at large n (Theorem 4).
- Extension to three alternatives (FNP3) and LP-based bounds for m >= 4.

## Methods and models

Axiomatic social choice with randomised rules, neutrality, voluntary participation, false-name-proofness with cost; i.i.d. preference model for asymptotics; linear programming for larger m.

## Limitations and open questions

Identity cost is exogenous and uniform; coalitions sharing costs (the group variant) largely erase the gain; results for many alternatives are bounds rather than characterisations. Nothing on how to impose the cost in practice.

## Relevance to us

Probably the single most useful theory result for designing agent-population votes or polls: it tells you what responsiveness you can buy for a given per-identity cost (proof-of-work, stake, verification fee), and warns that cost-sharing coalitions (one operator running many agents is exactly a coalition) take most of it back. Context: [[conitzer-2010-using]] (overview), [[conitzer-2006-computing]], [[aziz-2011-false]] and [[bachrach-2008-divide]] (weighted voting), [[sakurai-1999-limitation]] and [[yokoo-2000-effect]] (auction roots), proof-of-personhood as the cost mechanism in [[borge-2017-proof-of-personhood]] and [[ford-2020-identity]]. Root: [[douceur-2002-sybil]].
