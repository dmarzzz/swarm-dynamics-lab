---
id: camenisch-2006-how
type: paper
title: "How to win the clonewars"
authors: ["Jan Camenisch", "Susan Hohenberger", "Markulf Kohlweiss", "Anna Lysyanskaya", "Mira Meyerovich"]
year: 2006
venue: "Proceedings of the 13th ACM Conference on Computer and Communications Security (CCS 2006)"
url: https://eprint.iacr.org/2006/454
doi: "10.1145/1180405.1180431"
arxiv: null
cite: "Camenisch, J., Hohenberger, S., Kohlweiss, M., Lysyanskaya, A., & Meyerovich, M. (2006). How to win the clonewars: efficient periodic n-times anonymous authentication. In Proceedings of the 13th ACM Conference on Computer and Communications Security (CCS '06), pp. 201-210. ACM. Full version: IACR Cryptology ePrint Archive 2006/454."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "49 (OpenAlex record for the CCS version, 2026-10-03; likely undercounted across duplicate records)"
code: []
---

## Summary

Crossref records the CCS title as "How to win the clonewars"; the ePrint full version is titled "How to Win the Clone Wars: Efficient Periodic n-Times Anonymous Authentication". A credential system in which a user withdraws a "dispenser" of n e-tokens and may anonymously authenticate at most n times per time period; the dispenser refreshes automatically each period. Each e-token is single-use, and because the construction is built on compact e-cash, a user who reuses a token can be identified, all of her e-tokens traced, and her dispensers revoked. The abstract claims a factor-k speedup (k the security parameter) over the only prior scheme (Damgard et al. 2005), which also allowed only one authentication per period. It adds "glitch protection": occasional reuse by mostly honest users is recognised but does not deanonymise them unless it happens too often.

## Contribution

The seminal construction of periodic n-times anonymous authentication with tracing of over-users. Later rate-limit and clone-resistance gadgets cite it directly: the clone-resistance gadget in [[rosenberg-2023-zk-creds]] is taken from its Section 5.2, and [[chairattana-apirom-2025-everlasting]] names it as one of the two original constructions of anonymous rate-limited tokens.

## Key results

- n anonymous shows per period from one dispenser, refreshed per period, with tracing and revocation of cheaters (from abstract).
- Efficiency improvement of a factor of the security parameter over Damgard et al. (from abstract; numbers not checked).

## Methods and models

Built on e-cash techniques, per the abstract. Not read beyond the abstract.

## Limitations and open questions

Not read in full. Relies on a trusted issuer holding signing keys; the later decentralised and zkSNARK approaches ([[garman-2013-decentralized]], [[rosenberg-2023-zk-creds]]) target that assumption.

## Relevance to us

"At most n actions per epoch, anonymously, with deanonymisation for clones" is exactly the property a swarm wants when it lets many agents act on behalf of one accountable principal: copying a dispenser into extra agent instances buys no extra quota and exposes the cloner. RLN ([[barrywhitehat-2019-semaphore]], [[taheri-boshrooyeh-2022-privacy]]) targets the same property with Shamir secret sharing and stake slashing instead of e-cash tracing (our comparison, inferred).
