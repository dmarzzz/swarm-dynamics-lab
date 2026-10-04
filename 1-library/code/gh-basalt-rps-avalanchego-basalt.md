---
id: gh-basalt-rps-avalanchego-basalt
type: code
title: "avalanchego-basalt: BASALT Sybil-resistant random peer sampling patched into AvalancheGo"
repo: basalt-rps/avalanchego-basalt
url: https://github.com/basalt-rps/avalanchego-basalt
authors: [Basalt RPS Authors]
year: 2020
language: Go
license: BSD-3-Clause
stars: 0
last_commit: 2020-09-22
topics: [sybil-resistance, sync-consensus]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [auvolat-2021-basalt]
---

## Summary

Research fork of AvalancheGo (Ava Labs' Go node) carrying the BASALT peer-sampling implementation from [[auvolat-2021-basalt]]. The work is on the `basalt` branch in a single commit, "Implement Basalt peer sampling" (22 Sep 2020, +579/-23 lines), adding `network/peer_sampling/basalt.go` (285 lines: seeded ranking, view slots, hit counters, hierarchical IP-prefix ranking), a cost model, a pluggable sampler interface with a default sampler, tracing, and hooks into the network layer and validator set so Avalanche consensus samples peers via BASALT instead of by stake. Skimmed via the GitHub API commit file list; source not read line by line.

## What it can do for us

A compact, real-world reference implementation of a stake-free, address-diversity Sybil defence for peer sampling, small enough to port into a simulation of gossip among agents (sample peers across provenance classes rather than uniformly).

## Run notes

Not run. It is a 2020 fork of AvalancheGo and would need that era's Go toolchain and network; porting the ~300-line sampler is the practical use.

## Limitations

Unmaintained since 2020, zero stars, tied to an old AvalancheGo version; the paper notes they had to disable connection management in live tests because peers banned them for too many connection attempts.
