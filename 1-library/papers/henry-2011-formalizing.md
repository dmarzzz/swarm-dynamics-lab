---
id: henry-2011-formalizing
type: paper
title: "Formalizing Anonymous Blacklisting Systems"
authors: ["Ryan Henry", "Ian Goldberg"]
year: 2011
venue: "2011 IEEE Symposium on Security and Privacy"
url: https://api.openalex.org/works/W2149250358
doi: "10.1109/SP.2011.13"
arxiv: null
cite: "Henry, R., & Goldberg, I. (2011). Formalizing Anonymous Blacklisting Systems. In 2011 IEEE Symposium on Security and Privacy, pp. 81-95. IEEE."
topics: [sybil-resistance, meta]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "44 (OpenAlex, 2026-10-03); 27 (Crossref, 2026-10-03)"
code: []
---

## Summary

A survey and formalisation paper. Anonymous communication networks make all users look alike, so service providers cannot hold individual abusers accountable. Anonymous blacklisting (also called anonymous revocation) systems let users authenticate anonymously while allowing a service provider to revoke access from users who misbehave without revealing their identities, in contrast to revocable-anonymity systems where a trusted third party can deanonymise. The paper proposes a formal definition of anonymous blacklisting, a set of security and privacy properties, performance requirements for real-world adoption, and definitions of optional features, then surveys and compares existing schemes and their trade-offs.

## Contribution

The review article for this sub-area: a unified definition and comparison of existing anonymous blacklisting designs, including the Nymble-like schemes ([[tsang-2011-nymble]]) that rely on a trusted third party. [[davidson-2018-privacy]] cites it as the main formalisation of the whitelisting/blacklisting alternative to anonymous tokens.

## Key results

- Formal definition and security/privacy properties for anonymous blacklisting systems (abstract).
- Comparative survey of architectures and their trust assumptions (abstract; details not read).

## Methods and models

Definitional and survey work. Not read beyond the abstract.

## Limitations and open questions

Pre-dates zkSNARK-based credentials and blockchain registries; does not cover stake-slashing designs such as RLN.

## Relevance to us

Provides the property checklist (what the platform learns, who must be trusted, cost of a blacklist check as the list grows) that any anonymous-agent accountability scheme should be evaluated against. A survey of agent Sybil defences in this repo should use its taxonomy for the "revoke after misbehaviour" branch, alongside rate-limit schemes ([[camenisch-2006-how]], [[yun-2026-anonymous]]).
