---
id: davidson-2024-privacy
type: paper
title: "The Privacy Pass Architecture"
authors: ["Alex Davidson", "Jana Iyengar", "Christopher A. Wood"]
year: 2024
venue: "IETF RFC 9576 (Informational)"
url: https://www.rfc-editor.org/rfc/rfc9576.txt
doi: "10.17487/RFC9576"
arxiv: null
cite: "Davidson, A., Iyengar, J., & Wood, C. A. (2024). The Privacy Pass Architecture. RFC 9576. Internet Engineering Task Force. https://doi.org/10.17487/RFC9576"
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "5 (Crossref, 2026-10-03)"
code: []
---

## Summary

RFC 9576 generalises the 2018 Privacy Pass deployment ([[davidson-2018-privacy]]) into an architecture with four roles: Client, Origin (consumes tokens), Issuer (signs tokens) and Attester (checks a Client property such as solving a CAPTCHA, holding a valid device, or having an account). It defines the redemption protocol (Origin sends a TokenChallenge, Client presents a token; RFC 9577) and the requirements on issuance protocols (RFC 9578): unconditional input secrecy (blindness), one-more forgery security and concurrent security. It lists four privacy goals (Origin-Client, Issuer-Client and Attester-Origin unlinkability, plus redemption-context unlinkability) and four deployment models, from all roles run by one party to a fully split Origin/Attester/Issuer, stating for each which collusion breaks which goal.

## Contribution

The standard vocabulary for separating "who knows who you are" (Attester) from "who signs" (Issuer) from "who sees what you do" (Origin), with explicit non-collusion assumptions. It is the frame into which rate-limited issuance ([[chu-2023-security]]) and ARC ([[yun-2026-anonymous]]) are being slotted.

## Key results

- Token properties are classified as public verifiability, public metadata and private metadata; every metadata bit partitions the anonymity set, and N issuer keys leak log2(N) bits.
- If any trusted Attester is compromised, all tokens from that Issuer become untrustworthy to Origins, because Origins cannot tell which Attester was used.
- Per-Origin tokens from an Issuer that serves only one Origin let the Attester infer the Origin; cross-Origin tokens make consumption hard to regulate and need double-spend tracking.
- Section 7.1 names the "hoarding attack": many clients obtain cacheable tokens and pool them in one client to exceed a per-client limit. Mitigations: compare issuance and redemption context distributions, rate-limit issuance at Client, Attester or Issuer.
- Section 5 flags discriminatory treatment (only Clients able to attest get access) and centralization pressure, since meaningful anonymity sets need few Issuers.

## Methods and models

Architecture document with normative requirements (BCP 14 keywords). No experiments. Builds on RATS attestation terminology (RFC 9334).

## Limitations and open questions

Does not specify how to enforce non-collusion, how to bound issuer configurations (refers to a key-consistency draft), or any per-client rate limit inside the base issuance protocols. Attestation strength is out of scope, so Sybil resistance is exactly as strong as the weakest accepted Attester.

## Relevance to us

For agent swarms, the Attester/Issuer/Origin split is the right decomposition of "agent identity": an agent platform or payment rail attests that an agent is backed by a principal, an issuer mints anonymous tokens, and the service an agent calls sees only a valid token. The RFC's hoarding attack is precisely the multi-agent Sybil problem (one operator pooling allowances across many instances), and its "weakest Attester" result says a swarm accepting many identity sources is only as Sybil-resistant as the cheapest. Related: [[cloudflare-2025-forget]] (signed, non-anonymous agent identity as the opposite design point), [[adler-2024-personhood]].
