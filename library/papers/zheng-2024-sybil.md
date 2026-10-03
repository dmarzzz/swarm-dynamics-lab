---
id: zheng-2024-sybil
type: paper
title: "Sybil-Proof Mechanism for Information Propagation with Budgets"
authors: [Junjie Zheng, Xu Ge, Bin Li, Dengji Zhao]
year: 2024
venue: "Mechanism Design in Social Networks, Communications in Computer and Information Science, Springer"
url: https://arxiv.org/abs/2405.14293
doi: 10.1007/978-981-96-0214-8_1
arxiv: "2405.14293"
cite: "Zheng, J., Ge, X., Li, B., & Zhao, D. (2024). Sybil-Proof Mechanism for Information Propagation with Budgets. In Mechanism Design in Social Networks, Communications in Computer and Information Science, pp. 1-18. Springer. https://doi.org/10.1007/978-981-96-0214-8_1"
topics: [sybil-resistance, agent-budgets]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

Mechanism design for crowdsourcing over a social network: a sponsor with a fixed budget wants participants to contribute their full capacity and invite their neighbours (as in the DARPA red balloon challenge or referral schemes), while participants may withhold invitations, misreport capacity, or create fake identities to grab more reward. The Propagation Reward Distribution Mechanism (PRDM) layers the reported network by shortest-path depth from the sponsor, keeps only edges from one layer to the next, assigns weights in a contribution phase (by depth and contribution) and then redistributes part of each agent's weight to its invitees in a propagation phase with share parameter beta. They prove PRDM is incentive compatible (full contribution and full invitation are optimal), Sybil-proof (fake identities do not raise reward), and asymptotically budget balanced. Discussion gives an impossibility: no mechanism can be both strongly IC (each invitation strictly increases reward) and strongly Sybil-proof (each fake strictly decreases it), because a real invitee and a fake one are indistinguishable. Skimmed: introduction, model, mechanism, discussion; proofs not checked.

## Contribution

A budget-feasible referral reward rule for general (not just tree) networks with heterogeneous capacities that is provably immune to Sybil reward farming.

## Key results

- PRDM: IC, Sybil-proof, asymptotically budget balanced (theorems; proofs not checked).
- Impossibility: IC + SP precludes strong IC and strong SP, so the honest-invite incentive must be weak.
- Collusion among distinct real agents is not handled; authors flag a trade-off between Sybil-proofness, collusion resistance and incentives.

## Methods and models

Directed social graph with sponsor root, agent capacities, layered-graph construction, two-phase weight allocation; axiomatic proofs.

## Limitations and open questions

Theory only, no simulation or data. Sybil-proofness here means fakes cannot gain, not that fakes are detected; the mechanism pays for that by weakening the reward for genuine invitations. Collusion is open.

## Relevance to us

Referral and airdrop-style reward schemes are a prime target for agent swarms that can spawn identities at near-zero cost. This shows the design space: you can make spawning useless, but only by making genuine recruitment barely rewarded. Related false-name-proof mechanism work: [[conitzer-2010-using]], [[yokoo-2004-effect]], [[mazorra-2023-cost]], [[bonifacio-2025-voting]]; empirical test with LLM agents: [[gh-brunomazorra-llms-sybils]].
