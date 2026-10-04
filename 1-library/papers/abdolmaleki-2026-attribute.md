---
id: abdolmaleki-2026-attribute
type: paper
title: "Attribute-Based Threshold Issuance Anonymous Counting Tokens and Its Application to Sybil-Resistant Self-Sovereign Identity"
authors: [Behzad Abdolmaleki, Antonis Michalas, Reyhaneh Rabaninejad, Sebastian Ramacher, Daniel Slamanig]
year: 2026
venue: IACR Communications in Cryptology, vol. 3, no. 1, article cc3-1-46
url: https://cic.iacr.org/p/3/1/19
doi: 10.62056/ayivr-zn4
arxiv: null
cite: "Abdolmaleki, B., Michalas, A., Rabaninejad, R., Ramacher, S., & Slamanig, D. (2026). Attribute-Based Threshold Issuance Anonymous Counting Tokens and Its Application to Sybil-Resistant Self-Sovereign Identity. IACR Communications in Cryptology, 3(1). https://doi.org/10.62056/ayivr-zn4"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "1 (Crossref, 2026-10-03)"
code: []
---

## Summary

Builds a Sybil-resistant self-sovereign identity system (S3ID) whose goal is "one person, one master credential" without a central deduplicator and without linkability. The starting point is CanDID (Maram et al., IEEE S&P 2021), which achieves Sybil resistance by having an MPC committee compute a unique deterministic value from a secret-shared deduplication attribute (e.g. an SSN) and reject repeats; the authors fault CanDID for expensive MPC, loss of unlinkability if a single committee node is malicious, and repeated user-issuer interaction for every application-specific credential. Their primitive is the publicly verifiable threshold anonymous counting token (tACT): the user commits to attribute a (Pedersen commitment), t-of-N issuers return partial blind signatures, the user aggregates and unblinds into a deterministic high-entropy tag of a that issuers can deduplicate against while learning nothing about a, with a Groth-Sahai/Schnorr proof of correct evaluation. On top of this S3ID supports threshold issuance, unlinkable multi-show selective disclosure, non-interactive and non-transferable credentials, and a formal "strong unlinkability" that holds even under issuer-verifier collusion. Rust implementation (ark-bls12-381, groth-sahai-rs, code at github.com/ait-crypto/s3id) on a Core i7-1265U: tACT TokenRequest 252 ms / Verify 168 ms at N = 4, n = 30, rising to 4.4 s / 2.8 s at n = 128; S3ID Dedup 630 ms (N = 4, n = 30) to 10.8 s (N = 64, n = 128), MicroCred 137 ms at N = 4 and 1.6 s at N = 64, AppCred and VerifyCred about 28-31 ms regardless of parameters. Claimed more efficient than CanDID with more issuers and a one-round protocol run in parallel with all issuers (a direct empirical comparison was not possible because CanDID's reference code no longer builds). Read: abstract, introduction and technical overview, Section 5 evaluation including Table 2; the formal constructions and proofs (Sections 2-4) skimmed by heading.

## Contribution

Introduces threshold-issuance anonymous counting tokens in a distributed-trust setting and uses them to give proof-of-uniqueness (Sybil resistance) for SSI credentials without an MPC committee and without sacrificing unlinkability.

## Key results

- tACT and S3ID formally defined with security proofs; strong unlinkability under issuer-verifier collusion.
- Table 2 (ms): at N = 4, n = 30: TokenRequest 251.7, tIssue 25.9, Prove 31.0, Verify 168.4; Dedup 629.8, MicroCred 136.5, AppCred 27.3, VerifyCred 30.5. Costs scale linearly in threshold t' and n; MicroCred is linear in attribute count L.
- Issuer-side issuance runs in parallel across N issuers; AppCred/VerifyCred figures are lower bounds since policy evaluation is not implemented.

## Methods and models

BLS12-381 pairings (type-3 converted via a generic compiler), threshold blind signatures, Pedersen commitments, Groth-Sahai NIZK plus Schnorr proofs; parameters t = N/2 + 1, t' = n/2 + 1; N in {4, 64}, n in {30, 40, 128}.

## Limitations and open questions

Sybil resistance is only as good as the uniqueness attribute (an SSN-like value) and the honesty threshold of issuers; the scheme deduplicates humans, not agents, so it bounds agents per person only if credentials are non-transferable in practice. Accountability and recovery are explicitly out of scope. Deduplication at 0.6-10.8 s is fine for enrolment, not for per-interaction checks.

## Relevance to us

The strongest cryptographic "one human, one credential" construction in the library and a direct building block for any agent-identity scheme that wants to cap agents per operator: combine S3ID-style master credentials with the issuer-hiding showing of [[mir-2023-aggregate]] and you get privacy-preserving caps. Compare proof-of-personhood via physical pseudonym parties in [[borge-2017-proof-of-personhood]] and the identity landscape in [[ford-2020-identity]] and [[siddarth-2020-who]]; the naive SSI-for-LLM-agents proposal [[aydeger-2026-decentralized]] lacks exactly this deduplication layer. Root: [[douceur-2002-sybil]].
