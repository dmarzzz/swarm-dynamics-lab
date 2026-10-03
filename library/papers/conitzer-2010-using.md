---
id: conitzer-2010-using
type: paper
title: 'Using Mechanism Design to Prevent False-Name Manipulations'
authors:
- 'Vincent Conitzer'
- 'Makoto Yokoo'
year: 2010
venue: 'AI Magazine'
url: https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/download/2315/2183
doi: 10.1609/aimag.v31i4.2315
arxiv: null
cite: 'Conitzer, V., & Yokoo, M. (2010). Using Mechanism Design to Prevent False-Name Manipulations. AI Magazine, 31(4), 65-78.'
topics:
- sybil-resistance
- collective-decision
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 'OpenAlex 2026-10-03: 34'
code: []
---

## Summary

A survey of false-name-proof mechanism design, the economics name for Sybil resistance. It explains why majority voting, the Generalized Vickrey Auction and the Shapley value can all be gamed by one agent using several identifiers, states the main impossibility results, and reviews four ways around them: costly identities, verifying only some identities, using social-network structure, and anonymity-proof solution concepts for coalitional games. Each idea is illustrated with small worked examples rather than formal proofs.

## Contribution

The standard entry point to the false-name-proofness literature, linking it explicitly to Douceur's Sybil attack, and the best map of positive escape routes from the impossibility results as of 2010.

## Key results

- Voting, two alternatives: the unanimity rule (choose the unanimous choice, else flip a coin) is false-name-proof, and in a sense it is the best false-name-proof rule; with more alternatives the best is to pick two at random and run unanimity.
- GVA example: against a $100 bid for {A,B}, an agent valuing {A,B} at $80 bids $80 on each item under two names, wins both and pays $40 total.
- No false-name-proof combinatorial auction is always efficient [[yokoo-2004-effect]]; submodularity of surplus makes the GVA false-name-proof; the Set and Minimal Bundle mechanisms are false-name-proof; worst-case efficiency of any false-name-proof combinatorial auction is close to the Set mechanism.
- Costly identities: a voting rule where each extra vote of lead raises the leader's win probability by at most the per-identity cost (for example 0.01 per vote, certain at a 50-vote lead) is false-name-proof and approaches majority as the electorate grows.
- Limited verification: a protocol must request identification from at least two identifiers in every subset that could be a profitable false-name set; this is necessary and sufficient.
- Social networks: exclude accounts separated from trusted accounts by a vertex cut of size at most k, applied iteratively; minimum verification sets are computable in polynomial time.
- Shapley value example: an agent owning resources A and B in a game needing A, B and C gets 1/2, but splitting into two identities gets 2/3; paying resources instead invites hiding resources, which motivates the anonymity-proof core and Shapley value [[ohta-2008-anonymity]].

## Methods and models

Survey with worked examples. Covers Conitzer 2008 (anonymity-proof voting), Yokoo et al. 2004, Guo and Conitzer (bid withdrawal), Todo et al. 2009 (subadditivity plus weak monotonicity characterise false-name-proof allocation rules), Iwasaki et al. 2010, Wagman and Conitzer 2008, Conitzer 2007 (limited verification), Conitzer et al. 2010 (social networks), Yokoo et al. 2005 and Ohta et al. 2008 (coalitional games).

## Limitations and open questions

Written in 2010, so it predates blockchain-era work on costly Sybils, Bayesian Sybil-proofness and airdrops. Informal: no definitions are given, only examples. Conclusion argues that the most promising approaches combine mechanism design with other identity techniques.

## Relevance to us

The four escape routes map onto design choices for an agent swarm: charge per identity (stake, compute, fees), verify a few identities after the fact where it matters, exploit the trust graph between agents, and pay for resources rather than for identities. The Shapley splitting example is the template for attribution games among LLM agents or retrieved documents [[patel-2025-maxshapley]]. Later work extends each route: costly identities in [[mazorra-2023-cost]] and [[waggoner-2012-evaluating]], social structure in [[ethresearch-2023-collusion]], and the single-good characterisation in [[pan-2024-sybil]].
