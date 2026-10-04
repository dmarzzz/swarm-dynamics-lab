---
id: gh-vacp2p-zerokit
type: code
title: "zerokit: Rust zero-knowledge modules, mainly the RLN implementation used by Waku for anonymous spam protection"
repo: vacp2p/zerokit
url: https://github.com/vacp2p/zerokit
authors: ["Vac (vacp2p)"]
year: 2022
language: "Rust"
license: "Apache-2.0 (README also shows MIT badge)"
stars: 148
last_commit: 2026-10-03
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Rust library implementing Rate-Limiting Nullifier per the RLNv2 specification, with Circom circuits proven via arkworks Groth16, plus the Multi-Message-ID burn extension that lets one proof consume several message units. It cross-compiles, exposes a C FFI and builds to WebAssembly. The README lists nwaku (the Nim Waku v2 node) and js-rln as users, which makes this the production RLN stack for the Waku peer-to-peer messaging network. Active: last push 2026-10-03.

## What it can do for us

A deployable library if an experiment needs real RLN proofs inside agent messaging, for example rate-limiting each agent in a gossip network with a stake behind it. Production counterpart to the circuits in [[gh-rate-limiting-nullifier-circom-rln]].

## Run notes

Not run. `make installdeps && make build && make test` per README; also `nix develop`.

## Limitations

Groth16 needs a trusted setup per circuit. Waku is the main deployment; performance figures were not in the README.

## Notes from dmarz/sybil-credentials

Paper behind this stack: [[taheri-boshrooyeh-2022-privacy]] (WAKU-RLN-RELAY), which reports, citing the earlier kilic/rln library, about 0.5 s membership proof generation for a 2^32 group on an iPhone 8, about 30 ms verification and a 3.89 MB prover key. The README (read this session) states the current implementation follows the RLNv2 spec at lip.logos.co, which allows a per-member message limit per epoch instead of the single message of the original proposal [[barrywhitehat-2019-semaphore]].
