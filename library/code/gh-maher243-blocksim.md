---
id: gh-maher243-blocksim
type: code
title: "BlockSim: Python discrete-event simulator for blockchain network, consensus and incentive layers"
repo: maher243/BlockSim
url: https://github.com/maher243/BlockSim
authors: ["Maher Alharby", "Aad van Moorsel"]
year: 2019
language: "Python"
license: "none stated"
stars: 103
last_commit: 2022-03-26
topics: [sync-consensus]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: [alharby-2020-blocksim]
---

## Summary

Simulates: blockchains in three abstraction layers (network, consensus, incentives) with Base, Bitcoin and Ethereum models; outputs ledger, stale and uncle blocks and per-miner rewards to Excel. Interaction model: Python discrete-event. Scale: not stated in the README. LLM-driven: no. Adversarial hooks: none native (no attack files in the tree); hash-power fractions per node are configurable, which supports majority or concentration questions. Weight: pure Python plus pandas, numpy, sklearn and xlsxwriter; light.

## What it can do for us

Little beyond a readable reference for layering a blockchain simulation; superseded for our purposes by Ethereum-specific tools.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Last commit 2022-03-26, no licence file, proof-of-work era models, no adversaries.
