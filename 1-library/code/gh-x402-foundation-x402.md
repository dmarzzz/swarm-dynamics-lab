---
id: gh-x402-foundation-x402
type: code
title: "x402: open HTTP 402 payment standard and SDKs"
repo: x402-foundation/x402
url: https://github.com/x402-foundation/x402
authors: ["x402 Foundation (originally Coinbase)"]
year: 2025
language: TypeScript
license: Apache-2.0
stars: 6675
last_commit: 2026-10-02
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Reference specification and SDKs (TypeScript, Python, Go) for x402, an open standard for internet-native payments over HTTP. A resource server answers 402 Payment Required with a PAYMENT-REQUIRED header listing accepted (scheme, network) payment requirements; the client retries with a PAYMENT-SIGNATURE header carrying a signed payload; the server verifies locally or via a facilitator's /verify endpoint, serves the resource, and settles on-chain directly or via /settle, returning a PAYMENT-RESPONSE header. Schemes are pluggable (exact is the first; upto is described as a future metered scheme). The coinbase/x402 repo (README read, 167 lines) now says the project moved to the x402 Foundation and coinbase/x402 is a development fork; repo metadata here is from x402-foundation/x402.

## What it can do for us

Turns any HTTP endpoint an agent calls into a paid endpoint with a one-line middleware, so per-request payment can serve as the Sybil cost in agent-swarm experiments.

## Run notes

Not run. Install: `npm install @x402/core @x402/evm @x402/svm @x402/fetch` (client) or `@x402/express` (server); `pip install x402`.

## Limitations

Payments are attributable on-chain to payer addresses, so it gives Sybil cost without anonymity (contrast [[crapis-2026-zk]]). [[li-2026-five]] reports five practical attacks (unpaid service or paid-but-denied). [[ling-2026-how]] measures that with facilitator-sponsored gas, a large share of settlements are fictitious or intra-cluster, so payment counts are cheap to manufacture. Reputation over its payment graph: [[shi-2025-sybil]].
