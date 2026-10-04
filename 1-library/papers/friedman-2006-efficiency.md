---
id: friedman-2006-efficiency
type: paper
title: "Efficiency and Nash Equilibria in a Scrip System for P2P Networks"
authors: [Eric J. Friedman, Joseph Y. Halpern, Ian Kash]
year: 2006
venue: Proceedings of the 7th ACM Conference on Electronic Commerce (EC '06), Ann Arbor, pp. 140-149
url: https://www.cs.cornell.edu/home/halpern/papers/p2p.pdf
doi: 10.1145/1134707.1134723
arxiv: "0705.4094"
cite: "Friedman, E. J., Halpern, J. Y., & Kash, I. (2006). Efficiency and Nash Equilibria in a Scrip System for P2P Networks. In Proceedings of the 7th ACM Conference on Electronic Commerce (EC '06), pp. 140-149. ACM. https://doi.org/10.1145/1134707.1134723"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "42 (Crossref, 2026-10-03)"
code: []
---

## Summary

The original scrip-system analysis that [[kash-2012-optimizing]] later extends. Motivated by free riding (a small fraction of P2P users provide most service), the authors model n agents who occasionally request a service that one volunteer provides at cost alpha for one unit of scrip, with discounting delta. Theorem 3.1 shows that if agents use threshold strategies S_k (volunteer iff holding fewer than k dollars) the money distribution converges to a maximum-entropy distribution; Theorem 4.1 shows the best response to everyone playing a threshold strategy is itself a threshold strategy; Theorem 4.2 gives existence of an epsilon-Nash equilibrium in threshold strategies for sufficiently patient agents; Theorem 5.1 shows efficiency depends on the money-per-agent ratio M/n, so a designer can maximise social welfare by choosing M (illustrated for n = 1,000, M = 3,000) and scale M with n as users join. Section 6, "Sybils and collusion", is qualitative: having Sybils (citing Douceur) lets an agent (a) be chosen to work more often, so it can run a lower threshold, which the authors call "a real issue"; (b) advertise a wide range of features across identities; (c) manipulate the perceived population size by adding or withdrawing Sybils to move the price of work, with practicality depending on what Sybils cost the attacker; collusion via loans or fake transactions gives the same effect as pooling money. The follow-up paper quantifies these. Read: abstract, introduction, model, theorem statements, Section 6 and conclusion; proofs and appendix skimmed.

## Contribution

First formal equilibrium analysis of artificial-currency incentive systems for P2P service exchange, with the money-supply-sets-efficiency result and an explicit list of Sybil attack vectors against such systems.

## Key results

- Threshold strategies converge to a maximum-entropy money distribution (Thm 3.1); best responses are thresholds (Thm 4.1); epsilon-Nash exists (Thm 4.2).
- Efficiency is governed by M/n; the optimal ratio can be computed and maintained under population growth (Thm 5.1).
- Sybils: more chances to earn, feature-advertising across identities, and population-size manipulation; collusion equivalent to money pooling.

## Methods and models

Stochastic game with n agents, parameters alpha, beta, gamma, delta, discount; threshold strategies; entropy argument; numerical examples at n = 1,000, k = 5, m = 2 and M = 3,000.

## Limitations and open questions

Single service, uniform volunteer selection, no network topology; Sybil and collusion effects described but not computed (done in the 2012 journal version); identity cost left as the open parameter.

## Relevance to us

Background for the quantified Sybil results in [[kash-2012-optimizing]]: this is where the three mechanisms by which multiple identities game a token economy are first laid out, and the authors already note that the whole question reduces to how much an identity costs. Companion mechanism-design roots: [[sakurai-1999-limitation]], [[yokoo-2003-characterization]]; BitTorrent empirical counterparts: [[piatek-2007-incentives]], [[locher-2006-free]]. Root: [[douceur-2002-sybil]].
