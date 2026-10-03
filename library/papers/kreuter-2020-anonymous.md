---
id: kreuter-2020-anonymous
type: paper
title: "Anonymous Tokens with Private Metadata Bit"
authors: ["Ben Kreuter", "Tancrède Lepoint", "Michele Orrù", "Mariana Raykova"]
year: 2020
venue: "Advances in Cryptology - CRYPTO 2020, Lecture Notes in Computer Science"
url: https://eprint.iacr.org/2020/072
doi: "10.1007/978-3-030-56784-2_11"
arxiv: null
cite: "Kreuter, B., Lepoint, T., Orrù, M., & Raykova, M. (2020). Anonymous Tokens with Private Metadata Bit. In Advances in Cryptology - CRYPTO 2020, Lecture Notes in Computer Science, pp. 308-336. Springer."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "35 (OpenAlex, 2026-10-03); 30 (Crossref, 2026-10-03)"
code: []
---

## Summary

Presents PMBTokens: lightweight single-use anonymous trust tokens in which the issuer can embed one private bit that only the holder of the secret authority key can read; the bit is hidden from the user and everyone else. The construction generalises Privacy Pass ([[davidson-2018-privacy]]), is based on DDH and CTDH in the random oracle model, and provides unforgeability, unlinkability and privacy of the metadata bit. It also gives techniques that remove the NIZK proofs that Privacy Pass and PMBTokens otherwise need, while keeping unlinkability, and reports implementation costs.

## Contribution

Lets an issuer mark tokens (for example "suspected bot") without the user learning the mark, so fraud signals can flow from issuance to redemption. RFC 9576 cites it as the basis of private-metadata issuance ([[davidson-2024-privacy]]).

## Key results

- Single private bit per token with unforgeability, unlinkability and bit privacy under DDH and CTDH in the ROM (abstract).
- NIZK-free variants that still achieve unlinkability (abstract). Concrete costs not read.

## Methods and models

Not read beyond the abstract.

## Limitations and open questions

RFC 9576 Section 6.1 points out that every metadata bit partitions the anonymity set; an issuer can use a private bit to tag a single targeted user. The bit is therefore a tracking risk as well as a fraud signal.

## Relevance to us

For agent platforms, a private bit is how an issuer could quietly flag tokens obtained by suspected Sybil agents so that downstream services can throttle them without tipping off the operator. The same mechanism is a covert channel for deanonymising agents, so any swarm design that uses it needs bounds on metadata. Related: [[chu-2023-security]], [[yun-2026-anonymous]].
