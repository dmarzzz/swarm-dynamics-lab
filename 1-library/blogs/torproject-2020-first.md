---
id: torproject-2020-first
type: blog
title: "A First Take at PoW Over Introduction Circuits (Tor Proposal 327)"
authors: ["George Kadianakis", "Mike Perry", "David Goulet", "tevador"]
year: 2020
url: https://spec.torproject.org/proposals/327-pow-over-intro.html
site: Tor Project specifications (proposal 327)
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

Tor design proposal 327 (created 2 April 2020, status Closed) adds client proof-of-work to onion-service introductions, because floods of INTRODUCE cells force the service to build costly rendezvous circuits. Clients solve Equi-X (an asymmetric, CPU-oriented puzzle built on Equihash<60,3> and HashX); effort is a linear score (2^32 - 1) / hash prefix, and the service processes introductions from a priority queue ordered by effort rather than accepting or rejecting them. The service publishes a suggested effort in its descriptor and adjusts it every 300 s with an AIMD-like rule based on queue backlog and discarded effort; it drops to zero when not under attack.

## Key claims

- Attacker model: script kiddie (about 10 GHz CPU), small botnet of 500 machines (about 400 USD), large botnet of 100k machines (about 36k USD); the proposal targets the first two and states it cannot stop the large botnet.
- Attack analysis: at 1 ms verification an attacker saturates verification with 793 invalid cells/s; a hybrid of 91 high-effort plus 1,520 invalid requests/s saturates both stages; precomputation window of about 4 hours from seed rotation.
- Limitations: no end-to-end ACK to tell clients their PoW was too low, single-threaded verification, poor fit for battery-limited mobile clients.
- Names third-party anonymous tokens (issued for CAPTCHA or PoW) as the follow-on direction, which became [[torproject-2021-res]].

## Evidence quality

Design specification with back-of-envelope attacker economics, not measurements. Read via a summarising fetch, so depth is skim. Later deployed in Tor (not checked here).

## Relevance to us

Onion services face the same problem as an open agent endpoint: anonymous callers, no identity to block, and a costly per-request operation. PoW-as-priority (not as gate) with an adaptive price is a credential-free Sybil defence that keeps the service usable for honest anonymous callers under attack, at the cost of failing against large botnets. For agent swarms, compute-priced priority queues are a baseline against which credential schemes ([[davidson-2018-privacy]], [[yun-2026-anonymous]]) and payment schemes ([[crapis-2026-zk]]) should be compared.
