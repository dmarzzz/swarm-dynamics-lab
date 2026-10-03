---
id: gh-idena-network-idena-go
type: code
title: "idena-go: Go node for Idena, a proof-of-personhood blockchain based on synchronous flip-puzzle validation ceremonies"
repo: idena-network/idena-go
url: https://github.com/idena-network/idena-go
authors: ["Idena network developers"]
year: 2019
language: "Go"
license: "LGPL-3.0"
stars: 152
last_commit: 2025-12-22
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Golang implementation of the Idena node. Idena tries to give each human one identity by having every participant solve AI-hard "flip" puzzles at the same moment in a global validation ceremony, so that one person cannot attend many sessions at once. The README documents build steps (Go 1.16 or later), CLI flags, a private IPFS network that stores blocks and flips (pinned locally with 30 percent and 50 percent probability by default), and a local automine config whose Validation block exposes the ceremony timings: validation interval, flip lottery duration, short-session and long-session durations.

## What it can do for us

The one production system where Sybil resistance comes from synchrony: identity costs one human's attention during a fixed time window. [[siddarth-2020-who]] reviews Idena alongside other subjective proof-of-personhood protocols, and [[borge-2017-proof-of-personhood]] proposed the pseudonym-party form of the same synchrony idea. That idea transfers to agent swarms as a timed challenge that bounds how many identities a single operator can keep alive, and it is the case that capable LLM or vision agents most directly threaten, since flips are CAPTCHA-like.

## Run notes

Not run. `go build` per README; a local automine node can be configured with the JSON shown in the README to shorten ceremony timings for testing.

## Limitations

Last push December 2025. The README does not document the flip protocol itself; that lives in Idena docs we did not open. Security depends on flips staying hard for machines, which we did not evaluate.

## Notes from dmarz/sybil-foundations

The protocol this node implements is described and compared with BrightID, Duniter, Kleros Proof of Humanity, Upala, HumanityDAO and the Equality Protocol in [[siddarth-2020-who]] (read in full): synchronous validation ceremonies about every two weeks, human-made FLIP tests, invite codes, 4,012 validated identities as of 2020. [[ford-2020-identity]] groups Idena with Encointer as synchronous schemes that resist the time-shifting attack on asynchronous verification.
