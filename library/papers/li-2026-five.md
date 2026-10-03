---
id: li-2026-five
type: paper
title: "Five Attacks on x402 Agentic Payment Protocol"
authors: ["Zelin Li", "Qin Wang", "Zhipeng Wang"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2605.11781
doi: "10.48550/arXiv.2605.11781"
arxiv: "2605.11781"
cite: "Li, Z., Wang, Q., & Wang, Z. (2026). Five Attacks on x402 Agentic Payment Protocol. arXiv preprint arXiv:2605.11781."
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

x402 revives HTTP 402 Payment Required for web-native micropayments to APIs, content and agents, combining synchronous HTTP authorization with asynchronous blockchain settlement. The authors formally analyse x402 and present five concrete attacks on authorization, binding, replay protection and web-layer handling, validated on local chains, Base Sepolia and live endpoints, plus an audit of three open-source SDKs and endpoints. All five attacks are practical and produce either unpaid service or paid-but-denied outcomes. Mitigations are proposed. Preprint, 17 pages.

## Contribution

First security analysis we found of x402 as a protocol, relevant because payment-per-request is being proposed as the Sybil cost for agents.

## Key results

- Five practical attacks across stages of the payment flow; two outcome classes (free service, or paid but denied) (abstract).

## Methods and models

Formal analysis plus reproducible testbed. Not read beyond the abstract.

## Limitations and open questions

Not read in full; which attacks remain after the x402 v2 spec changes is not checked.

## Relevance to us

If payment is the Sybil cost for agents, a replay or binding bug that yields unpaid service makes Sybils free again. Any swarm design that prices agent actions with x402 should check these attacks. See [[gh-x402-foundation-x402]], [[ling-2026-how]], and the anonymous alternative [[crapis-2026-zk]].
