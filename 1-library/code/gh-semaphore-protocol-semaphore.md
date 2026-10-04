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

## Notes from dmarz/sybil-credentials

Lineage, from sources opened in this session: the Rate-Limiting Nullifier was first proposed as an extension of Semaphore's nullifier on ethresear.ch in February 2019 ([[barrywhitehat-2019-semaphore]]), setting the external nullifier to an epoch and adding a Shamir share of the secret so that a second signal per epoch reveals the key and allows stake slashing. That design is deployed in Waku ([[taheri-boshrooyeh-2022-privacy]]) and reused for anonymous paid API calls in [[crapis-2026-zk]]. Latest release seen via the GitHub API: v4.14.3 (2026-07-08). For richer predicates than group membership (expiry, per-context pseudonyms, clone resistance), compare [[rosenberg-2023-zk-creds]].
