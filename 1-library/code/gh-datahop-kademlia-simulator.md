---
id: gh-datahop-kademlia-simulator
type: code
title: "kademlia-simulator: PeerSim-based Kademlia DHT simulator with malicious-node scenarios (discv5, data availability sampling)"
repo: datahop/kademlia-simulator
url: https://github.com/datahop/kademlia-simulator
authors: ["datahop"]
year: 2022
language: "Java"
license: "none stated"
stars: 9
last_commit: 2024-06-11
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulates: a Kademlia DHT on top of PeerSim (cycle- and event-driven Java P2P simulator), built for Ethereum discv5 service-discovery research and later data availability sampling (DAS). Interaction model: abstract message-passing nodes in a single JVM. Scale: not stated in the README. LLM-driven: no. Adversarial hooks: native malicious node classes (MaliciousProtocol.java, EvilDASProtocol and evil validator or non-validator variants) and configs under simulator/config/malicious, including a 25% evil-node config, plus a notebook comparing honest and evil runs. Weight: Java plus Maven, light, runs on a laptop.

## What it can do for us

The cheapest way to run a DHT Sybil or eclipse sweep (fraction of malicious nodes against lookup success) on a laptop, and a template for adding adversarial node classes to PeerSim.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API. Malicious-node files found by listing the repo tree.

## Limitations

Nine stars, no licence, tied to one research project. PeerSim abstracts away transport, so timing results do not transfer to real networks.
