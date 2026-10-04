---
id: gh-ethereum-ethshadow
type: code
title: "Ethshadow: run a full Ethereum network of real clients (Lighthouse, Geth and others) inside Shadow"
repo: ethereum/ethshadow
url: https://github.com/ethereum/ethshadow
authors: ["Ethereum Foundation contributors"]
year: 2023
language: "Rust"
license: "GPL-3.0"
stars: 59
last_commit: 2025-03-12
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Simulates: an Ethereum proof-of-stake network (execution plus consensus clients, libp2p gossipsub and discv5) by running the real client binaries inside [[gh-shadow-shadow]]. Interaction model: discrete-event, real protocol code. Scale: not stated in the README. LLM-driven: no. Adversarial hooks: none packaged; one adds malicious or Sybil validators by building modified clients, and topology or latency through Shadow's network graph. Weight: Linux, requires building Lighthouse v5.3.0 and Geth v1.14.11 from source plus Shadow; heavy. The README states the point: no simulation-specific protocol code, so a protocol change is tested by implementing it in a client.

## What it can do for us

Closest off-the-shelf testbed for Ethereum p2p attacks we care about (gossip eclipse, validator Sybils, block propagation timing that matters for MEV and builder latency) with deterministic replay.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API. Linux-only via Shadow.

## Limitations

Last commit 2025-03-12, pinned to old client versions; small community (59 stars). No attack scenarios in the repo. No relay or builder (MEV-Boost) components mentioned in the README.
