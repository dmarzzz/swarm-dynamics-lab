---
id: ling-2026-how
type: paper
title: "How Agentic Is Agentic Commerce? A Population-Scale Measurement of x402 Adoption and Authenticity"
authors: ["Shengchen Ling", "Yajin Zhou", "Lei Wu", "Cong Wang"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2607.12575
doi: "10.48550/arXiv.2607.12575"
arxiv: "2607.12575"
cite: "Ling, S., Zhou, Y., Wu, L., & Wang, C. (2026). How Agentic Is Agentic Commerce? A Population-Scale Measurement of x402 Adoption and Authenticity. arXiv preprint arXiv:2607.12575."
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

A measurement study of x402 settlements on Base (with a coarser Solana census). It identifies settlements from on-chain events, resolves the true payer through the meta-transaction layer, and classifies each by what its trace can prove using a payment graph. Over a 280-day window Base carries 136,708,672 settlements worth 44,121,383.81 USD, concentrated on every axis (payer, recipient and value Gini all above 0.98). 21.20% of settlements are fictitious and 63.78% are internal settlement within a linked cluster. Genuinely independent value is bounded between 187,861.35 USD that demonstrably reaches a nameable service and 20,258,746.09 USD (45.92% of value) not provably manufactured. The manufacturable component is a star-shaped, machine-timed, gas-subsidised operator-driven economy. Conclusion: settlement count measures manufacturability, not adoption.

## Contribution

Empirical evidence that cheap per-request payments with sponsored gas do not by themselves impose Sybil cost: a party can manufacture most of the observed "agent economy" because the facilitator pays gas and nothing on-chain marks who controls a payment.

## Key results

- 136.7M settlements, 44.1M USD over 280 days on Base; Gini > 0.98 on payer, recipient and value (abstract).
- 21.20% fictitious, 63.78% intra-cluster; independent value between 0.19M and 20.26M USD (abstract).

## Methods and models

On-chain event extraction, meta-transaction payer resolution, payment-graph clustering. Not read beyond the abstract.

## Limitations and open questions

Clustering heuristics define "linked"; we did not check them. Solana coverage is coarser.

## Relevance to us

A direct, quantified Sybil finding for agent economies: identity-free payment rails let one operator simulate many agents and much activity at near-zero cost. Any metric of swarm activity or reputation that counts payments (for example [[shi-2025-sybil]]) is manipulable unless payments carry a real, non-subsidised cost or are tied to rate-limited identities ([[crapis-2026-zk]], [[rosenberg-2023-zk-creds]]). See also [[gh-x402-foundation-x402]].
