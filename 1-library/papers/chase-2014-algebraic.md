---
id: chase-2014-algebraic
type: paper
title: "Algebraic MACs and Keyed-Verification Anonymous Credentials"
authors: ["Melissa Chase", "Sarah Meiklejohn", "Greg Zaverucha"]
year: 2014
venue: "Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security (CCS '14)"
url: https://api.openalex.org/works/W2134244876
doi: "10.1145/2660267.2660328"
arxiv: null
cite: "Chase, M., Meiklejohn, S., & Zaverucha, G. (2014). Algebraic MACs and Keyed-Verification Anonymous Credentials. In Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security, pp. 1205-1216. ACM."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "108 (OpenAlex, 2026-10-03); 87 (Crossref, 2026-10-03)"
code: []
---

## Summary

Considers anonymous credentials in the setting where the issuer is also the verifier, or more generally where issuer and verifier share a key. In that setting the credential can be built on message authentication codes instead of public-key signatures, which the paper calls algebraic MACs, giving keyed-verification anonymous credentials (KVAC). The OpenAlex abstract record is truncated after this framing; we did not read further.

## Contribution

Foundation of the KVAC line. The IETF ARC specification [[yun-2026-anonymous]] describes ARC as a specialisation of KVAC and cites this work; ARC uses the MAC_GGM algebraic MAC.

## Key results

- MAC-based anonymous credentials for the shared-key setting (abstract). No results read.

## Methods and models

Not read beyond the abstract.

## Limitations and open questions

Keyed verification means only the key holder can verify, so it fits "the service issues and checks its own credentials" and not open, publicly verifiable settings.

## Relevance to us

Most agent-facing services (an LLM API, a tool server) both issue and check their own access credentials, which is exactly the KVAC setting; that is why ARC is built on it. For a swarm platform, KVAC-based rate-limited credentials are the cheapest way to give each principal a bounded, unlinkable quota at one service. Related: [[davidson-2024-privacy]].
