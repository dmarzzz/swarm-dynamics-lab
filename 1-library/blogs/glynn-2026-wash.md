---
id: glynn-2026-wash
type: blog
title: "Wash-building in contribution protocols is not a Sybil problem"
authors: [William Glynn]
year: 2026
url: https://ethresear.ch/t/wash-building-in-contribution-protocols-is-not-a-sybil-problem/25643
site: ethresear.ch
topics: [sybil-resistance, collective-decision]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Forum post (6 August 2026) separating two attacks on contribution graphs (dependency graphs, quadratic and retro funding). Sybil is fake identity: one actor with many masks. Wash is fake value: many real, distinct identities that build on and endorse each other's worthless work. The author argues these are orthogonal and that Sybil has answers (external personhood anchors, or aggregation by the Myerson value so that graph-disconnected identities earn near-zero marginal credit), while wash does not: no graph-internal signal separates a wash tree from genuine layered collaboration. Reported measurements from the author's own code: a block forging a parent edge to a high-coverage block without adding coverage earns under a quarter of an honest block's credit; on Deep Funding jury labels a graph-topology model predicts at about 0.53 against a 0.50 floor and a rich-feature judge reaches about 0.60; jury-implied value correlates with actual funding at Spearman about -0.05. The proposed escape is to stop detecting and make value vest only on external realised use, via a refundable, contribution-denominated bond whose size grows with coordination and which is refunded on external use.

## Key claims

- A closed colluding set can forge every signal internal to it; only a signal exogenous to the set discriminates.
- Cyclic collusion (rings) has a topological signature (Helmholtz-Hodge harmonic energy); wash trees do not.
- Any cost imposed must be conditional, denominated in contribution rather than capital, and superadditive on coordinated clusters, or it rebuilds a capital gate.
- Coordination-proportional cost alone taxes honest collaboration; the external-use refund is what separates the two.

## Evidence quality

Argument plus small measurements from the author's repository (file paths are cited in the post, the repo itself is not linked in a form I opened). The impossibility claim is informal ("information-theoretic") and not proved. I read the full first post; there were no replies.

## Relevance to us

For agent swarms this is a needed distinction: a swarm of genuinely distinct agents (different operators, real identities) can still collude to inflate each other's reputation or contribution scores, and Sybil defences such as personhood or stake will not catch it. Experiments on Sybil resistance in multi-agent reputation should therefore test both fake-identity attacks and real-identity collusion, and should include an exogenous signal (use by independent parties) as a baseline defence. The Myerson-value point gives a mechanism-level Sybil defence for credit assignment in agent collaboration graphs. Related: correlation-based detection of common control [[buterin-2024-supporting]], reputation flow on trust graphs [[zebedee-2019-evidence]], market pricing of identities [[porobov-2026-price]].
