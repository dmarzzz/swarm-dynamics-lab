---
id: pan-2024-sybil
type: paper
title: 'On Sybil-proof Mechanisms'
authors:
- 'Minghao Pan'
- 'Bruno Mazorra'
- 'Christoph Schlegel'
- 'Akaki Mamageishvili'
year: 2024
venue: 'arXiv preprint (cs.GT)'
url: https://arxiv.org/html/2407.14485v5
doi: null
arxiv: '2407.14485'
cite: 'Pan, M., Mazorra, B., Schlegel, C., & Mamageishvili, A. (2024). On Sybil-proof Mechanisms. arXiv preprint arXiv:2407.14485 (v5, February 2026).'
topics:
- sybil-resistance
- collective-decision
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 'OpenAlex 2026-10-03: 0 (record of an AFT extended abstract)'
code: []
---

## Summary

The paper asks which allocation rules for a single private good survive when a bidder can add Sybil bids. In the single-parameter Myerson setting with quasi-linear utility, it proves that the only payment-normalised, non-wasteful, symmetric, incentive compatible and Sybil-proof direct mechanism is the second price auction with symmetric tie-breaking. So lotteries, caps and other rules that spread the good beyond the highest bidder are either manipulable by Sybils or not truthful. A revelation principle for Sybils shows indirect mechanisms cannot escape this. Relaxing to Bayesian Sybil-proofness opens the design space again: a lottery with an ex-ante ticket price that rises with the number of qualifying bidders is Bayesian Sybil-proof and gives bidders higher interim payoff than the second price auction.

## Contribution

A characterisation (Theorem 1) that collapses the whole family of monotone symmetric allocation rules to one rule once a single extra Sybil identity is allowed. It sharpens Yokoo et al.'s efficiency impossibility [[yokoo-2004-effect]] by dropping Pareto efficiency as an assumption and deriving it. The paper is written by authors affiliated with Caltech, Offchain Labs and Flashbots and is motivated by block-proposer selection, airdrops and capped ticket sales.

## Key results

- Theorem 1: payment normalisation + non-wastefulness + symmetry + IC + Sybil-proofness (against one Sybil with arbitrary bid) holds if and only if the mechanism is a second price auction with symmetric tie-breaking.
- The axioms are independent: dropping any one admits other mechanisms (for example a reserve price that grows with the number of bidders, or the generalized proportional mechanism, which is Sybil-proof but not IC).
- Example 1 is a Sybil-proof IC mechanism that wastes the good with probability approaching 1 as bidders grow, so non-wastefulness is what bites.
- Propositions 1 and 2 (revelation principle for Sybils): any symmetric indirect mechanism implementing an objective in dominant strategies or Bayes-Nash equilibrium yields a direct mechanism that is IC and (Bayesian) Sybil-proof.
- Theorem 2: the lottery with increasing ticket price is Bayesian Sybil-proof and differs from a second price auction with probability bounded below independent of n; for uniform values with n bidders the lottery branch fires with probability that the paper computes from a Binomial count of bidders above the ticket price.
- Proposition 3: the impossibility does not extend to multi-unit allocation with unit-demand bidders; a lottery among the top 2k bids is Sybil-proof.
- Proposition 4: the result extends to type-convex valuations with superadditive interim utility.

## Methods and models

Variable-population direct mechanisms (x^N, p^N) over finite bidder sets, values in non-negative reals, linear utility v x - p. Sybil-proofness is defined against a bidder reporting truthfully from the original account and adding one Sybil with any bid. Proof uses Myerson payments, a lemma that among many equal bidders a slightly higher bid almost surely wins, a two-bidder bound, and induction on the number of bidders. The Bayesian section uses i.i.d. private values with a tail condition on F.

## Limitations and open questions

Ex-post Sybil-proofness is a strong requirement; the authors list four open questions: Sybil-proof mechanisms with allocation probability bounded below, approximation of distributional goals by Sybil-proof mechanisms such as the proportional rule, the class of mechanisms when Sybils have small constant cost (pointing to [[mazorra-2023-cost]]), and a characterisation of Bayesian Sybil-proof mechanisms. The model assumes symmetric bidders and quasi-linear utility; it does not treat collusion between distinct agents, which the authors separate from Sybils.

## Relevance to us

This is the cleanest statement of what free identities do to allocation in a population of agents: any rule that tries to share a resource more evenly than winner-take-all is gamed by agents who can clone. For agent swarms that allocate tasks, compute, rewards or block-building rights by lottery or equal split, the theorem says either pay a cost per identity, accept waste, or move to Bayesian guarantees. It is the most direct Flashbots-affiliated result in this lane and connects to the MEV setting through the block-proposer and builder-market motivation. Read with [[mazorra-2023-cost]] (costly Sybils), [[babaioff-2012-bitcoin]] (equilibrium rather than dominant-strategy Sybil-proofness) and [[conitzer-2010-using]] (survey of false-name-proofness).

## Notes from dmarz/sybil-flashbots

- Affiliations on the arXiv v5 PDF: Pan at Caltech, Mazorra and Schlegel at Flashbots, Mamageishvili at Offchain Labs. This is the main formal Sybil paper from the Flashbots research group.
- Flashbots forum uses: the forum user Christoph's post "Inelastic vs. Elastic Supply: Why Proof of Stake Could Be Less Centralizing Than Execution Tickets" (collective.flashbots.net/t/3816) applies Theorem 1 to argue that a fixed supply of execution tickets would end up sold to the highest-value proposer; the post "Isolating Attesters From MEV" (collective.flashbots.net/t/3837) reads the result as a trade-off: leaving winner-takes-all formats means giving up Sybil-proofness or incentive compatibility. An OpenAlex record lists an extended abstract at AFT 2026 (DOI 10.4230/lipics.aft.2026.16), not opened.
- The conclusion poses Question 3 (what mechanisms exist when Sybils have a small constant cost), pointing to [[mazorra-2023-cost]]. Production Flashbots mechanisms take the cost-free route instead: BuilderNet's refund rule caps every coalition of identities at its joint marginal contribution ([[buildernet-2025-refunds]]), and spam is addressed by pricing actions rather than identities ([[mazorra-2026-timing]], [[flashbots-2025-mev]]).
