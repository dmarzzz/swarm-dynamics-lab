---
id: mir-2023-aggregate
type: paper
title: "Aggregate Signatures with Versatile Randomization and Issuer-Hiding Multi-Authority Anonymous Credentials"
authors: [Omid Mir, Balthazar Bauer, Scott Griffy, Anna Lysyanskaya, Daniel Slamanig]
year: 2023
venue: Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security (CCS '23), pp. 30-44
url: https://eprint.iacr.org/2023/1016
doi: 10.1145/3576915.3623203
arxiv: null
cite: "Mir, O., Bauer, B., Griffy, S., Lysyanskaya, A., & Slamanig, D. (2023). Aggregate Signatures with Versatile Randomization and Issuer-Hiding Multi-Authority Anonymous Credentials. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security (CCS '23), pp. 30-44. ACM. https://doi.org/10.1145/3576915.3623203"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: "52 (Crossref, 2026-10-03)"
code: []
---

## Summary

Cryptography paper that introduces Issuer-Hiding Multi-Authority Anonymous Credentials (IhMA): a user holding credentials from several independent issuers can present them in one compact showing (multi-authority, MA) without revealing which issuer signed which credential, only that the set of issuers satisfies a verifier policy (issuer hiding, IH). The motivation is self-sovereign identity and verifiable credentials, where the combination of issuers in a showing would otherwise fingerprint the user. Two new signature primitives carry the construction: AtoSa (aggregate signatures with randomizable tags and public keys) and ATMS (aggregate mercurial signatures, the first aggregate structure-preserving signature on equivalence classes, which additionally randomizes messages). IhMA_AtoSa needs no trusted party but has credential size linear in issuers; IhMA_ATMS gives constant-size credentials and faster showing but needs a trusted party holding a set-commitment trapdoor. Security definitions and proofs are given. A Python implementation (bplib/petlib, BN256 curve, ~100-bit security, Core i5-6200U) reports per-operation times in Table 2: AtoSa sign 2.5 ms, verify 8.4 ms, aggregate-verify 9 ms for two signers; ATMS sign 3 ms, verify 33 ms, aggregate-verify 72 ms; aggregation itself ~0.05 ms for 10 signers; issuing 8-10 ms; showing times scale with the number of issuers n from 2 to 10 (Fig. 11). Read from the IACR ePrint 2023/1016 full version: abstract, introduction and contribution overview, comparison Table 1, Section 6 evaluation, conclusion; the constructions and proofs (Sections 3-5) skimmed by heading.

## Contribution

First anonymous credential scheme that is simultaneously multi-authority and issuer-hiding, built on two new aggregate signature primitives with randomizable keys, tags and (for ATMS) messages.

## Key results

- IhMA achieved with two trade-off instantiations (trusted party vs. linear credential size).
- Table 2 timings in ms: AtoSa PC 6 / Sign 2.5 / Verify 8.4 / AggrSign 0.005 / VerifyAggr 9; ATMS 8.6 / 3 / 33 / 0.01 / 72.
- Aggregation cost negligible (0.05 ms at n = 10); verification dominated by pairings.

## Methods and models

Type-3 bilinear groups, SPS-EQ and mercurial signatures, set commitments, Schnorr-style ZKPoK with Damgard's technique or Fiat-Shamir; generic-group / standard assumption proofs (not checked in detail).

## Limitations and open questions

Anonymous credentials are the opposite of a Sybil defence unless paired with something that limits credentials per person: unlinkable showings mean a verifier cannot count how many agents one holder is running. The paper does not discuss Sybil resistance, rate limiting or one-per-person issuance. Python prototype timings, not production.

## Relevance to us

Low-to-moderate: it defines the privacy end of the agent-identity design space. If LLM agents carry verifiable credentials from multiple issuers (operator, model provider, platform), IhMA is how they would present them without being fingerprinted by the issuer set, which is exactly the capability a swarm operator would want and a detector would not. Should be read against proof-of-personhood and credential-with-uniqueness designs: [[rosenberg-2023-zk-creds]], [[ford-2020-identity]], [[siddarth-2020-who]], and the SSI-for-agents proposal in [[aydeger-2026-decentralized]].
