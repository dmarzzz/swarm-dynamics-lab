---
id: chu-2023-security
type: paper
title: "On the Security of Rate-limited Privacy Pass"
authors: ["Hien Chu", "Khue Do", "Lucjan Hanzlik"]
year: 2023
venue: "Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security (CCS '23)"
url: https://api.openalex.org/works/doi:10.1145/3576915.3616619
doi: "10.1145/3576915.3616619"
arxiv: null
cite: "Chu, H., Do, K., & Hanzlik, L. (2023). On the Security of Rate-limited Privacy Pass. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, pp. 2871-2885. ACM."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "8 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

The IETF draft by Hendrickson et al. (privacypass-rate-limit-tokens) adds a "mediator" to Privacy Pass: the mediator applies per-user access policies to rate-limit how many tokens a user obtains for a website, while staying oblivious to which website (origin) the user is accessing. This paper gives the first formal definition of rate-limited Privacy Pass (RlP), a game-based security model capturing the draft's informal notions, and a construction from simple building blocks that meets the definitions and admits a post-quantum instantiation. The instantiation in the IETF draft is shown to be a special case, so the deployed version inherits the security argument.

## Contribution

Supplies the missing security model for per-user, per-origin rate limits in anonymous tokens, which the base architecture [[davidson-2024-privacy]] leaves to deployments.

## Key results

- Formal syntax and game-based security definitions for RlP (abstract).
- Generic construction, with a post-quantum option, of which the IETF draft is an instance (abstract). Proof details not read.

## Methods and models

Not read beyond the abstract.

## Limitations and open questions

Not read in full. RFC 9576 notes that the rate-limited issuance protocol requires the Issuer to learn the Origin, so it is unsuitable for the Joint Attester and Issuer deployment model.

## Relevance to us

Per-origin rate limiting with an oblivious mediator is a direct pattern for agents: an agent platform (mediator) can enforce "this principal's agents may hit service X at most k times per window" without learning which services they hit, while the service sees only unlinkable tokens. That is a Sybil bound on how much a single principal's agent fleet can extract from any one service. Compare ARC [[yun-2026-anonymous]] and periodic n-times authentication [[camenisch-2006-how]].
