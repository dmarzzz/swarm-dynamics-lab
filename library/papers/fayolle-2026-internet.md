---
id: fayolle-2026-internet
type: paper
title: "On the Internet, Nobody Knows You're an LLM Bot: Unmasking Web Agents with Multi-Layer Fingerprinting"
authors: ["Iliana Fayolle", "Sihem Bouhenniche", "Samuel Pélissier", "Pierre Laperdrix", "Clémentine Maurice", "Walter Rudametkin"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.30119
doi: null
arxiv: "2606.30119"
cite: "Fayolle, I., Bouhenniche, S., Pélissier, S., Laperdrix, P., Maurice, C., & Rudametkin, W. (2026). On the Internet, Nobody Knows You're an LLM Bot: Unmasking Web Agents with Multi-Layer Fingerprinting. arXiv:2606.30119."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Deploys honeysites protected by robots.txt, CAPTCHAs, proof-of-work and Cloudflare's free bot protection, and prompts six LLM-based web agents to visit them while recording network, HTTP and browser-level fingerprints. Some agents bypassed every anti-bot mechanism; all evaluated agents could be distinguished from humans and from one another with multi-layer fingerprinting; stealth and anti-detection features often increased detectability.

## Contribution

Honeysite evaluation of anti-bot defences against LLM web agents, cloud and local.

## Key results

- Some web agents bypassed all evaluated anti-bot mechanisms (abstract).
- All six agents distinguishable from humans and from each other via multi-layer fingerprinting (abstract).
- Stealth features often increased detectability (abstract).

## Methods and models

Honeysites with combinations of defences; network, HTTP and browser fingerprint collection.

## Limitations and open questions

Six agents; abstract-only reading.

## Relevance to us

Stealth-backfires is a useful prior for swarm detection: evasion tooling itself becomes a signature. Related: [[kang-2026-whose]], [[wang-2026-fp]].
