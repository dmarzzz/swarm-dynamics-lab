---
id: gilad-2017-algorand
type: paper
title: "Algorand: Scaling Byzantine Agreements for Cryptocurrencies"
authors: ["Yossi Gilad", "Rotem Hemo", "Silvio Micali", "Georgios Vlachos", "Nickolai Zeldovich"]
year: 2017
venue: "Proceedings of the 26th Symposium on Operating Systems Principles (SOSP 2017), pp. 51-68"
url: https://eprint.iacr.org/2017/454.pdf
doi: null
arxiv: null
cite: "Gilad, Y., Hemo, R., Micali, S., Vlachos, G., & Zeldovich, N. (2017). Algorand: Scaling Byzantine Agreements for Cryptocurrencies. In Proceedings of the 26th Symposium on Operating Systems Principles (SOSP '17), pp. 51-68. ACM. https://doi.org/10.1145/3132747.3132757. Preprint: IACR Cryptology ePrint Archive 2017/454."
topics: [sybil-resistance, sync-consensus, collective-decision]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "1819 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Algorand is a cryptocurrency whose Byzantine agreement protocol, BA*, confirms blocks without forks on the order of a minute while scaling to many users. Sybil resistance comes from weighting users by the money in their accounts: BA* is safe as long as more than 2/3 of the money is held by honest users. Scalability comes from committees chosen by cryptographic sortition, in which each user privately evaluates a verifiable random function (VRF) on a public seed and learns whether, and how many times, it was selected in proportion to its stake, attaching a proof to its messages. Committee members speak once and are replaced each step. On 1,000 EC2 VMs simulating up to 500,000 users, Algorand confirmed a 1 MB block in about 22 seconds with 50,000 users, with nearly constant latency up to 500,000 users and 125 times Bitcoin's throughput.

## Contribution

The standard primary reference for stake-weighted sortition as Sybil resistance. The key observation for identity: selection is binomial in a user's currency units treated as sub-users, and because B(k1; n1, p) + B(k2; n2, p) = B(k1 + k2; n1 + n2, p), splitting stake across many Sybil identities does not change the number of committee seats the owner controls. Identity count becomes irrelevant; only weight matters.

## Key results

- Safety holds if a weighted fraction above 2/3 of users (by money) is honest; liveness assumes strong synchrony (for example 95% of honest users reach 95% of honest users within a known bound), safety tolerates bounded periods of asynchrony.
- Sortition with VRFs is private and non-interactive, so an adversary cannot target committee members before they speak; participant replacement removes the value of attacking them after.
- Seeds are refreshed every round from the previous seed via VRF, and the seed used for selection is refreshed every R rounds to limit grinding.
- Gossip peers are selected weighted by how much money they hold, "so as to mitigate pollution attacks"; messages are signed and not relayed twice.
- Measured: about 22 s to confirm a 1 MB block with 50,000 users; latency nearly flat up to 500,000 users; 125x Bitcoin throughput.

## Methods and models

Weighted users, VRF-based sortition (Algorithm 1), BA* with final and tentative consensus and a recovery protocol, Byzantine adversary controlling under 1/3 of stake, synchrony assumptions as above. Prototype evaluated on 1,000 EC2 VMs. I read the abstract, introduction, threat model, overview, gossip and sortition sections; not the full BA* proofs or every evaluation figure.

## Limitations and open questions

Sybil resistance is only as good as the stake distribution: it bounds influence by wealth, which is a plutocratic weight rather than a per-person bound. Liveness depends on a gossip network the adversary cannot partition at scale, and the paper notes that bootstrapping users can be eclipsed ([[heilman-2015-eclipse]] style). The Crossref record for the SOSP DOI is titled only "Algorand", so the DOI is kept in the citation rather than the doi field to avoid a false title mismatch.

## Relevance to us

For agent swarms, Algorand's sortition is the cleanest mechanism that makes the number of identities irrelevant: if agents are weighted by a bonded resource and committee seats are drawn in proportion, an operator gains nothing by splitting into many agents. It bounds influence (by stake), not identities. The weighted gossip-peer selection is a small but direct example of stake used inside the p2p layer, the same move as [[alpturer-2026-aetherweave]] and [[kadianakis-2023-proof]]. Contrast with personhood-based weighting in [[borge-2017-proof-of-personhood]] and with resource burning in [[gupta-2021-bankrupting]], which argues stake is not resource burning. Related: [[buterin-2017-casper]], [[freitas-2022-homomorphic]], [[burianova-2025-secret]], [[castro-1999-practical]].
