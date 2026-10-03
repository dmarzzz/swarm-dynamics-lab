---
id: resnick-2023-contingent
type: paper
title: "Contingent Fees in Order Flow Auctions"
authors: [Max Resnick]
year: 2023
venue: arXiv preprint (econ.TH)
url: https://arxiv.org/abs/2304.04981
doi: 10.48550/arXiv.2304.04981
arxiv: "2304.04981"
cite: "Resnick, M. (2023). Contingent Fees in Order Flow Auctions. arXiv preprint arXiv:2304.04981."
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

Short theory paper (Rook Labs author, funded by a Flashbots grant per its acknowledgements, and listed by Flashbots as FRP 28) comparing order flow auctions where the winner pays only if the order executes (contingent fee) with auctions where the winner pays upfront. Contingent fees turn bids into the strike price of a free option, which lowers execution probability and revenue and widens effective spreads in competitive equilibrium. Reputation systems are discussed as a "negative contingent fee" and their weaknesses listed, including re-entry under new identities.

## Contribution

Formalises the free-option problem in order flow auctions and recommends upfront payment over contingent fees, with reputation as an imperfect substitute.

## Key results

- Under zero-profit competition, the upfront-payment auction's winning bid equals the option's expected value E[max(S - K, 0)]; the contingent-fee auction yields lower execution probability, lower revenue and higher effective spreads.
- Mixed designs with share alpha paid upfront interpolate between the two; reputation penalties for non-execution act like a partial upfront payment.
- Reputation limitations listed in the discussion: manipulation through "collusion, fake accounts, or exploiting loopholes"; design complexity; and enforcement, because "participants in decentralized environments or markets with low entry barriers may re-enter under new identities, circumventing reputational consequences".

## Methods and models

Stylised auction model with a stochastic execution value S and strike K, competitive equilibria under upfront, contingent and mixed payment, plus an extension for exogenous execution success or failure. Read: abstract, model, results summary and discussion.

## Limitations and open questions

Simple model with risk-neutral competitive bidders; the reputation discussion is qualitative.

## Relevance to us

States in one line the whitewashing problem for reputation in permissionless markets: if an identity can be discarded, a reputational penalty is bounded by the cost of a new identity. Upfront payment does not depend on identity at all, which is why Flashbots designs repeatedly prefer per-action payment to reputation ([[collective-2024-dealing]], [[flashbots-2021-proposal]]). For agent task markets, the analogue is requiring a stake or fee at task acceptance rather than a reputation hit on non-delivery. Design context: [[flashbots-2022-order]]; formal identity-cost model: [[mazorra-2023-cost]].
