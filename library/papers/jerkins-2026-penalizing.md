---
id: jerkins-2026-penalizing
type: paper
title: "Penalizing Malicious Web Bots with an Allow List Based Reverse Proxy and Tarpit"
authors: ["James A. Jerkins"]
year: 2026
venue: "Proceedings of the 2026 ACM Southeast Conference"
url: https://www.semanticscholar.org/paper/893116012e8b5310b2665c55bba5d7b8c99b3e7f
doi: "10.1145/3746467.3801539"
arxiv: null
cite: "Jerkins, J. A. (2026). Penalizing Malicious Web Bots with an Allow List Based Reverse Proxy and Tarpit. In Proceedings of the 2026 ACM Southeast Conference (ACMSE 2026), pp. 293-297. https://doi.org/10.1145/3746467.3801539."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: "0 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Jerkins combines stock reverse-proxy software with an allow list and a purpose-built HTTP tarpit daemon so that requests not on the allow list are held open slowly, shifting cost back to bot operators instead of just dropping requests. A trial deployment showed less malicious bot traffic than in the pre-deployment period.

## Contribution

Cost-imposition rather than classification; a small practitioner paper on tarpits.

## Key results

- Measured (abstract): malicious bot traffic decreased after deployment compared to before; no figures in the abstract.

## Methods and models

Reverse proxy with allow list and a custom tarpit daemon; before/after comparison on one site. Abstract only.

## Limitations and open questions

Abstract only; one site, before/after design without a control.

## Relevance to us

Tarpits are one of the honeypot-adjacent tools named in our topic. Compare reasoning-cost throttling in [[kumar-2025-throttling]] and decoy content such as Cloudflare's AI Labyrinth (cited in [[fayolle-2026-internet]]).
