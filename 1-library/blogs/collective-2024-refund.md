---
id: collective-2024-refund
type: blog
title: "Refund rule: wat dis, how to and FAQ"
authors: [Quintus]
year: 2024
url: https://collective.flashbots.net/t/refund-rule-wat-dis-how-to-and-faq/4049
site: collective.flashbots.net (Flashbots forum)
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Forum explainer (November 2024) for the Flashbots builder's gas fee refund rule, aimed at searchers. Searchers send bundles exclusively to the refund builder; after the block lands, builder profit is paid back in proportion to each identity's marginal contribution to block value, capped by what that identity paid. The post motivates the rule as a permissionless replacement for private "refund deals" between searchers and builders, and argues it never pays a searcher to bid above true value. Refunds are defined per identity, which is the hook for the Sybil constraint published later.

## Key claims

- Market context: searchers bid in a sealed first-price bundle auction while builders bid in a roughly open-outcry block auction, so some searchers integrate with builders or strike off-chain refund deals; a decentralised builder needs a permissionless equivalent.
- The rule: with v(T) the value of the best block from bundle set T, b_i(T) the payment of all bundles from identity i, and c the payment to the proposer, the marginal contribution is mu_i = min{b_i, v(T) - v(T without i)} and the refund is phi_i = mu_i / sum_j mu_j times min{v(T) - c, sum_j mu_j}.
- Worked example: two mutually exclusive arbs (5 and 6 ETH) and two exclusive liquidations (1 and 4 ETH) give block value 10, contributions 1 and 3; at c up to 6 everyone gets their full contribution, at c = 8 everyone gets half.
- Claimed property: overstating your value only helps in cases where your net payment exceeds your value, so bidding above value is never profitable.
- Smart multiplexing forwards bundles to other builders when the refund builder is unlikely to win; the reported error rate is about 1%.
- The rule cannot tell whether a bundle was also sent to other builders, but the authors argue high-contribution flow is still incentivised to be exclusive.

## Evidence quality

Mechanism description by the operator, with one worked on-chain example (block 20843717, a 38 ETH payment where the rule would have refunded 34 ETH but the bundle was disqualified). The incentive claims are argued informally, not proven in the post.

## Relevance to us

Any reward rule keyed on "identity i" invites the question of whether splitting into several identities raises total payout. This post defines the rule per identity but does not yet address splitting; the BuilderNet documentation later adds an explicit identity constraint that caps any set of identities at its joint marginal contribution ([[buildernet-2025-refunds]]). That pair is a worked example, from a production system, of turning a contribution-sharing rule into a Sybil-resistant one. Agent swarms that split credit by marginal contribution (Shapley-style attribution of work among agents) face the same issue; see [[mazorra-2023-cost]] for theory on Sybil-proof reward sharing.
