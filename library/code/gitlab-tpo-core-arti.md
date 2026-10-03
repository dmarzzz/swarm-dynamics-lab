---
id: gitlab-tpo-core-arti
type: code
title: 'Arti: embeddable Rust implementation of the Tor client and onion services'
repo: tpo/core/arti (gitlab.torproject.org)
url: https://gitlab.torproject.org/tpo/core/arti
authors: [The Tor Project]
year: 2020
language: Rust
license: MIT OR Apache-2.0 (per crates/arti-client/Cargo.toml and LICENSE files)
stars: 9
last_commit: 2026-10-02
topics: [fork-merge-security, sybil-resistance]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [dingledine-2004-tor]
---

## Summary

Arti is the Tor Project's rewrite of Tor in Rust, hosted on the Tor GitLab (star count 9 there, which reflects GitLab usage, not adoption). The README states that as of August 2026 Arti is a full-featured Tor client with all relevant security features and support for connecting to onion services, judged suitable for general client use, while relay and directory authority support is in progress. It is designed as an embeddable library (`arti-client` crate, version 0.47.0 at access) rather than a SOCKS proxy with bolted-on integrations, and the project estimates at least half of C Tor's tracked security bugs would have been impossible in Rust. GitLab metadata: created August 2020, last activity 2 October 2026.

## What it can do for us

Q1: the practical way for a child agent to reach the parent, or a rendezvous point, without revealing network location, using Tor circuits and onion services [[dingledine-2004-tor]]. Because it embeds as a Rust library, each child can carry its own client and contact the parent through an onion service, so an observer of the foreign domain cannot link a child's traffic to the parent's address. Combined with the parent pulling reports from several onion addresses (or from a mixnet such as [[gh-nymtech-nym]]), it makes "which child will be merged" harder to infer from traffic. Tor's guard and directory designs are also worked examples of Sybil-resistant relay selection, hence the sybil-resistance tag.

## Run notes

Not run. Build with cargo from the repository; usage with Tor Browser is in `crates/arti/README.md`.

## Limitations

Tor hides network location, not behaviour: a child that is compromised in the foreign domain can simply tell the attacker where it will report. Relay support is incomplete. Tor is known to be vulnerable to traffic correlation by an adversary watching both ends, which is the relevant adversary if the attacker controls the foreign domain and can watch the parent's side.
