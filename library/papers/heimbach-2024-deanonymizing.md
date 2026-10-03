---
id: heimbach-2024-deanonymizing
type: paper
title: 'Deanonymizing Ethereum Validators: The P2P Network Has a Privacy Issue'
authors: [Lioba Heimbach, Yann Vonlanthen, Juan Villacis, Lucianna Kiffer, Roger Wattenhofer]
year: 2024
venue: USENIX Security 2025 (extended version on arXiv)
url: https://arxiv.org/abs/2409.04366
doi: null
arxiv: '2409.04366'
cite: 'Heimbach, L., Vonlanthen, Y., Villacis, J., Kiffer, L., & Wattenhofer, R. (2024). Deanonymizing Ethereum Validators: The P2P Network Has a Privacy Issue. arXiv:2409.04366. Accepted at USENIX Security 2025.'
topics: [fork-merge-security, sybil-resistance]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 27 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

The authors show that Ethereum's peer-to-peer layer lets any node link validator identifiers to the IP addresses of the peers hosting them. Using data collected from four nodes over three days they located more than 15% of Ethereum validators, and they report the resulting distribution of validators across peers, countries and hosting organisations. The Ethereum Foundation paid a bug bounty for the finding. They propose mitigations for validators.

## Contribution

A measured network-layer deanonymisation of the parties that consensus-layer secret leader election tries to hide.

## Key results

- More than 15% of validators located from four vantage nodes over three days (abstract).
- Deanonymisation needs only ordinary participation in the P2P network.

## Methods and models

Passive measurement of gossip behaviour from connected peers (details not read beyond the abstract).

## Limitations and open questions

Only the abstract was read; coverage is limited to validators on directly connected peers.

## Relevance to us

Q1. Protocol-level hiding of which part acts (SSLE, [[boneh-2020-single]], [[ethresear-2022-whisk]]) assumes the transport does not leak identity; this paper measures that it does. For a fork-merge agent the lesson is that hiding which sub-agent will be reintegrated is defeated if the side channel (where its traffic comes from, how it gossips) links it to the parent, so the selection layer needs a metadata-hiding transport underneath, such as [[piotrowska-2017-loopix]]. The same point for LLM agent protocols is made in [[dangol-2026-privacy]]. Simulated consequences of 80% IP linkability are in [[burianova-2025-secret]].
