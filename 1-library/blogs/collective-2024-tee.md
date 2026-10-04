---
id: collective-2024-tee
type: blog
title: "TEE-Boost"
authors: [shea]
year: 2024
url: https://collective.flashbots.net/t/tee-boost/3741
site: collective.flashbots.net (Flashbots forum)
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Flashbots design proposal (August 2024) to reduce and eventually remove the MEV-Boost relay by letting validators accept TEE proofs directly from block builders. Builders would run pinned, attested software whose measurement is allowlisted; once per epoch they submit a full attestation, and per block they sign bids with a key generated inside the TEE. The post lists what relays do today (privacy, validation, data availability, safe multiplexing including spam protection) and asks openly whether removing the relay exposes validators and builders to DoS from each other.

## Key claims

- About 90% of Ethereum blocks are served by about 5 centralised relays (stated by the author).
- Relays currently resimulate blocks or require builders to stake collateral for optimistic bids, and they shield validators and builders from spam and hide their IPs.
- Two-phase proof: per-epoch attestation verification, then a cheap per-block signature with a TEE-held key, "reducing work in the hot path and the cost of spam".
- Integrity rests on the assumption that the hardware vendor and cloud provider would both have to collude to forge proofs.
- Open questions include whether validators face more DoS when MEV-Boost must process one bid per builder rather than one per relay, and whether builders face new DoS vectors from validators.

## Evidence quality

Early design proposal from the operator, with an explicit list of open questions; no implementation results in the post.

## Relevance to us

Shows how an attested key can stand in for a reputation-bearing identity in a permissionless market: verification is front-loaded once per epoch, and every later message is cheaply checkable against an allowlisted measurement. The open DoS questions are the remaining Sybil problem: the number of attested builders is bounded only by how many attested machines an operator can run, which the attestation itself does not limit ([[collective-2024-portrait]]). For agent swarms, the same two-phase pattern (expensive identity admission, cheap per-message authentication) is practical, but admission must be scarce for it to bound Sybils. Context: relay-era defences in [[gh-flashbots-mev-boost-relay]] and [[flashbots-2022-relay]].
