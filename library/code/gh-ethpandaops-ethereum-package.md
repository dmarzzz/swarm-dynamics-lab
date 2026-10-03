---
id: gh-ethpandaops-ethereum-package
type: code
title: "ethereum-package: Kurtosis package for private multi-client Ethereum devnets with MEV-Boost relays and builders"
repo: ethpandaops/ethereum-package
url: https://github.com/ethpandaops/ethereum-package
authors: ["ethPandaOps"]
year: 2022
language: "Starlark"
license: "MIT"
stars: 481
last_commit: 2026-09-28
topics: [sync-consensus, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Simulates: a private Ethereum testnet of n execution and consensus client pairs over Docker or Kubernetes, with genesis generation, a transaction spammer, Grafana and Prometheus, Blobscan, and optional PBS infrastructure through mev-boost with flashbots, helix, mev-rs, commit-boost or mock relays. Interaction model: real clients in containers in real time. Scale: n is a parameter; no figure in the README. LLM-driven: no, but agents can attach over JSON-RPC. Adversarial hooks: none native; it is the substrate that [[gh-crytic-attacknet]] attacks. Weight: Docker plus the Kurtosis CLI; `kurtosis run --enclave my-testnet github.com/ethpandaops/ethereum-package`.

## What it can do for us

The fastest way to get a live PBS stack (proposers, relays such as [[gh-flashbots-mev-boost-relay]], builders) to drop LLM searcher or builder agents into; actively maintained by the Ethereum DevOps team.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API. Not run because a multi-client devnet needs more than the ten-minute budget.

## Limitations

Real-time emulation, so not deterministic; resource-heavy with many clients. No attacker or Sybil tooling built in.
