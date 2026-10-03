---
id: gh-complete-knowledge-ck
type: code
title: "Complete-Knowledge/ck: on-chain verification of ASIC-based proofs of complete knowledge"
repo: Complete-Knowledge/ck
url: https://github.com/Complete-Knowledge/ck
authors: [Complete-Knowledge GitHub organisation (IC3 complete-knowledge project)]
year: 2022
language: Solidity
license: none declared at repo level (individual files carry MIT or Unlicense SPDX headers)
stars: 4
last_commit: 2023-01-12
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Hardhat project with the smart contracts behind the "Complete Knowledge" prototype described in [[austgen-2023-complete]]. `CKVerifier.sol` registers a job (commitments plus a public key), takes trusted randomness as a challenge, and verifies that Bitcoin-format blocks mined by an ASIC embed a Schnorr-style response, which shows the secret key was handed to TEE-free mining hardware. `CKRegistry.sol` keeps a per-address 256-bit array of verification types, lets the owner set which verifier types are trusted (so a method can be revoked if found insecure), and exposes `isCK(address)`. The organisation also hosts an ASIC miner fork, a stratum pool and Android prover and verifier apps. Repo created 2022-05-24; no commits after January 2023.

## What it can do for us

Provides a working example of an on-chain registry of "this key is not encumbered" attestations with revocable verifier types. For agent-swarm Sybil experiments it is a reference for how to gate participation on proof that a principal holds its own key outright, which is the countermeasure to identity rental through TEEs.

## Run notes

Not run. README commands: `npx hardhat compile` then `npx hardhat run scripts/verify.js --network hardhat`; tests with `npx hardhat test`. The full pipeline needs a physical Bitcoin mining ASIC and the pool software.

## Limitations

Research prototype, unmaintained since January 2023, 4 stars, no repo-level licence. Depends on specialised hardware for the PoW route; the mobile-TEE route lives in separate Android repos I did not inspect.
