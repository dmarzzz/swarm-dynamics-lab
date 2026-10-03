---
id: gh-testground-testground
type: code
title: "Testground: platform for testing and simulating distributed and P2P systems from 2 to 10k instances"
repo: testground/testground
url: https://github.com/testground/testground
authors: ["Protocol Labs"]
year: 2019
language: "Go"
license: "Apache-2.0 OR MIT (GitHub reports NOASSERTION)"
stars: 436
last_commit: 2023-05-30
topics: [sybil-resistance, sync-consensus, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulates: real P2P software (libp2p, IPFS, Filecoin) in containers with traffic shaping between instances. Interaction model: emulation in real time; test plans are written like unit tests against local APIs, with a sync service for barriers and pub-sub between instances; runners local:exec, local:docker and cluster:k8s. Scale: README says 2 to 10k instances. LLM-driven: no, but any containerised process works. Adversarial hooks: per-group parameters let one group run attacker code (used in [[gh-libp2p-gossipsub-hardening]] for Sybil and eclipse attacks); latency, bandwidth and partitions through the network sidecar. Weight: Go plus Docker locally, Kubernetes on AWS for large runs. Built by Protocol Labs.

## What it can do for us

The pattern of "groups" (publishers, lurkers, attackers) with separate parameters is exactly the shape of a Sybil-injection experiment, and existing gossipsub attack plans run on it.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Last commit 2023-05-30; effectively unmaintained. Real-time emulation, so not deterministic or replayable (unlike Shadow). Binaries are not distributed; build from source with Go and Docker.
