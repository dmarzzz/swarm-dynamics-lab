---
id: gh-rate-limiting-nullifier-circom-rln
type: code
title: "circom-rln: Rate-Limiting Nullifier circuits that let anonymous members send at most N messages per epoch or lose their stake"
repo: Rate-Limiting-Nullifier/circom-rln
url: https://github.com/Rate-Limiting-Nullifier/circom-rln
authors: ["Rate-Limiting-Nullifier contributors (PSE)"]
year: 2023
language: "Circom / TypeScript"
license: "Apache-2.0"
stars: 33
last_commit: 2024-07-13
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: []
---

## Summary

RLN is a zero-knowledge gadget for spam prevention in anonymous settings. In `circuits/rln.circom` (read for this entry) a member's rate commitment Poseidon(identityCommitment, userMessageLimit) must be in a Merkle tree; a private messageId is range-checked below the member's limit; and the circuit outputs a Shamir share y = identitySecret + a1 * x with a1 = Poseidon(identitySecret, externalNullifier, messageId), plus nullifier = Poseidon(a1). Sending two messages with the same messageId in one epoch reveals two points on the same line, so anyone can recover the secret and slash the member's deposit via the registry contract. The README says the circuits were audited by Veridise, yAcademy fellows and internally.

## What it can do for us

RLN turns a one-off Sybil cost (a deposit per identity) into a bound on throughput per identity, with automatic punishment by revelation. That matches the agent-swarm problem well: we usually cannot stop an operator from running many agents, but we can make each one pay a stake and cap how fast each can post. It builds on [[gh-semaphore-protocol-semaphore]] and is implemented in Rust in [[gh-vacp2p-zerokit]].

## Run notes

Not run. Circuits compiled with circom 2.1; tests in the repo's workflow.

## Limitations

Small repo, last commit July 2024. Rate limits bound per-identity throughput, not identity count; Sybil resistance still rests on the cost of registering each identity.
