---
id: crapis-2026-zk
type: blog
title: "ZK API Usage Credits: LLMs and Beyond"
authors: ["Davide Crapis", "Vitalik Buterin"]
year: 2026
url: https://ethresear.ch/t/zk-api-usage-credits-llms-and-beyond/24104
site: Ethereum Research forum (ethresear.ch)
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: skim
relevance: 5
---

## Summary

A research-forum design post (11 February 2026) for paying for API calls, LLM inference in particular, privately. A user generates a secret key, derives an identity commitment and deposits D into a contract that keeps commitments in a Merkle tree. Each request uses a strictly increasing ticket index i and carries a ZK proof of solvency, (i + 1) * C_max <= D + R, where C_max is the maximum per-request cost and R is the sum of server-signed refund tickets the user has collected privately (the server refunds C_max - C_actual after execution). Rate-Limiting Nullifiers bind each ticket: slope a = Hash(k, i), signal y = k + a * x with x = Hash(message), nullifier Hash(a). Reusing a ticket index with a different message reveals k, and the deposit D can be claimed by anyone who proves the double-signal. A separate policy stake S can be burned, but not claimed, by the server for policy violations, so the server gains nothing by false bans. The thread discusses a v2 that re-randomises encrypted refund totals to avoid linkability.

## Key claims

- Deposit once, make thousands of calls; the provider is guaranteed payment and spam protection, and requests are unlinkable to the depositor and to each other unless the user double-spends.
- Worked example in the post: 100 USDC deposit, 500 LLM queries, none linkable to the depositor or each other.
- Applies to LLM inference, RPC, image generation, cloud compute, VPNs and data APIs.
- Commenters raise side channels: inference metadata (output token count, time-to-first-token) and shared-cache timing leaks (citing vLLM CVE-2025-46570, about 99% request correlation) can re-link requests despite payment anonymity; parallel requests in the homomorphic variant force over-provisioning.

## Evidence quality

Design proposal with protocol sketch and forum discussion; no implementation measurements in the post as read. Web search results (Ethereum Foundation blog, 1 October 2026) report a mainnet implementation called zkAPI; we did not open that post, so this is not checked. Read via a summarising fetch of the thread, so depth is skim. Builds on RLN ([[barrywhitehat-2019-semaphore]], [[taheri-boshrooyeh-2022-privacy]]).

## Relevance to us

This is the clearest current design for "payment as anonymous Sybil cost" for AI agents: every agent call is paid from a stake, unlinkable, and over-spending forfeits the stake. For agent swarms it bounds total consumption by deposit rather than by identity count, so spinning up more agents does not help a principal unless it deposits more. The dual-stake split (claimable for cryptographic double-spend, burn-only for policy) is a reusable pattern for slashing misbehaving agents without giving the judge a profit motive. Contrast identity-revealing payment rails [[gh-x402-foundation-x402]] and [[gh-lightninglabs-aperture]], and the measured manipulability of x402 activity in [[ling-2026-how]].
