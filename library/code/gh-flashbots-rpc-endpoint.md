---
id: gh-flashbots-rpc-endpoint
type: code
title: "rpc-endpoint: Flashbots Protect RPC server, with salted, hourly-rotating IP fingerprints as its rate-limit key"
repo: flashbots/rpc-endpoint
url: https://github.com/flashbots/rpc-endpoint
authors: [Flashbots]
year: 2021
language: Go
license: MIT
stars: 214
last_commit: 2025-10-30
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Go server behind Flashbots Protect (rpc.flashbots.net), the wallet RPC that proxies ordinary JSON-RPC calls to a node and sends eth_sendRawTransaction calls privately to Flashbots as bundles for up to 25 blocks, so users avoid the public mempool. Repo created 2021-10-05. For identity, the relevant piece is server/fingerprint.go: users are not identified by account but by a hash of the X-Forwarded-For IP with an hourly salt, used "as a key for rate limiting".

## What it can do for us

- A worked example of rate limiting anonymous users while limiting tracking: Fingerprint = xxhash("XFF:<ip>|SALT:<hour-truncated timestamp XOR seed>"). The seed blocks rainbow-table reversal by the operator, and the hourly salt rotates fingerprints so behaviour "cannot reasonably" be tracked over time.
- The code comment records a design choice: adding the User-Agent header was rejected "because it would make the fingerprint gameable". Any client-controlled field multiplies identities for free.
- The fingerprint is forwarded upstream as a synthetic IPv6 address in the 2001:db8::/32 documentation range, so downstream rate limiters can key on it without seeing the real IP.
- Also contains a function-selector allowlist for transactions that never need protection, and an OFAC address blocklist.

## Run notes

Not run. Read the README, fingerprint.go and the HTTP proxy client. The README gives `go run cmd/server/main.go -redis dev -signingKey dev -proxy PROXY_URL` for local development.

## Limitations

IP-based identity is Sybil-able by anyone with many addresses or proxies; the design accepts that in exchange for privacy and zero onboarding. Rate-limit thresholds are not in this repository.

## Relevance to us

For public agent-facing APIs the trade-off is the same: the cheapest identity that is somewhat scarce is the network address, and keying on anything the client controls (headers, self-declared agent IDs) gives Sybils for free. The salted rotating fingerprint is a reusable pattern when you want rate limits without a persistent user profile. Contrast with signing-key reputation in [[flashbots-2021-flashbots]] and per-IP relay limits in [[gh-flashbots-mev-boost-relay]].
