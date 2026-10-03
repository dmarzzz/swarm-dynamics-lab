---
id: karantaidou-2024-blind
type: paper
title: "Blind Multisignatures for Anonymous Tokens with Decentralized Issuance"
authors: ["Ioanna Karantaidou", "Omar Renawi", "Foteini Baldimtsi", "Nikolaos Kamarinakis", "Jonathan Katz", "Julian Loss"]
year: 2024
venue: "Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS '24)"
url: https://api.crossref.org/works/10.1145/3658644.3690364
doi: "10.1145/3658644.3690364"
arxiv: null
cite: "Karantaidou, I., Renawi, O., Baldimtsi, F., Kamarinakis, N., Katz, J., & Loss, J. (2024). Blind Multisignatures for Anonymous Tokens with Decentralized Issuance. In Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security, pp. 1508-1522. ACM."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "21 (Semantic Scholar, 2026-10-03); 17 (Crossref, 2026-10-03)"
code: []
---

## Summary

First constructions of anonymous tokens with decentralized issuance: a dynamic set of signers, from any subset of which a user obtains a publicly verifiable token unlinkable to the issuance process even if all signers collude. The paper formalises blind multi-signatures (BMS), gives one construction based on BLS signatures and one based on discrete logarithms without pairings, proves both secure in the algebraic group model, and reports a proof-of-concept with low-cost verification, which the authors identify as the critical operation for blockchain applications. Found by forward citation chasing from [[davidson-2018-privacy]]; abstract read via the Semantic Scholar API, metadata via Crossref.

## Contribution

Removes the single-issuer trust point of Privacy Pass-style tokens without moving to heavier zkSNARK credentials, complementing list-based decentralised issuance ([[garman-2013-decentralized]], [[rosenberg-2023-zk-creds]]).

## Key results

- Two BMS constructions (BLS-based; pairing-free DL-based) with AGM proofs; cheap verification (abstract). Numbers not read.

## Methods and models

Not read beyond the abstract.

## Limitations and open questions

Not read in full. Decentralised issuance spreads trust but does not by itself make issuance Sybil-resistant; each signer still needs an admission rule.

## Relevance to us

A swarm with no central authority could have a committee of agents or validators jointly issue anonymous action tokens, so no single issuer can mint Sybil tokens for itself. RFC 9576 ([[davidson-2024-privacy]]) raises centralization of Issuers as a deployment concern; this is one technical answer.
