---
id: gh-semaphore-protocol-semaphore
type: code
title: "Semaphore: zero-knowledge group membership proofs with per-scope nullifiers for anonymous signalling"
repo: semaphore-protocol/semaphore
url: https://github.com/semaphore-protocol/semaphore
authors: ["Privacy and Scaling Explorations (Ethereum Foundation)"]
year: 2019
language: "TypeScript (Circom circuits, Solidity)"
license: "MIT"
stars: 1088
last_commit: 2026-09-18
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: []
---

## Summary

Semaphore lets a member of a group prove membership and send a message (a vote, endorsement or signal) without revealing which member they are. The core is a Circom circuit (`packages/circuits/src/semaphore.circom`, read for this entry): an EdDSA identity on Baby Jubjub is hashed with Poseidon into an identity commitment, a binary Merkle proof shows the commitment is in the group tree, and the nullifier is Poseidon(scope, secret), so each identity yields exactly one nullifier per scope and a second signal in the same scope is detectable. The repo also ships Solidity verifier contracts and JavaScript packages for off-chain proof generation. Maintained by PSE; 1,088 stars.

## What it can do for us

This is the basic primitive for anonymous one-identity-one-action in a multi-agent system: if admission to a group is Sybil-resistant (World ID, Passport, a stake), Semaphore preserves that property per action while hiding which agent acted. It is used by [[gh-worldcoin-world-id-contracts]] and extended for rate limiting by [[gh-rate-limiting-nullifier-circom-rln]].

## Run notes

Not run. Packages on npm under `@semaphore-protocol/*`; documentation at semaphore.pse.dev.

## Limitations

Semaphore does not create Sybil resistance; it only carries it from group admission to actions. Nullifiers are per scope, so an identity can act once in each of many scopes.
