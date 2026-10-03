---
id: gh-libp2p-gossipsub-hardening
type: code
title: "gossipsub-hardening: Testground plans that attack gossipsub with Sybil, eclipse and covert-flash adversaries"
repo: libp2p/gossipsub-hardening
url: https://github.com/libp2p/gossipsub-hardening
authors: ["Protocol Labs"]
year: 2020
language: "Python"
license: "none stated"
stars: 13
last_commit: 2025-05-01
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [vyzovitis-2020-gossipsub]
---

## Summary

Simulates: a gossipsub pub-sub mesh with three node groups (publishers, lurkers, attackers) on [[gh-testground-testground]]. Interaction model: real Go gossipsub nodes in containers; Python generates composition files and Jupyter notebooks analyse latency and peer-score data. Scale: the README reports 500 containers on a 56-core Xeon with 124 GiB RAM, about 25 on a 16 GB MacBook, larger runs on Kubernetes. LLM-driven: no. Adversarial hooks: native. Attacker hosts run badboy.go, a minimal gossipsub with Sybil behaviour, configured through SybilParams; scenarios include eclipse and the covert flash attack studied in [[vyzovitis-2020-gossipsub]]. Weight: Testground plus Docker or Kubernetes.

## What it can do for us

A ready, parameterised Sybil and eclipse attack harness against the peer-scoring defence specified in [[gh-libp2p-specs]]. Its scoring-versus-Sybil design is the baseline any agent-swarm reputation experiment should compare against.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

No licence file. Depends on the unmaintained Testground. Analysis needs 8 GB or more RAM. Attackers are scripted, not adaptive.
