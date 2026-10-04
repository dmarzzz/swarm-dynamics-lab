---
id: quintus-2023-problems
type: blog
title: "The Problems Solved By SUAVE"
authors: [Quintus (Flashbots forum user; signs as Quintus); replies by Rahul Kothari (Aztec)]
year: 2023
url: https://collective.flashbots.net/t/the-problems-solved-by-suave/2816
site: collective.flashbots.net (Flashbots forum)
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Short forum post (15 December 2023, thread of 3 posts to May 2024) listing four categories of SUAVE use cases, all about one party making stronger commitments by running code in a TEE ("kettle"). The first category is "Removing Whitelists and Staking": counterparty behaviour is usually enforced by repeated games (whitelists) or ex-post penalties (fines, slashing), which bring capital inefficiency, monitoring overhead and high barriers to entry. If good behaviour is encoded in a SUAVE contract, "we can trust anyone running a kettle". Examples: CoW Swap solvers would not need to post slashable collateral, and searchers could encrypt order flow to all kettles instead of to whitelisted builders. The other categories are counterparty assurances, richer information sharing, and cheap verification via TEE signatures.

## Key claims

- TEE attestation can substitute for stake and whitelists as the admission mechanism for untrusted counterparties.
- The trusted party also benefits: builders need not convince searchers they are legitimate, solvers need not stake.
- In reply to Rahul Kothari's question whether solver staking (which deters quoting a good price then executing a bad one) can be replaced, the author points to executable quotes and to attestations such as "I am running this block building algo in private which clearly does not frontrun or unbundle you", not to private reputation.

## Evidence quality

Labelled by the author as "a researcher's observations", not a design spec. No analysis of what happens when attestation can be forged or when one operator runs many kettles.

## Relevance to us

States the design bet plainly: replace Sybil-resistance-by-capital (stake, slashing) and Sybil-resistance-by-reputation (whitelists) with attestation of behaviour. That works for integrity (any kettle behaves correctly) but drops the per-identity cost, so it only suffices where the number of participants does not matter. Where counts matter (voting, rate limits, rewards per node), attestation-only admission lets one operator add kettles at hardware cost, and after [[seto-2025-wiretap]] and [[chuang-2025-teefail]] possibly at the cost of one compromised CPU. BuilderNet's later fallback to allowlists [[collective-2025-why]] and the Proof of Cloud work [[rezabek-2025-proof]] show that the whitelist came back. Economic-security counterpart: [[charbonneau-2023-suave]]. TEE coprocessor design: [[miller-2024-sirrah]].
