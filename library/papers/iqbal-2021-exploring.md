---
id: iqbal-2021-exploring
type: paper
title: "Exploring Sybil and Double-Spending Risks in Blockchain Systems"
authors: [Mubashar Iqbal, Raimundas Matulevičius]
year: 2021
venue: IEEE Access, vol. 9, pp. 76153-76177
url: https://ieeexplore.ieee.org/document/9435780
doi: 10.1109/access.2021.3081998
arxiv: null
cite: "Iqbal, M., & Matulevičius, R. (2021). Exploring Sybil and Double-Spending Risks in Blockchain Systems. IEEE Access, 9, 76153-76177. https://doi.org/10.1109/ACCESS.2021.3081998"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "125 (Crossref, 2026-10-03)"
code: []
---

## Summary

Applies a security risk management (SRM) domain model (assets, threats, vulnerabilities, countermeasures) to the two blockchain risks the authors consider most concerning, Sybil attacks and double-spending, and produces a framework table for each. The Sybil section enumerates seven threat patterns with cited sources: (1) break-consensus-protocol attacks on sharded chains such as Elastico, where PoW-generated node IDs assume uniform compute so an attacker with 25% of hash power against <= 16 shards and >= 600 nodes succeeds with probability <= 1e-4, but with 33-53% the probability is >= 0.8 and reaches 1 at >= 56%; (2) generate-fake-transaction attacks on the same systems, needing more compute; (3) tampering node reputation in TrustChain-style reputation DAGs; (4) node isolation / partition; (5) routing-table insertion (Kademlia-style peer-table poisoning); (6) Sybil-based linking / de-anonymisation of users; (7) Sybil-based DoS. The double-spending section covers Sybil-based double spending, 51%, PoS long-range, time-advantage, eclipse-based, BGP hijacking, 0-confirmation race, Finney and Vector76 attacks with countermeasures such as confirmation depth, checkpointing and relay monitoring. The framework is exercised on two Ethereum healthcare dApps (MedRec for Sybil, MIStore for double-spending) to derive a risk model and countermeasure list; a closing section surveys other challenges (selfish mining, quantum threats, smart-contract and wallet attacks) and argues permissioned chains control many of them through admission. Future work is an ontology-based blockchain security reference model. Read from the IEEE Xplore HTML (open access): abstract, structure, the full Sybil analysis section, the double-spending headings, example-of-use and conclusions; background and permissioned-chain sections skimmed.

## Contribution

A structured, citation-backed catalogue of what Sybil identities let an attacker do inside blockchain systems, framed as SRM assets/threats/vulnerabilities/countermeasures rather than as a protocol-level survey.

## Key results

- Seven Sybil threat patterns and nine double-spending patterns mapped to vulnerabilities and countermeasures (Tables 7 and 10).
- Quoted shard-attack numbers: P(BCP) <= 1e-4 at 25% compute with >= 600 nodes and <= 16 shards; >= 0.8 at 33-53%; 1 at >= 56% (from the cited analysis, not new).
- Worked risk models for MedRec and MIStore.

## Methods and models

Literature-driven SRM domain modelling; no experiments; evaluation by applying the framework to two published dApps.

## Limitations and open questions

Catalogue rather than analysis: numbers are relayed from cited work; the framework does not rank or quantify risks; coverage is Ethereum/PoW-centric with light PoS treatment; countermeasures are listed, not evaluated.

## Relevance to us

Useful as a checklist when mapping blockchain Sybil threats onto agent networks: reputation tampering, routing-table insertion, partitioning and linking all have direct analogues for agent registries and gossip layers. Points back to [[douceur-2002-sybil]] and forward to the eclipse literature ([[heilman-2015-eclipse]], [[singh-2006-eclipse]]) and to P2P taxonomies ([[urdaneta-2011-survey]]). For an actual defence survey use [[levine-2006-survey]] or [[yu-2011-sybil]]; this one is for threat enumeration.
