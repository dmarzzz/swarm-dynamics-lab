---
id: kash-2012-optimizing
type: paper
title: "Optimizing scrip systems: crashes, altruists, hoarders, sybils and collusion"
authors: [Ian A. Kash, Eric J. Friedman, Joseph Y. Halpern]
year: 2012
venue: Distributed Computing, vol. 25, no. 5, pp. 335-357
url: https://arxiv.org/abs/1204.3494
doi: 10.1007/s00446-012-0170-z
arxiv: "1204.3494"
cite: "Kash, I. A., Friedman, E. J., & Halpern, J. Y. (2012). Optimizing scrip systems: crashes, altruists, hoarders, sybils and collusion. Distributed Computing, 25(5), 335-357. https://doi.org/10.1007/s00446-012-0170-z"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "12 (Crossref, 2026-10-03)"
code: []
---

## Summary

Game-theoretic analysis of scrip (artificial currency) systems of the kind used to discourage free-riding in P2P file sharing: agents occasionally request a single service, one volunteer is chosen to provide it at a small utility cost, and payment is one unit of scrip. Building on the authors' EC 2006/2007 results that threshold strategies form an epsilon-Nash equilibrium and the money distribution converges, the paper shows social welfare is maximised by setting the money-per-agent ratio m just below a critical point at which the system suffers a "monetary crash" (money is so devalued that nobody is willing to work). It then studies four deviations from the standard agent. Altruists act like extra money and lower the crash point; hoarders act like removed money and can stabilise the system; Sybils (one agent operating several identities, citing Douceur) raise the owner's chance of being picked to work and so let it earn faster, benefiting the first few Sybils strongly with rapidly diminishing returns; collusion (pooling money inside a group) is "almost entirely positive" for everyone unless colluders can pass requests to each other, which makes them act as Sybils. Key Sybil findings (Section 5.3, simulated with 1,000 agents): if one fifth of agents each create one Sybil the system crashes at m = 9.5, a value that was near optimal without Sybils (crash between 10.25 and 10.5), so a designer who tunes m aggressively without accounting for Sybils will crash the system; a small number of agents with many Sybils can raise aggregate welfare while making non-Sybil agents worse off (20% of agents need at least eight Sybils each before the rest break even); a discontinuity appears when about a third of agents have Sybils because they begin competing with each other; and Theorem 8 shows any welfare gain from Sybils in a single-type population can be achieved without them by adjusting m and the volunteer-selection bias. Read: abstract, introduction, model overview, Section 5.3 Sybils and 5.4 Collusion, discussion; proofs and appendices skimmed.

## Contribution

Quantifies, in an equilibrium model rather than by assumption, what Sybils do to a currency-based cooperation mechanism: they shift the efficiency/stability frontier and can trigger systemic collapse even when few agents use them, and the same effects are better achieved by the designer tuning the money supply.

## Key results

- Optimal scrip supply sits just under the crash point; altruists lower it, hoarders raise it.
- 20% of agents with one Sybil each move the crash from m in (10.25, 10.5) to m = 9.5 (Fig. 8).
- Sybil benefits are front-loaded: the first few identities help a lot, additional ones little, so "moderately costly" identities suffice to keep Sybil counts small in practice.
- Non-Sybil agents are worse off unless the 20% Sybil-holders create >= 8 Sybils each (Fig. 6/7 parameters).
- Theorem 8: with a single agent type, Sybil-induced welfare can be matched without Sybils.
- Collusion is welfare-positive unless colluders can relay requests (then it reduces to the Sybil case).

## Methods and models

Discrete-time stochastic game with n agents of finitely many types (parameters alpha cost of service, gamma utility, beta chance of being able to satisfy a request, chi relative likelihood of being chosen, delta discount); threshold strategies; epsilon-Nash analysis via the limiting money distribution (maximum-entropy argument); numerical experiments at n = 1,000.

## Limitations and open questions

Single homogeneous service, fixed price of one unit, volunteers chosen uniformly (Sybils modelled purely as a boost to chi); no network structure; equilibria are epsilon-Nash in threshold strategies only. The crash phenomenon is a model artefact of fixed prices, which the authors acknowledge.

## Relevance to us

A rare formal treatment of Sybils as an incentive-level problem rather than an identity-level one: the harm is systemic (crash) and arises from a small fraction of agents, which is close to what a few operators running many LLM agents could do to any token-metered agent economy or reputation currency. Useful for the mechanism-design side of the sybil-resistance survey alongside [[cheng-2005-sybilproof]] (Sybilproof reputation), [[yokoo-2004-effect]] and [[aziz-2011-false]] (false-name manipulation in auctions and voting), and the tokenised-coordination work in [[strobel-2020-blockchain]]. Root: [[douceur-2002-sybil]].
