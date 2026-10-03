---
id: davidson-2018-privacy
type: paper
title: "Privacy Pass: Bypassing Internet Challenges Anonymously"
authors: ["Alex Davidson", "Ian Goldberg", "Nick Sullivan", "George Tankersley", "Filippo Valsorda"]
year: 2018
venue: "Proceedings on Privacy Enhancing Technologies"
url: https://petsymposium.org/popets/2018/popets-2018-0026.pdf
doi: "10.1515/popets-2018-0026"
arxiv: null
cite: "Davidson, A., Goldberg, I., Sullivan, N., Tankersley, G., & Valsorda, F. (2018). Privacy Pass: Bypassing Internet Challenges Anonymously. Proceedings on Privacy Enhancing Technologies, 2018(3), 164-180."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "127 (OpenAlex, 2026-10-03); 108 (Crossref, 2026-10-03)"
code: [gh-privacypass-challenge-bypass-extension]
---

## Summary

Privacy Pass lets a user who solves one CAPTCHA receive N blinded tokens that can later be redeemed, unlinkably, instead of solving further CAPTCHAs. The construction is a verifiable oblivious PRF (2HashDH from Jarecki et al.) on elliptic curves: the client blinds T = H1(t) as T^r, the server returns T^(rk) with a batched Chaum-Pedersen DLEQ proof that every token was signed under the same committed key, and the client unblinds to W = T^k. Redemption sends t plus an HMAC over request-binding data (Host header and path) keyed by H2(t, W); the server recomputes W and keeps a double-spend list. The authors deployed it as a Chrome/Firefox extension with Cloudflare, with N = 30 tokens per solved CAPTCHA and a server cap of 100.

## Contribution

First deployed anonymous-token system at internet scale; it turns one unit of "proof of humanity" (a CAPTCHA) into a small, unlinkable, spendable allowance, and names the attacks that matter in practice (token farming, hoarding, key-partitioning, early-adopter deanonymisation). It is the ancestor of the IETF architecture [[davidson-2024-privacy]] and of Tor's token proposal [[torproject-2021-res]].

## Key results

- Measured at Cloudflare (7-day averages, November 2017): 1.6 trillion requests accepted, 780 million over Tor; 1.04% of all traffic challenged versus 17% of Tor traffic.
- Uptake 20 days after release: 8,499 Chrome and 3,489 Firefox users. Redemptions peaked at 2,000/s globally and 200/s from Tor; 22.58% of Tor requests carried clearance cookies.
- Unlinkability of signing and redemption is unconditional (the blinded point is uniform); one-more-token unforgeability reduces to one-more-decryption security of El Gamal.
- Costs on P-256: server signing 1.48 + 0.87 N ms, server redemption 0.8 ms; client signing request 340 + 180 N ms in JavaScript; redemption request 396 bytes.
- Key-consistency: clients verify a batch DLEQ proof against a published key commitment, so a server cannot use per-client keys to partition users; key rotation every few days is recommended, with at most 2-3 live keys.

## Methods and models

VOPRF protocol with formal correctness, unlinkability and one-more-token proofs in the random oracle model (Section 5), embedded into the CDN challenge workflow (Section 6), benchmarked over N = 5..100 with 100 repetitions (Section 7). Section 8 analyses out-of-band attacks: man-in-the-middle theft of signing requests, token accumulation for DDoS (1,000,000 tokens would need at least 10,000 CAPTCHA solutions at the cap of 100), token exhaustion by a malicious sub-resource, timing-based deanonymisation of early adopters, and double-spending across services.

## Limitations and open questions

- Tokens carry no binding to a client, so a farm of CAPTCHA solvers can mint and pool tokens; the only bound is the per-solution cap and key rotation.
- Anonymity depends on large user counts; small anonymity sets after key rotation are linkable.
- One-show tokens: no notion of per-epoch rate limits or identity-level revocation; misbehaviour cannot be attributed.
- Security against a server is only as good as key-consistency distribution (the paper suggests the Tor consensus).

## Relevance to us

Privacy Pass is the simplest "cost per identity converted into anonymous allowance" primitive. For agent swarms it shows the shape of a deployable defence: an attester spends something scarce once (a human check, a payment, a hardware attestation), the agent gets N unlinkable tokens, and each action spends one. Its stated failure modes map directly onto swarm Sybils: token pooling across many agents is the "hoarding" attack, and a solver farm is the same as an operator running many agent instances. Rate-limited and identity-bound successors fix parts of this: [[camenisch-2006-how]] (n per period with tracing), [[chu-2023-security]] (rate-limited Privacy Pass), [[yun-2026-anonymous]] (ARC), [[chairattana-apirom-2025-everlasting]]. Private-metadata extension: [[kreuter-2020-anonymous]].

## Notes from dmarz/sybil-code-data

A current server-side implementation of the IETF Privacy Pass issuance protocol that descends from this paper is [[gh-cloudflare-privacypass-issuer]] (Cloudflare Workers, publicly verifiable blind-RSA tokens, draft 16).
