---
id: gh-teksander-toychain
type: code
title: "Toychain: lightweight Python blockchain with pluggable consensus for swarm robotics research"
repo: teksander/toychain
url: https://github.com/teksander/toychain
authors: ["Alexandre Pacheco"]
year: 2023
language: Python
license: "none stated"
stars: 1
last_commit: 2026-05-01
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [pacheco-2024-toychain]
---

## Summary

Python toy blockchain where each node is an object with its own host, port, consensus module and custom timer driven by robot control steps. New consensus protocols implement verify_chain, a block-generation thread and a genesis block; proof of work options include mining difficulty. Maintained by Alexandre Pacheco (GitHub profile: research on robot swarms self-organising with blockchains), author of [[pacheco-2024-toychain]]. The link between repo and report is inferred from the matching name and author, not stated in the arXiv abstract.

## What it can do for us

Quick way to add a ledger with deposits or authority-based admission to a Python agent simulation, to test economic Sybil resistance without Ethereum.

## Run notes

Not run. README read via the GitHub API on 2026-10-03.

## Limitations

One star, no licence reported, research-grade code.
