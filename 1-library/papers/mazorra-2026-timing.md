---
id: mazorra-2026-timing
type: paper
title: "Timing Games: Probabilistic backrunning and spam"
authors: [Bruno Mazorra, Christoph Schlegel, Akaki Mamageishvili]
year: 2026
venue: arXiv preprint (cs.GT)
url: https://arxiv.org/abs/2602.22032
doi: 10.48550/arXiv.2602.22032
arxiv: "2602.22032"
cite: "Mazorra, B., Schlegel, C., & Mamageishvili, A. (2026). Timing Games: Probabilistic backrunning and spam. arXiv preprint arXiv:2602.22032."
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

Game-theory paper by two Flashbots researchers and one Offchain Labs researcher modelling "probabilistic backrunning": n players race to act first after an opportunity that appears at a random time and is only observed with delay, and every action costs c. They characterise the unique symmetric equilibrium as a recursively generated random point process, show equilibrium payoff is zero, and bound total equilibrium spam (actions beyond the one needed) between V/c - 1 and V/c, tight as n grows. A companion Flashbots forum thread presents the same results.

## Contribution

A formal model of why cheap repeated on-chain attempts ("spam") arise in private-mempool and first-come-first-served chains, with a closed-form bound linking the volume of spam to opportunity value over per-action cost. It sits between the empirical spam measurements of [[flashbots-2025-mev]] and classical war-of-attrition and Hotelling-style timing models.

## Key results

- Two-player example with c >= 1/e: at most one transaction each; the equilibrium CDF of send time is sigma(x) = log(x/c) for x >= c.
- For low cost, players send many transactions; first-send timing stays log-uniform for two players while later sends become closer to uniform.
- Every symmetric equilibrium has zero expected payoff, so rents are dissipated fully in spam costs.
- Expected total spam lies between V/c - 1 and V/c, and converges to the lower bound as the number of players goes to infinity.

## Methods and models

Continuous-time timing game on [0,1] with an absolutely continuous arrival distribution, mixed strategies as finite point processes, first-order conditions from local perturbations, and a Bellman/monotone-successor argument for zero payoff and uniqueness. Read: abstract, introduction, model overview and stated results; the proofs were not checked.

## Limitations and open questions

Risk-neutral symmetric players, a single opportunity per window, a fixed marginal cost per action, and arrival-order processing (or priority with predictable fee ties). The paper does not model identities: each player may send any number of transactions, so the number of accounts is irrelevant to the result.

## Relevance to us

The useful point for Sybil resistance is the absence of identity in the model: the amount of wasteful competition depends only on V/c, the value at stake divided by the cost of one action, not on how many accounts a player uses. In settings where identities are free, the lever that bounds flooding is the per-action price or a mechanism that removes the race (an explicit auction), which is the conclusion Flashbots draws in [[flashbots-2025-mev]] and [[collective-2024-dealing]]. For agent swarms that poll or race for shared opportunities, V/c gives a back-of-envelope estimate of how much redundant work to expect. Same authors on Sybil-proof allocation: [[pan-2024-sybil]].
