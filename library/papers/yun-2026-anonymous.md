---
id: yun-2026-anonymous
type: paper
title: "Anonymous Rate-Limited Credentials Cryptography"
authors: ["Cathie Yun", "Christopher A. Wood", "Armando Faz-Hernandez"]
year: 2026
venue: "IETF Internet-Draft draft-ietf-privacypass-arc-crypto-01 (work in progress)"
url: https://www.ietf.org/archive/id/draft-ietf-privacypass-arc-crypto-01.html
doi: null
arxiv: null
cite: "Yun, C., Wood, C. A., & Faz-Hernandez, A. (2026). Anonymous Rate-Limited Credentials Cryptography. Internet-Draft draft-ietf-privacypass-arc-crypto-01, Internet Engineering Task Force. Work in progress."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

The ARC specification, adopted by the IETF Privacy Pass working group from draft-yun-cfrg-arc. ARC is a specialisation of keyed-verification anonymous credentials ([[chase-2014-algebraic]]) built on the MAC_GGM algebraic MAC. A client obtains a credential bound to its secrets and to application-specific public information, then may present it up to a fixed presentationLimit agreed with the server. Each presentation uses a fresh nonce in [0, presentationLimit) hidden in a Pedersen commitment with a range proof, and reveals a tag computed as (m1 + nonce)^-1 * generatorT, so the server detects reuse of a nonce (double presentation) without learning the nonce. Presentations are unlinkable to each other and to issuance. Version 01 is dated 2 March 2026; authors are from Apple and Cloudflare.

## Contribution

An IETF working-group, pairing-free construction of n-times anonymous authentication for a single service, i.e. a modern, specifiable descendant of [[camenisch-2006-how]] packaged for Privacy Pass ([[davidson-2024-privacy]]).

## Key results

- Claimed properties: correctness, unforgeability, anonymity and blind issuance (referencing KVAC definitions); computational binding under discrete log, noted as not quantum-safe.
- Clients must keep a stateful counter; exceeding the limit breaks unlinkability.
- The draft compares MAC_GGM with MAC_DDH (larger credentials) and BBS (needs pairings).

## Methods and models

Specification with algorithms, encodings and security considerations. Read via a summarising fetch of the draft HTML, so depth is skim.

## Limitations and open questions

Keyed verification: only the issuing server can verify. Rate limit is per credential, so Sybil resistance still depends on how credentials are issued (the Attester in Privacy Pass terms). Unlike RLN or clone-resistance gadgets, over-use is detected and rejected but does not reveal the identity.

## Relevance to us

ARC is the most likely near-term deployed mechanism by which an agent could hold an anonymous, bounded quota at a service (for example an LLM API) without an account linking its calls. For swarms: issue one ARC credential per accountable principal, set presentationLimit to the per-principal budget, and spinning up more agents does not increase that budget. Compare [[taheri-boshrooyeh-2022-privacy]] and [[crapis-2026-zk]] (stake-backed, identity-revealing) and [[chu-2023-security]].
