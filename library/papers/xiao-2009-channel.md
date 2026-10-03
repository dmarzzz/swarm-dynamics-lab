---
id: xiao-2009-channel
type: paper
title: "Channel-Based Detection of Sybil Attacks in Wireless Networks"
authors: ["Liang Xiao", "Larry J. Greenstein", "Narayan B. Mandayam", "Wade Trappe"]
year: 2009
venue: "IEEE Transactions on Information Forensics and Security"
url: https://api.openalex.org/works/doi:10.1109/tifs.2009.2026454
doi: "10.1109/tifs.2009.2026454"
arxiv: null
cite: "Xiao, L., Greenstein, L. J., Mandayam, N. B., & Trappe, W. (2009). Channel-Based Detection of Sybil Attacks in Wireless Networks. IEEE Transactions on Information Forensics and Security, 4(3), 492-503."
topics: [sybil-resistance]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "160 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Physical-layer authentication against Sybil clients: exploits spatial variability of radio channels in rich-scattering indoor and urban environments and builds a hypothesis test for wideband and narrowband systems (WiFi, WiMax) using existing channel estimation. Verified with propagation modelling software and field measurements with a vector network analyzer.

## Contribution

The wireless-security precursor that robotics Sybil defences ([[gil-2015-guaranteeing]], [[huang-2019-lightweight]]) build on and argue against (static nodes, bulky hardware).

## Key results

- False alarm and miss rates usually below 0.01 with three tones, 10 mW pilot power and 20 MHz bandwidth (abstract).

## Methods and models

Channel-response hypothesis testing. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Assumes static clients; mobility makes channels fluctuate, which is the gap the robotics work addresses.

## Relevance to us

Background for the claim that the physical channel is an identity anchor; the general principle (use a signal the attacker cannot cheaply duplicate) is what transfers to agents.
