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
