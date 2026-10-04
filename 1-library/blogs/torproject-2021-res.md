---
id: torproject-2021-res
type: blog
title: "Res tokens: Anonymous Credentials for Onion Service DoS Resilience (Tor Proposal 331)"
authors: ["George Kadianakis", "Mike Perry"]
year: 2021
url: https://spec.torproject.org/proposals/331-res-tokens-for-anti-dos.html
site: Tor Project specifications (proposal 331)
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

Tor design proposal 331 (created 11 February 2021, status Draft) specifies "res tokens": blind-RSA-signed anonymous tokens that clients obtain from third-party issuers after a CAPTCHA, proof-of-work or account check, cache, and later embed in INTRODUCE1 cells to onion services. The service verifies the token against the issuer key published in the Tor consensus; tokens encode the destination service and expire through key rotation.

## Key claims

- Issuer types: CAPTCHA issuers (the proposal names ctokens.torproject.org as an example), proof-of-work issuers, and onion services self-issuing to trusted users.
- RSA-1024 keys rotated every 6 hours to keep tokens small enough for INTRODUCE1 cells (about 200 bytes); verification about 0.104 ms per token.
- Deliberately avoids multi-show schemes (for example BBS+) to keep tokens small and fast.
- Open issues listed: how many issuer keys are active, consensus voting for keys, whether a destination digest is needed.
- Limitations: one-show tokens, a compromised issuer can mint for attackers, small RSA modulus, and token hoarding then burst redemption.

## Evidence quality

Draft design specification with a micro-benchmark for verification. Read via a summarising fetch, so depth is skim.

## Relevance to us

Shows how an anonymity network moves from compute cost ([[torproject-2020-first]]) to transferable anonymous credentials issued by a third party, the same move an agent ecosystem would make from per-request PoW or payment to pre-issued agent tokens. Its listed failure modes (issuer compromise, hoarding) are the same ones RFC 9576 names ([[davidson-2024-privacy]]), and the one-show design is weaker against Sybil pooling than rate-limited credentials ([[yun-2026-anonymous]]). Directly descended from [[davidson-2018-privacy]].
