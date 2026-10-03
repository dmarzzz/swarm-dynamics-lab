---
id: gh-flashbots-buildernet-orderflow-proxy
type: code
title: "buildernet-orderflow-proxy: TEE-side proxy that authenticates BuilderNet peers by registered signer keys and rate limits the public user API"
repo: flashbots/buildernet-orderflow-proxy
url: https://github.com/flashbots/buildernet-orderflow-proxy
authors: [Flashbots]
year: 2024
language: Go
license: MIT
stars: 16
last_commit: 2025-12-02
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Orderflow proxy for BuilderNet (repo created 2024-09-25). A receiver proxy runs inside each TDX builder image: it generates its own TLS certificate and orderflow signer key, serves a user API and a peer API, forwards local orderflow to the builder and to other builders, and archives requests. A sender proxy signs requests with an orderflow signer key and sends them to peers fetched from BuilderHub. Identity enters in two places: who may use system endpoints (only Flashbots' signer or a registered peer's key) and how much the public user API accepts (a token-bucket rate limit).

## What it can do for us

- Peer authentication by key: ValidateSigner accepts system-endpoint requests only when the signer equals the configured Flashbots orderflow signer address or a peer's registered EcdsaPubkeyAddress from BuilderHub ([[gh-flashbots-builder-hub]]).
- Bundles carry the request signer as SigningAddress, which is the identity the refund rule and "same signer is non-competitive" rule key on ([[buildernet-2025-refunds]]).
- Public user API protected by a golang.org/x/time/rate limiter with limit and burst set from --max-local-requests-per-second (default 100); rejected requests return "requests to user API are rate limited".

## Run notes

Not run. Read the README and the receiver API and proxy setup code.

## Limitations

The user-facing rate limit is global per proxy, not per user, so it protects the node rather than allocating capacity fairly among users; per-user Sybil resistance is left to refunds and signer rules. Maintenance appears to have slowed (last commit 2025-12-02).

## Relevance to us

A small, readable example of a two-tier identity design for a multi-operator network: strong identities (attested, registered keys) for peers, weak or no identities for the public, with a global throttle as the only public-side defence. Agent networks that mix vetted internal agents with open external callers can copy the split and should note that a global throttle lets one caller crowd out others.
