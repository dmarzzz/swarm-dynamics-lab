---
id: chairattana-apirom-2025-everlasting
type: paper
title: "Everlasting Anonymous Rate-Limited Tokens"
authors: ["Rutchathon Chairattana-Apirom", "Nico Döttling", "Anna Lysyanskaya", "Stefano Tessaro"]
year: 2025
venue: "Advances in Cryptology - ASIACRYPT 2025, Lecture Notes in Computer Science"
url: https://eprint.iacr.org/2025/1030
doi: "10.1007/978-981-95-5119-4_14"
arxiv: null
cite: "Chairattana-Apirom, R., Döttling, N., Lysyanskaya, A., & Tessaro, S. (2025). Everlasting Anonymous Rate-Limited Tokens. In Advances in Cryptology - ASIACRYPT 2025, Lecture Notes in Computer Science, pp. 435-468. Springer."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "3 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Anonymous rate-limited tokens give a user a "token dispenser" from which up to k unlinkable, publicly verifiable tokens can be produced. Tokens are bound to a context (e.g. the service), and producing more than N <= k tokens for the same context reveals the user's identity. This paper gives the first construction with everlasting unlinkability: anonymity holds against computationally unbounded adversaries (so stored tokens stay anonymous even if future quantum computers break the assumptions), while unforgeability remains computational. The construction uses pairings; although some parameters grow with k, the cost of dispensing a single token is independent of k.

## Contribution

Upgrades the Camenisch et al. line ([[camenisch-2006-how]] and the EUROCRYPT 2005 compact e-cash paper the abstract cites) to statistical anonymity, motivated explicitly by Privacy Pass efficiency ([[davidson-2018-privacy]]).

## Key results

- First everlasting-anonymous construction of rate-limited tokens; dispensing cost independent of k (abstract).
- Deliberately non-post-quantum for unforgeability, as a pragmatic trade-off (abstract).

## Methods and models

Pairing-based construction. Not read beyond the abstract.

## Limitations and open questions

Not read in full; concrete sizes and timings unknown to us.

## Relevance to us

Agent swarms leave long-lived logs of every action; if agent identities are hidden only computationally, logs harvested today could deanonymise principals later. Everlasting unlinkability is the property to ask for when agent activity records are retained. It keeps the same "N per context, then identity revealed" Sybil bound as [[camenisch-2006-how]] and the RLN family ([[taheri-boshrooyeh-2022-privacy]]).
