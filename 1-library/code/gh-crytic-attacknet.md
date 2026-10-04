---
id: gh-crytic-attacknet
type: code
title: "Attacknet: chaos testing of blockchain devnets with network, clock and container faults (Trail of Bits)"
repo: crytic/attacknet
url: https://github.com/crytic/attacknet
authors: ["Trail of Bits"]
year: 2023
language: "Go"
license: "AGPL-3.0"
stars: 75
last_commit: 2025-07-09
topics: [sync-consensus, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulates: faults on a real Ethereum devnet: clock skew, network splits, packet loss, corruption, latency, bandwidth limits, container kills and restarts, I/O latency and errors, CPU and memory stress. Interaction model: real clients in Kubernetes launched by Kurtosis ([[gh-ethpandaops-ethereum-package]]), faults injected by Chaos Mesh, health checks at the end; a planner generates fault-by-target matrices. Scale: not stated. LLM-driven: no. Adversarial hooks: partitions and degraded nodes natively; not Sybil identities or Byzantine (equivocating) behaviour. Weight: heavy, needs a containerd Kubernetes cluster (1.27 or older), Chaos Mesh, Kurtosis engine and gateway. A Trail of Bits blog post (2024-03-18, seen only as a search snippet) says it was used to test the Dencun hard fork.

## What it can do for us

Borrow its fault taxonomy and planner idea (matrix of fault types by target classes) for agent-swarm chaos tests; partition and clock-skew faults are the network analogue of a sub-agent going stale before a merge.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

AGPL-3.0. Infrastructure-heavy; non-deterministic emulation; no identity-level attacks.
