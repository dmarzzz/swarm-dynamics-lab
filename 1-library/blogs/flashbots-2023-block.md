---
id: flashbots-2023-block
type: blog
title: "Block Building inside SGX"
authors: [Chris Hager, Frieder Paape]
year: 2023
url: https://writings.flashbots.net/block-building-inside-sgx
site: writings.flashbots.net
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Engineering report (2023-03-03) on running a full Flashbots block builder inside an Intel SGX enclave via Gramine, with RA-TLS remote attestation and a reproducible MRENCLAVE. It measures about 150 Mgas/s, roughly half a non-SGX builder, and a 4.5 hour startup to load an encrypted 1 TB geth database. A short section on public access names the identity problem: if users connect straight into the enclave, outside infrastructure can no longer rate limit, filter spam or manage reputation.

## Key claims

- Remote attestation is exposed as an RA-TLS certificate generated at startup, so any client can verify the enclave code before sending orders.
- End-to-end TLS into the enclave means request contents cannot be inspected by outside infrastructure. That removes the usual places where "TLS termination, rate-limiting, spam prevention, load-balancing and reputation management" happen.
- The builder "wants to focus on building, not on terminating TLS connections or dealing with spam". The stopgap that keeps access permissionless is "heavy network-based rate-limiting"; the longer-term plan is to prevent spam "through pre-simulation" in a scalable SGX architecture.
- Future work lists mutual attestation between enclaves, which is the basis for attested peer identity in later systems.

## Evidence quality

First-hand engineering notes with specific performance numbers on named hardware (48 cores, 384 GB). The spam section is a problem statement, not a solution.

## Relevance to us

Shows a tension that any confidential multi-agent system will hit: confidentiality of agent inputs removes the observation points that conventional Sybil and spam defences rely on (content filtering, per-user reputation at a proxy). What remains is network-level rate limiting, which is keyed on IP addresses and therefore Sybil-able by anyone with many addresses, or moving the filter inside the trusted boundary. Later Flashbots designs take the second path and use attestation itself as a node identity ([[gh-flashbots-builder-hub]], [[collective-2024-portrait]], [[rezabek-2025-proof]]). The per-IP limit that the public relay actually used is recorded in [[gh-flashbots-mev-boost-relay]].
