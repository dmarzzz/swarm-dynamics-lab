---
id: shi-2025-sybil
type: paper
title: "Sybil-Resistant Service Discovery for Agent Economies"
authors: ["David Shi", "Kevin Joo"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2510.27554
doi: "10.48550/arXiv.2510.27554"
arxiv: "2510.27554"
cite: "Shi, D., & Joo, K. (2025). Sybil-Resistant Service Discovery for Agent Economies. arXiv preprint arXiv:2510.27554."
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

A 5-page proposal for ranking x402-enabled HTTP services (APIs, data feeds, inference providers that accept crypto payments) when agents must choose which to trust. TraceRank seeds addresses with precomputed reputation and propagates reputation along payment flows, weighting by transaction value and recency, so payments act as endorsements; it is combined with semantic search for natural-language queries. The authors argue this resists Sybil attacks because spam services paid by many low-reputation addresses rank below legitimate services paid by a few high-reputation ones.

## Contribution

Applies trust-propagation (PageRank-style) Sybil defence to the agent payment graph rather than to a social graph.

## Key results

- Algorithm and argument only; the abstract reports no measured evaluation.

## Methods and models

Reputation propagation over the x402 payment graph. Not read beyond the abstract.

## Limitations and open questions

Sybil resistance depends on the seed reputation set and on wash payments being expensive; [[ling-2026-how]] measures that a large share of x402 settlements are fictitious or internal to linked clusters, which is exactly the input this ranking consumes.

## Relevance to us

Represents the graph-based (non-cryptographic) branch of agent Sybil defence: rank by who pays whom. It complements credential schemes, which bound how many identities a principal holds, with a way to rank services when identities are cheap. Pair with [[gh-x402-foundation-x402]] and [[li-2026-five]].
