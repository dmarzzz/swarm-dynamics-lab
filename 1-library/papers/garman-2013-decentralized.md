---
id: garman-2013-decentralized
type: paper
title: "Decentralized Anonymous Credentials"
authors: ["Christina Garman", "Matthew Green", "Ian Miers"]
year: 2013
venue: "IACR Cryptology ePrint Archive 2013/622 (zk-creds cites a 2014 version as GGM14; venue not checked)"
url: https://eprint.iacr.org/2013/622
doi: null
arxiv: null
cite: "Garman, C., Green, M., & Miers, I. (2013). Decentralized Anonymous Credentials. IACR Cryptology ePrint Archive, Report 2013/622."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Existing anonymous credential systems need a trusted issuer, which is a single point of failure and hard to find in ad hoc settings such as anonymous peer-to-peer networks. This paper proposes an anonymous credential scheme with no trusted issuer: credentials are recorded on a distributed transaction ledger of the kind used by Bitcoin, and users make flexible identity assertions against that ledger with standard primitives. The authors give a security proof for a basic system, discuss applications including resource management in ad hoc networks and prevention of Sybil attacks, and implement and measure the scheme.

## Contribution

Origin of the "issue to a public list instead of signing" idea that [[rosenberg-2023-zk-creds]] says it is directly inspired by. zk-creds reports that this scheme requires each client to store the full credential list and to compute proofs linear in the number of issued credentials for every show (RSA accumulator based), which zk-creds replaces with Merkle forests and proof reuse.

## Key results

- Issuer-free anonymous credentials over a public ledger, with a proof of security (abstract).
- Sybil prevention named as an application (abstract). Numbers not read.

## Methods and models

Not read beyond the abstract; the characterisation of costs above is from zk-creds' related-work section.

## Limitations and open questions

Per zk-creds: linear-time shows, full-list storage, no composition of credentials, and no way to justify issuance without disclosing the supporting information to the list maintainer.

## Relevance to us

A swarm with no central authority (a decentralised agent network) can still require each agent to hold a credential registered on a shared ledger, with registration priced to make Sybils costly, and agents then prove membership anonymously. This is the conceptual bridge between proof-of-stake style admission and anonymous participation, later instantiated by RLN registries ([[taheri-boshrooyeh-2022-privacy]]) and Semaphore groups ([[gh-semaphore-protocol-semaphore]]).
