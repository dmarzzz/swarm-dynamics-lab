---
id: gh-flashbots-builder-hub
type: code
title: "builder-hub: BuilderNet registry that admits builder nodes by allowlisted TEE measurements and IP, then provisions their credentials and peers"
repo: flashbots/builder-hub
url: https://github.com/flashbots/builder-hub
authors: [Flashbots]
year: 2024
language: Go
license: MIT
stars: 16
last_commit: 2026-04-30
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

BuilderHub is "the central data source for BuilderNet builder registration and configuration", with three stated jobs: builder identity management, provisioning of secrets and configuration, and peer discovery. Repo created 2024-09-18. A node proves what it is through an attested TLS channel; the hub checks the presented measurements against an active row in a measurements_whitelist table for that attestation type, looks the builder up by source IP, and only then registers its TLS certificate and ECDSA key and hands it configuration and the peer list.

## What it can do for us

- Shows attestation used as an admission credential: VerifyIPAndMeasurements requires both a measurement match (OR semantics per field across allowed values) and a known IP, which is the "attestations and IP allowlists" combination described in [[collective-2025-why]].
- Separates node identity (registered TLS certificate and ECDSA public key per builder and service) from code identity (allowlisted measurement), so peers can authenticate each other cheaply after admission. The peer orderflow proxy checks signatures against these registered keys ([[gh-flashbots-buildernet-orderflow-proxy]]).
- Admin API (behind HTTP Basic Auth) adds measurements and toggles them active, which makes the trust root an operator-governed allowlist.

## Run notes

Not run. Read the README and application/service.go. The README gives a Postgres plus `go run cmd/httpserver/main.go` setup and example calls to /api/l1-builder/v1/measurements, /builders, /configuration and /register_credentials/rbuilder.

## Limitations

Centralised and permissioned by design: the number of identities is bounded by the operator's IP and measurement allowlists, not by anything intrinsic to the attestation. The forum posts on on-chain TEE governance propose replacing this with smart contracts.

## Relevance to us

The most concrete code we found for admitting nodes into a multi-operator network on the basis of attestation. For an attested agent swarm it shows the minimum pieces: an allowlist of acceptable code measurements, a binding from attestation to a long-lived node key, and some scarce outer identifier (here an IP registered by the operator) because attestation alone does not limit how many instances one party runs ([[collective-2024-portrait]]). The location-binding upgrade path is [[rezabek-2025-proof]].
