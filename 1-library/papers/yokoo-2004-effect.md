---
id: yokoo-2004-effect
type: paper
title: 'The effect of false-name bids in combinatorial auctions: new fraud in internet auctions'
authors:
- 'Makoto Yokoo'
- 'Yuko Sakurai'
- 'Shigeo Matsubara'
year: 2004
venue: 'Games and Economic Behavior'
url: https://courses.cs.duke.edu/fall06/cps296.2/yokoo_geb.pdf
doi: 10.1016/S0899-8256(03)00045-9
arxiv: null
cite: 'Yokoo, M., Sakurai, Y., & Matsubara, S. (2004). The effect of false-name bids in combinatorial auctions: new fraud in internet auctions. Games and Economic Behavior, 46(1), 174-188.'
topics:
- sybil-resistance
- collective-decision
- agent-budgets
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: 'OpenAlex 2026-10-03: 257'
code: []
---

## Summary

The paper defines false-name bids, bids submitted by one bidder under several identifiers such as e-mail addresses, and a protocol as false-name-proof if truthful bidding under one identity is a dominant strategy. It shows that the Vickrey-Clarke-Groves mechanism is not false-name-proof, that no false-name-proof combinatorial auction protocol is Pareto efficient, and that concavity of the surplus function over bidders (implied by submodularity for all bidder sets) is a sufficient condition for VCG to be false-name-proof. It also separates false-name-proofness from group-strategy-proofness.

## Contribution

The founding paper of false-name-proof mechanism design. It introduces the identifier mapping phi(i) that is private to each bidder and proves the efficiency impossibility that later Sybil-proofness results, including [[pan-2024-sybil]], build on.

## Key results

- VCG is strategy-proof and efficient without false names but is not false-name-proof.
- No false-name-proof combinatorial auction protocol satisfies Pareto efficiency.
- If the surplus function U is submodular for every set of bidders then the VCG mechanism is false-name-proof (Proposition 3); submodularity is close to necessary (Proposition 4).
- False-name-proofness and group-strategy-proofness are independent properties.

## Methods and models

Quasi-linear private-value model with free disposal; a set of identifiers M partitioned among bidders by a private map phi; almost anonymous protocols; proofs by counterexample and by concavity arguments. This is the October 2002 preprint hosted on a Duke course page; I compared its abstract with the journal record (Crossref volume 46 issue 1 pages 174-188).

## Limitations and open questions

I skimmed the preprint (abstract, model, theorem statements, submodularity section) and did not check every proof. The model forbids impersonating existing bidders and assumes zero cost identities.

## Relevance to us

Gives the base definitions any Sybil-proof allocation for agents must meet, and the warning that efficient allocation of bundles (tasks, compute slots, block space) cannot be false-name-proof in general. Submodular value structure is the one regime where the standard VCG survives cloning. See [[conitzer-2010-using]] for the survey context and [[pan-2024-sybil]] for the single-good sharpening.
