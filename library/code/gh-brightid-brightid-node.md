---
id: gh-brightid-brightid-node
type: code
title: "BrightID-Node: node software that stores and serves the BrightID social graph for proof of uniqueness"
repo: BrightID/BrightID-Node
url: https://github.com/BrightID/BrightID-Node
authors: ["BrightID contributors"]
year: 2017
language: "JavaScript"
license: "ISC"
stars: 52
last_commit: 2026-05-03
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

BrightID nodes host the social graph of BrightID, a system where people verify each other through face-to-face or video connection parties and applications query whether an account is a unique human. The README is short and points to a wiki with a development guide, an installation guide for running a node and an API spec for integrators. Issues carry bounties paid in BrightID Subs tokens. The repo has 52 stars, was created in 2017 and last received a push in May 2026.

## What it can do for us

An operational example of graph-based Sybil resistance with a federated set of nodes that each hold the graph and run the anti-Sybil ranking from [[gh-brightid-brightid-antisybil]]. Relevant if we want an agent swarm to rely on vouching between agents rather than on hardware or biometrics.

## Run notes

Not run. README read via the GitHub API on 2026-10-03.

## Limitations

README is a pointer page; the substance is in the wiki and the API spec. Node operators must be trusted to run the ranking honestly. Low recent activity relative to its 2020 to 2022 peak (inferred from stars and commit dates only).
