---
id: gh-nymtech-nym
type: code
title: 'nym: Nym mixnet platform (nym-node mixnodes and gateways, clients, SOCKS5 proxy)'
repo: nymtech/nym
url: https://github.com/nymtech/nym
authors: [Nym Technologies SA]
year: 2020
language: Rust
license: Apache-2.0 (SPDX header in README; GitHub API detects no licence file)
stars: 1965
last_commit: 2026-10-02
topics: [fork-merge-security, sybil-resistance]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [piotrowska-2017-loopix]
---

## Summary

Nym is a production mix network in Rust maintained by Nym Technologies SA. The repository builds nym-node (running as mixnode, entry gateway or exit gateway), nym-client for embedding in applications, a SOCKS5 client for existing applications, a wallet and a CLI. Mixnodes shuffle Sphinx packets; gateways act as mailboxes so offline or firewalled clients can still receive. The README describes protection against network-level attackers and anonymous transactions via blinded, re-randomisable decentralised credentials. I read the README and repository metadata only.

## What it can do for us

A ready transport for experiments on hiding which sub-agent reports back: sub-agents could send results through the mixnet to a gateway mailbox instead of to the parent's address, giving Loopix-style unlinkability ([[piotrowska-2017-loopix]]) without writing a mixnet.

## Run notes

Not run. Build instructions are in the Nym operators guide linked from the README.

## Limitations

Real deployment depends on the public Nym network and its operators; latency in seconds is expected for mixnets ([[das-2018-anonymity]]); the README does not state which academic designs it implements, so the link to Loopix is my inference, not checked against Nym documentation.
