---
id: gh-jackyzha0-bft-json-crdt
type: code
title: 'bft-json-crdt: JSON-like Byzantine fault tolerant CRDT implementing Kleppmann 2022 in Rust'
repo: jackyzha0/bft-json-crdt
url: https://github.com/jackyzha0/bft-json-crdt
authors: [Jacky Zhao]
year: 2022
language: Rust
license: MIT
stars: 234
last_commit: 2024-04-15
topics: [fork-merge-security, sync-consensus]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: [kleppmann-2022-making, kleppmann-2020-byzantine]
---

## Summary

An instructional Rust implementation of the ideas in "Making CRDTs Byzantine Fault Tolerant" [[kleppmann-2022-making]] on top of a simplified Automerge-style list CRDT, composed into a JSON CRDT with list and last-writer-wins register nodes. Every operation carries a hash-based id over its fields and an Ed25519 signature by its author; `BaseCrdt::apply` rejects ops whose signature does not match the claimed author (`ErrDigestMismatch`) or whose content does not match its id (`ErrHashMismatch`, which catches equivocation where an author reuses an id with different content), and queues ops whose causal dependencies have not arrived. The README benchmark (author's 2019 MacBook Pro) reports the BFT variant replaying a 259k-op editing trace in 335 s versus 88.6 s without BFT, using 59.5 MB.

## What it can do for us

Q2: a concrete merge rule for children's state that converges among honest replicas no matter how many replicas are Byzantine, which is the property Kleppmann proves for Byzantine eventual consistency [[kleppmann-2020-byzantine]]. Running the tests made the boundary of that guarantee clear: the code rejects forged and equivocating ops, but a validly signed op from a compromised child is applied like any other. So a BFT CRDT gives "no threshold needed for consistency" but "threshold 1 for content": it stops a corrupted child from splitting the parent's state or impersonating siblings, and does nothing about a corrupted child that writes poison under its own key. The test file also lists eclipse attacks and unbounded future-dated queues as untested Byzantine behaviours, which are relevant to a parent that waits on children.

## Run notes

Ran on macOS (Apple silicon) with the local Rust toolchain:
`git clone --depth 1 https://github.com/jackyzha0/bft-json-crdt.git && cd bft-json-crdt && cargo test --test byzantine` gave 3 passed (test_equivocation, test_forge_update, test_path_update) in 0.01 s after compile. `cargo test --test commutative` gave 1 passed (test_list_fuzz_commutative) in 0.46 s. A full `cargo test` including the Kleppmann editing-trace replay did not finish within 10 minutes in a debug build, so I stopped it.

## Limitations

The author describes it as a learning project: Vec-backed storage, over 168 bytes per op, no persistence, no network transport, an unbounded message queue. Last commit April 2024. Malformed messages and eclipse attacks are explicitly out of scope of the tests.
