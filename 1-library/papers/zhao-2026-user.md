---
id: zhao-2026-user
type: paper
title: "User-Side Pairing-Free Lightweight Distributed Anonymous Counting Tokens"
authors: [Yanqi Zhao, Minghong Sun, Xiaoyi Yang, Min Xie, Yong Yu]
year: 2026
venue: "IEEE Transactions on Dependable and Secure Computing"
url: https://doi.org/10.1109/TDSC.2026.3682682
doi: 10.1109/TDSC.2026.3682682
arxiv: null
cite: "Zhao, Y., Sun, M., Yang, X., Xie, M., & Yu, Y. (2026). User-Side Pairing-Free Lightweight Distributed Anonymous Counting Tokens. IEEE Transactions on Dependable and Secure Computing, 23(4), 8349-8359. https://doi.org/10.1109/TDSC.2026.3682682"
topics: [sybil-resistance]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

Anonymous Counting Tokens (ACT) let an issuer give each client at most one valid token per message (for example one vote or one sign-up per context) without learning who the client is. Standard ACT has a single central issuer, a single point of failure, and heavy client-side pairing operations unsuited to IoT devices. LDACT distributes issuance across several issuers, removes pairings from the user side, keeps tokens publicly verifiable, and is proven unforgeable and unlinkable; benchmarks on Ubuntu and Raspberry Pi report millisecond-level client cost and comparisons with other schemes. Only the abstract (candidate record and IEEE Xplore) was read; the threshold structure and exact timings are not recorded.

## Contribution

Makes the "one anonymous token per user per message" primitive cheaper on constrained clients and removes the single trusted issuer.

## Key results

- Unforgeability and unlinkability proofs (abstract).
- Millisecond-level user-side computation on a Raspberry Pi (abstract; numbers not read).

## Methods and models

Distributed issuance, pairing-free user-side computation, publicly verifiable tokens; security analysis; benchmarks on Ubuntu and Raspberry Pi.

## Limitations and open questions

ACT bounds tokens per credential, not per human: Sybil resistance still depends on how clients obtain their base identity. Not assessed beyond the abstract.

## Relevance to us

A primitive for "each identity acts at most once per context" (voting, airdrops, sign-ups), which is the rate-limit half of Sybil resistance for agent swarms; the identity half comes from personhood or stake. Related token primitives: [[davidson-2018-privacy]], [[chu-2023-security]], [[hanff-2025-security]]; personhood: [[adler-2024-personhood]].
