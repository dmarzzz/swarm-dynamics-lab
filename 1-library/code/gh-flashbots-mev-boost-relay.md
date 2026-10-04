---
id: gh-flashbots-mev-boost-relay
type: code
title: "mev-boost-relay: Flashbots MEV-Boost relay, with per-builder priority, blacklist, collateral and demotion as its builder-identity controls"
repo: flashbots/mev-boost-relay
url: https://github.com/flashbots/mev-boost-relay
authors: [Flashbots]
year: 2022
language: Go
license: AGPL-3.0
stars: 499
last_commit: 2026-08-10
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Reference implementation of the MEV-Boost relay used in Ethereum proposer-builder separation, maintained by Flashbots (repo created 2022-05-20). Builders submit blocks keyed by a BLS builder public key; the relay simulates them and serves the best bid to validators. Its builder table records, per public key, is_high_prio, is_blacklisted, is_optimistic, collateral and a builder_id that groups several keys under one entity. Optimistic submissions are accepted before simulation if collateral is posted, and a failed simulation demotes every key sharing the builder_id.

## What it can do for us

- Shows a production identity layer for a permissionless producer market: unknown keys default to low priority with no collateral (logged as "unable to read builder ... using low-prio and no collateral"), known keys can be promoted to high priority, and keys can be blacklisted.
- Identity aggregation: SetBlockBuilderIDStatusIsOptimistic updates is_optimistic for all rows with the same builder_id, so one entity cannot escape a demotion by switching to another of its keys. This is the code-level answer to the "many accounts and stakes" objection raised in [[flashbots-2022-relay]], although grouping keys into a builder_id is an operator decision, not something the relay can infer.
- Collateral-backed optimism: a builder whose optimistic block fails simulation is demoted (with a carve-out for transient simulation errors); collateral is stored per builder and exposed through an internal endpoint (how it is used to compensate proposers was not checked in the code).
- Simulation load control: a built-in blocksim rate limiter (BLOCKSIM_MAX_CONCURRENT, default 4 per API node) or the external flashbots/prio-load-balancer service (not catalogued separately) with high-priority and low-priority queues. A 2022 forum note states the production relay limited block submissions to 2 per second per IP address.

## Run notes

Not run. Read the README, database types and migrations, and the builder status, collateral and demotion paths in services/api/service.go.

## Limitations

The relay trusts its operator to assign priority, blacklist and builder_id groupings; there is no protocol-level Sybil resistance for new keys beyond low priority and IP rate limits. AGPL-3.0 licence.

## Relevance to us

The relay is a working answer to the questions debated in [[flashbots-2021-proposal]] and [[flashbots-2022-relay]]: new identities are admitted freely but start at the bottom (low priority, no optimistic path), privileges are granted by the operator on evidence, and penalties attach to an operator-declared entity (builder_id) rather than to a single key, so key rotation does not reset them. For agent swarms, the transferable parts are default-low trust for new identities and grouping identities into accountable entities before applying penalties; the non-transferable part is that the grouping relies on off-chain knowledge of who runs which keys.
