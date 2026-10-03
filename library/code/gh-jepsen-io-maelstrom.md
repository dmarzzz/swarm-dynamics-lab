---
id: gh-jepsen-io-maelstrom
type: code
title: "Maelstrom: Jepsen workbench that runs toy distributed-system nodes over a simulated network and checks consistency"
repo: jepsen-io/maelstrom
url: https://github.com/jepsen-io/maelstrom
authors: ["Kyle Kingsbury"]
year: 2017
language: "Clojure"
license: "EPL-1.0"
stars: 3707
last_commit: 2026-07-10
topics: [fork-merge-security, sync-consensus]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulates: a network that routes JSON messages over stdin and stdout between user-written node processes in any language, with workloads (broadcast, CRDT g-set and g-counter, transactional key-value, Raft) and checkers up to strict serialisability (via Elle). Interaction model: real processes, simulated network with latency, message loss and partitions. Scale: 25 or more nodes; 60,000 messages per second on a 48-way Xeon per the README. LLM-driven: a node could wrap an LLM, nothing built in. Adversarial hooks: partitions, latency and loss natively; no Byzantine or Sybil nodes. Weight: JVM; light, runs on a laptop.

## What it can do for us

A ready consistency oracle for merge semantics: write fork-and-merge agent memory as a Maelstrom node, then let the CRDT or transactional checkers find anomalies under partitions. Byzantine merges ([[gh-ept-byzantine-eventual]]) are not covered and would need a custom checker.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Crash-fault model only; no malicious nodes. Toy scale by design.
