---
id: gh-davidrusu-bft-crdts
type: code
title: 'bft-crdts: Byzantine fault tolerant eventually consistent algorithms over secure broadcast (Maidsafe research)'
repo: davidrusu/bft-crdts
url: https://github.com/davidrusu/bft-crdts
authors: [David Rusu]
year: 2020
language: Rust
license: MIT/BSD-3 stated in README; none detected by GitHub API
stars: 63
last_commit: 2025-12-11
topics: [fork-merge-security, sync-consensus]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [kleppmann-2020-byzantine]
---

## Summary

Research code funded by Maidsafe that layers a Byzantine fault tolerant network over eventually consistent algorithms. The README describes three layers: an inner algorithm that validates and applies operations (an ORSWOT set CRDT, a distributed bank, and an AT2 asset-transfer implementation), a deterministic Secure Broadcast layer after Malkhi and Reiter that prevents conflicting operations from the same actor being accepted (double-spend protection, source ordering), and an in-memory network layer that assumes reliable but unordered delivery. Algorithms implement a `SecureBroadcastAlgorithm` trait with a `validate` hook where algorithm-specific Byzantine checks go. Correctness properties are checked with quickcheck over random network behaviours, and tests emit message sequence charts.

## What it can do for us

Q2: unlike [[gh-jackyzha0-bft-json-crdt]], secure broadcast adds a quorum step, so an operation is accepted only after enough peers have acknowledged it. That is the place where a k-of-n rule lives in a merge protocol: a parent could require that a child's contribution be co-signed by a quorum of sibling children before it is applied. The `validate` hook is where content checks (not just signature checks) would go. Compared with Byzantine eventual consistency [[kleppmann-2020-byzantine]], this design trades the "any number of faults" guarantee for agreement, which is the trade a fork-merge parent faces.

## Run notes

Not run. README: install Rust, then `QUICKCHECK_TESTS=1000 cargo test`; render `.msc` outputs with mscgen.

## Limitations

Simulated in-memory network with no packet loss. Sporadic maintenance (last push December 2025). The README does not state the fault threshold of its secure broadcast; I did not read the source to confirm it.
