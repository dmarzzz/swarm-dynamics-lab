---
id: wang-2026-when
type: paper
title: 'When HTTP 402 Meets the Blockchain: Risks on Emerging x402 Payments'
authors:
- Qinying Wang
- Yong Yang
- Yuan Chen
- Shouling Ji
- Mathias Payer
year: 2026
venue: USENIX Security 2026 (arXiv preprint)
url: https://arxiv.org/abs/2607.19545
doi: null
arxiv: '2607.19545'
cite: 'Wang, Q., Yang, Y., Chen, Y., Ji, S., & Payer, M. (2026). When HTTP 402 Meets the Blockchain: Risks on Emerging x402 Payments. In Proceedings of the 35th USENIX Security Symposium (USENIX Security 2026). arXiv:2607.19545.'
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Security study of x402, the HTTP 402 payment protocol for web APIs and AI agents, where third-party facilitators verify payment proofs and settle on chain. The authors define eight security rules for facilitators, derive four attacks (Free Shopping, Asset Theft, Service Denial, Gas Abuse), and build a semi-automated black-box tester run against 15 major facilitators serving over 60K sellers and 360K buyers; all 15 violated at least one rule, and Coinbase among others adopted mitigations. They also measure over 119 million recent Base and Solana transactions to quantify x402 adoption, facilitator centralisation and ecosystem risk indicators.

## Contribution

Characterises the payment substrate through which agent swarms would transact and shows facilitator centralisation, which is also the natural observation point for agent-traffic measurement.

## Key results

- 15 of 15 tested facilitators violated at least one of eight security rules.
- Facilitators collectively serve over 60K sellers and 360K buyers; 119M+ Base and Solana transactions measured.

## Methods and models

Specification analysis, black-box conformance testing, responsible disclosure, chain measurement.

## Limitations and open questions

Abstract-level read; buyer counts are wallets, not distinct agents or humans. Venue line on the arXiv page says USENIX Security 2026; full proceedings citation not checked.

## Relevance to us

x402 facilitators see every agent payment, so they are where an agent-swarm census or honeypot would sit. Compare authenticity measurement in [[ling-2026-how]] and attack catalogue in [[li-2026-five]].
