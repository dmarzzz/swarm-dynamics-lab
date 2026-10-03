---
id: gh-worldcoin-world-id-contracts
type: code
title: "world-id-contracts: Solidity contracts for World ID 3.0, Semaphore-based anonymous proof of unique humanity"
repo: worldcoin/world-id-contracts
url: https://github.com/worldcoin/world-id-contracts
authors: ["Worldcoin"]
year: 2022
language: "Solidity"
license: "MIT"
stars: 198
last_commit: 2026-03-26
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

On-chain part of World ID 3.0, which the README says is entering a sunsetting phase in favour of World ID 4.0 (worldcoin/world-id-protocol). Identity commitments derived from Orb iris verification are inserted into a Merkle tree by an Identity Operator (an OpenZeppelin Relay wallet) and users prove membership with [[gh-semaphore-protocol-semaphore]] proofs, so an app can check "a unique human did this once" without learning which human. The README lists privileged operations: the owner multisig can upgrade the contract, change verifiers and the state bridge, and set the identity operator; timelocks were discussed and rejected because they would desynchronise the contract from the off-chain signup sequencer.

## What it can do for us

The reference design for one-human-one-nullifier per action, which is the primitive an agent swarm would need to rate-limit or deduplicate agents that each claim backing by a distinct human.

## Run notes

Not run. README offers `docker run -p 8545:8545 ghcr.io/worldcoin/world-id-contracts` for an anvil node with contracts predeployed; Foundry for development.

## Limitations

Being sunset. Strong operator trust: an upgradeable contract under a multisig and a single relay that inserts identities.
