---
id: mazorra-2023-cost
type: paper
title: 'The Cost of Sybils, Credible Commitments, and False-Name Proof Mechanisms'
authors:
- 'Bruno Mazorra'
- 'Nicolás Della Penna'
year: 2023
venue: 'arXiv preprint (cs.GT)'
url: https://arxiv.org/pdf/2301.12813
doi: null
arxiv: '2301.12813'
cite: 'Mazorra, B., & Della Penna, N. (2023). The Cost of Sybils, Credible Commitments, and False-Name Proof Mechanisms. arXiv preprint arXiv:2301.12813.'
topics:
- sybil-resistance
- collective-decision
- llm-agent-swarms
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

The paper unifies the Sybil-attack literature (one attacker, honest others) and the false-name-proof literature (everyone may clone at zero cost) with a Sybil extension game in which every player chooses how many identities to present at a cost c per identity. It shows that equal-split reward sharing has a symmetric mixed equilibrium with welfare Theta(R/n), a loss of order n it calls the price of identity. It characterises Sybil-proof reward distribution: the welfare-optimal symmetric, prior-free rule is r(n) = R / 2^(n-1), a construction called pie shrinking with crowding. The same technique bounds Sybil-proof cake cutting, builds Sybil-proof bidding rings in second price auctions, and shows that Shapley, Hybrid and VCG cost-sharing for public excludable goods are not Sybil-proof. A final section on Sybil commitments shows that when agents can credibly commit their Sybils to act as independent rational players (smart contracts, or delegated AI agents), mechanisms that are Sybil-proof without commitment can break.

## Contribution

A cost-parameterised model of identity creation that recovers classical mechanism design (c infinite), the Sybil-attack model and false-name-proofness (c = 0) as special cases, plus the first treatment of Sybils that commit to independent strategies. It is cited by [[pan-2024-sybil]] as the source of the costly-Sybil open question.

## Key results

- Simple example in the paper: with R = 10, c = 0.1 and 3 other identities, presenting 2 identities pays 3.8 against 2.4 for one, so cloning is profitable even with positive cost.
- Proposition 1: equal-split reward with linear identity cost has a symmetric mixed equilibrium with welfare Theta(R/n); optimal welfare over equilibrium welfare is Theta(n).
- Proposition 3: r(n) = R / 2^(n-1) is Sybil-proof for all c >= 0 and is welfare-optimal among Sybil-proof prior-free reward rules, so no efficient prior-free Sybil-proof reward mechanism exists.
- Proposition 6: the unique twice-differentiable pro-rata mechanism with a strictly dominant strategy has equilibrium welfare R n e^(-n+1).
- Proposition 7: no truthful Sybil-proof cake-cutting mechanism is alpha-proportional for alpha > 1/2^(n-1); worst-case welfare is at most n/2^(n-1), and a matching non-constructive mechanism exists (Proposition 8).
- Proposition 10: profitable Sybil-proof bidding rings exist in second price auctions; efficient bidding rings are not Sybil-proof.
- Proposition 11: the Hybrid, Shapley and VCG mechanisms for public excludable goods are not Sybil-proof.
- Theorem 12: in Sybil-commitment games with symmetric bounded super-additive utilities and identity cost c = O(1/l^2), Sybil-commitment-proofness forces equilibrium welfare O(n/2^n); Cournot oligopoly is Sybil-proof but not Sybil-commitment-proof (with n = 10, beta = 10, c = 0.001 the best response is 11 Sybils).
- A simulation of batched CFMM arbitrage (a concave pro-rata game) shows a player gains by committing one extra identity.

## Methods and models

Games with an unknown number of players modelled as Bayesian games with active and inactive types; anonymous payoff maps U over direct sums of action spaces; identity cost C(x, y) = c x. Sybil-proofness: every Sybil strategy is weakly dominated by a single-identity strategy. Proofs are analytic; one numerical experiment on a constant-product market maker. The paper links to a code repository, github.com/BrunoMazorra/CostsOfSybils, which returned 404 on 2026-10-03; a repository named BrunoMazorra/Cost-of-Sybils exists but holds only a README and a PDF.

## Limitations and open questions

Several mechanisms are non-constructive (cake cutting relies on Neyman's theorem). The welfare bounds are worst-case and exponential, which means Sybil-proofness by pie shrinking is extremely costly at large n. The commitment section is the least developed and the CFMM simulation is a single configuration. The paper is a v3 preprint dated June 2023; I did not find a refereed version.

## Relevance to us

Two ideas transfer directly to agent swarms. First, the price of identity: in any equal-share reward, a population of cloning agents dissipates the pot, with welfare falling as 1/n. Second, Sybil commitments: an LLM agent that spawns sub-agents, each credibly running its own policy, is exactly the delegated-commitment setting of Section 3, and the paper shows this breaks mechanisms that resist ordinary Sybils. The author's later repository [[gh-brunomazorra-llms-sybils]] tests whether LLM agents discover such strategies. Read with [[pan-2024-sybil]], [[mazorra-2023-optimality]] and [[yaish-2026-inequality]].
