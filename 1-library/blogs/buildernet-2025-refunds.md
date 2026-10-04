---
id: buildernet-2025-refunds
type: blog
title: "Refunds"
authors: [BuilderNet]
year: 2025
url: https://buildernet.org/docs/refunds
site: buildernet.org (BuilderNet documentation)
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

BuilderNet's documentation page defining how the network refunds MEV to the parties whose orderflow it uses. It states the "flat tax" rule (refunds proportional to each identity's capped marginal contribution) and then an explicit anti-Sybil "identity constraint": no set of identities may receive more in total than its joint marginal contribution, enforced by choosing refunds closest in squared distance to the flat-tax rule subject to that constraint for every subset. Per the source repository history (BuilderNet/website, docs/refunds.mdx), the refund rule and identity constraint were added on 2025-05-13.

## Key claims

- Mechanism: BuilderNet may bid less than its block's value in MEV-Boost and retain the remainder for refunds; each transaction's contribution is the difference between the best block with and without it, computed retroactively.
- Flat tax rule: mu_i(T) = min{b_i(T), v(T) - v(T \ {i})}; refund phi_i = mu_i / sum_j mu_j times min{v(B(T)) - c, sum_j mu_j}.
- Identity constraint, quoted motive: "To avoid the rule being gamed by submitting bundles from multiple identities". For each set I of identities, mu_I(T) = min{sum_{i in I} b_i(T), v(T) - v(T \ I)} is the joint marginal contribution, and refunds r solve min sum_i (r_i - phi_i)^2 subject to sum_{i in I} r_i <= mu_I(T) for each I, and sum_i r_i <= v(T) - c.
- Transactions seen in the public mempool, or bundles made only of public transactions, get no refund; "Bundles sent by the same signer will be treated as non-competitive."
- The page says the implementation is customised and has "modifications for DoS protection and scalability" not described here.

## Evidence quality

Normative specification from the operator; no data on how often the constraint binds. The documentation states the rule is indicative. The GitHub history of the page shows a later commit (2026-09-29) removing TEE-node and operator content and noting a security-model transition; the rendered page read on 2026-10-03 still contained the refund rule.

## Relevance to us

The most concrete production example we have found of making a contribution-sharing mechanism resistant to identity splitting. Why it is needed (our reading, not stated on the page): if two complementary bundles are only valuable together, each is pivotal when submitted from its own identity, so the sum of individual marginal contributions can be up to twice what the pair adds; capping every coalition of identities at its joint marginal contribution removes the gain from splitting. This is a core-style constraint (no coalition is paid more than it adds) and is directly reusable for credit assignment in agent swarms, where one operator can run many agents that submit overlapping work. The cost is computational (constraints over subsets) and the page notes DoS modifications. Same-signer bundles being treated as non-competitive is a second, simpler identity rule. The earlier per-identity rule is in [[collective-2024-refund]]; theory on Sybil-proof reward sharing is [[mazorra-2023-cost]]; the general impossibility for non-highest-bidder allocation is [[pan-2024-sybil]]; a critical outside view of BuilderNet's trust model is [[eigenphi-2025-buildernet]].
