---
id: venugopalan-2024-fp-inconsistent
type: paper
title: "FP-Inconsistent: Measurement and Analysis of Fingerprint Inconsistencies in Evasive Bot Traffic"
authors: ["Hari Venugopalan", "Shaoor Munir", "Shuaib Ahmed", "Tangbaihe Wang", "Samuel T. King", "Zubair Shafiq"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2406.07647
doi: "10.48550/arXiv.2406.07647"
arxiv: "2406.07647"
cite: "Venugopalan, H., Munir, S., Ahmed, S., Wang, T., King, S. T., & Shafiq, Z. (2024). FP-Inconsistent: Measurement and Analysis of Fingerprint Inconsistencies in Evasive Bot Traffic. arXiv preprint arXiv:2406.07647."
topics: ["swarm-detection", "sybil-resistance"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: "6 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Venugopalan, Munir, Ahmed, Wang, King and Shafiq bought traffic from 20 bot services that sell 'realistic and undetectable' visits and pointed it at a honey site protected by DataDome and BotD. Over about half a million requests, average evasion was 52.93% against DataDome and 44.56% against BotD. Evasive bots alter fingerprint attributes but leave inconsistencies, both within one fingerprint (two attributes that cannot co-occur) and over time (one attribute that changes when it should not). Data-driven rules for these spatial and temporal inconsistencies cut evasion against DataDome by 48.11% and against BotD by 44.95%.

## Contribution

The pre-LLM baseline for honeypot measurement of commercial evasive bots, and the inconsistency-rule method that [[fayolle-2026-internet]] and [[wang-2026-fp-agent]] build on.

## Key results

- Measured (abstract): 20 bot services, about 500,000 requests.
- Measured (abstract): evasion 52.93% vs DataDome, 44.56% vs BotD.
- Measured (abstract): inconsistency rules reduce evasion by 48.11% (DataDome) and 44.95% (BotD).

## Methods and models

Honey site with two anti-bot services; purchased bot traffic; mining of attribute-pair and attribute-over-time inconsistency rules. Abstract only.

## Limitations and open questions

Abstract only. Bot services, not LLM agents; rules may be evaded once published.

## Relevance to us

Method template for a swarm honeypot: buy or attract the traffic, then mine consistency rules. Inconsistent fingerprints are also what made 'stealth' agents more detectable in [[fayolle-2026-internet]]. Same senior author as [[wang-2026-fp-agent]].
