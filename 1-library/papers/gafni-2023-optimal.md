---
id: gafni-2023-optimal
type: paper
title: "Optimal Mechanism Design for Agents with DSL Strategies: The Case of Sybil Attacks in Combinatorial Auctions"
authors: [Yotam Gafni, Moshe Tennenholtz]
year: 2023
venue: Theoretical Aspects of Rationality and Knowledge 2023 (TARK 2023), EPTCS vol. 379, pp. 245-259
url: https://arxiv.org/abs/2210.15181
doi: 10.4204/EPTCS.379.20
arxiv: "2210.15181"
cite: "Gafni, Y., & Tennenholtz, M. (2023). Optimal Mechanism Design for Agents with DSL Strategies: The Case of Sybil Attacks in Combinatorial Auctions. In R. Verbrugge (Ed.), Proceedings of Theoretical Aspects of Rationality and Knowledge (TARK 2023), EPTCS 379, pp. 245-259. https://doi.org/10.4204/EPTCS.379.20"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "not checked (OpenAlex budget exhausted 2026-10-03)"
code: []
---

## Summary

Introduces a robust-decision solution concept, DSL (distinguishable safety level, the "discrimin" ordering from fuzzy constraint satisfaction), for agents facing uncertainty without a usable prior: compare two actions only on the states of nature where they give different payoffs, and prefer the one with the better worst case there. Leximin implies DSL but not conversely, and the paper places DSL in a hierarchy with safety-level and min-max regret (Figure 1, Section 3 and Appendix A). The main application is Sybil (false-name) bidding in combinatorial auctions, where it is known that VCG is not false-name-proof and that in full-information settings any false-name-proof mechanism has poor welfare (citing Iwasaki et al.). The key observation is that profitable false-name attacks on VCG typically require overbidding true valuations, which is risky without full information about other bids. Theorem 4.2: when all bidders play DSL strategies, a discretised VCG (valuations on an epsilon grid, bids on a finer grid) achieves optimal social welfare even under false-name attacks with general valuations. The proof classifies Sybil attacks into overbidding (not DSL, because some state gives negative utility where truth gives zero), underbidding and exact bidding, and shows the latter still yield the welfare-maximising allocation while truthful bidding is itself DSL. The paper notes that for the XOS valuation class an adversary with full information can drive VCG to arbitrarily bad welfare (full version), so the uncertainty assumption is doing the work. Discussion: the same concept gives near truthfulness and optimal revenue in discrete first-price auctions (Appendix B) but not in voting (full version). Skim: abstract, introduction, Section 1.2 on VCG and Sybils, Theorem 4.2 statement and proof outline, discussion; hierarchy proofs and appendices not read.

## Contribution

Shows that Sybil robustness in auctions can come from the attacker's risk posture rather than from the mechanism: under a strong but natural risk-aversion notion (DSL) and uncertainty about others' bids, plain VCG is welfare-optimal despite false-name bidding, sidestepping the known impossibility for false-name-proof mechanisms.

## Key results

- DSL is strictly stronger than safety level; leximin implies DSL; min-max regret is incomparable (Section 3, Appendix A).
- Theorem 4.2: with DSL bidders, discrete VCG attains optimal welfare under false-name attacks for general combinatorial valuations.
- Overbidding Sybil attacks are never DSL; underbidding and exact-bidding Sybil attacks do not reduce welfare (proof structure, Section 4).
- Counterpoint: under full information, XOS valuations admit Sybil attacks that make VCG arbitrarily suboptimal (stated, proved in full version).

## Methods and models

Game-theoretic; quasi-linear combinatorial auction with each real agent able to submit a vector of bids under separate identities; welfare measured over real agents; discretised bid and valuation grids to avoid tie issues. No simulations.

## Limitations and open questions

Relies on bidders being DSL (a strong risk-aversion assumption) and on the nature state being pure; the authors admit that with mixed nature states DSL collapses to safety level. Equilibrium selection is not addressed; the result is about the induced allocation given DSL play, not about dominant strategies. Open questions listed: whether DSL strategies exist in other settings with safety-level guarantees, and single-item implications.

## Relevance to us

Economics side of the Sybil question for agent swarms that allocate via auctions: complements the mechanism-side line ([[yokoo-2004-effect]], [[yokoo-2006-false]], [[yokoo-2007-making]], [[conitzer-2010-using]], [[todo-2013-false]]) by arguing that uncertainty plus risk-averse agents already neutralises false-name bidding. For LLM agents, the interesting question is which risk posture they actually exhibit; if agents are DSL-like, VCG is fine, if they are risk-neutral expected-utility maximisers with good information, it is not. See also the scrip-system Sybil analysis in [[kash-2009-manipulating]].
