---
id: yves-christian-2018-total
type: paper
title: "Total Eclipse: How To Completely Isolate a Bitcoin Peer"
authors: [Adja Elloh Yves-Christian, Badis Hammi, Ahmed Serhrouchni, Houda Labiod]
year: 2018
venue: 2018 Third International Conference on Security of Smart Cities, Industrial Control System and Communications (SSIC), Shanghai, pp. 1-7
url: https://ieeexplore.ieee.org/document/8556790
doi: 10.1109/ssic.2018.8556790
arxiv: null
cite: "Yves-Christian, A. E., Hammi, B., Serhrouchni, A., & Labiod, H. (2018). Total Eclipse: How To Completely Isolate a Bitcoin Peer. In 2018 Third International Conference on Security of Smart Cities, Industrial Control System and Communications (SSIC), pp. 1-7. IEEE. https://doi.org/10.1109/SSIC.2018.8556790"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "18 (Crossref, 2026-10-03)"
code: []
---

## Summary

Follow-on to Heilman et al.'s Bitcoin eclipse attack. The original attack monopolises a victim's outgoing (permanent) connections by filling its address tables with attacker IPs, but the victim's non-permanent incoming connections stay open and can leak honest blocks, weakening the eclipse. This paper (1) characterises Bitcoin Core's misbehaviour-scoring and banning mechanism and its weaknesses, and (2) gives a method to monopolise all of a peer's connections including the non-permanent ones, using a minimal number of IP addresses, by exploiting that misbehaviour mechanism (presumably by provoking the victim into banning honest peers or by occupying inbound slots). Characterisation and attack were carried out against a real client on the main Bitcoin network. Abstract only (IEEE paywalled, no OA copy); the IP count, the exact banning-logic exploit and success rates are not visible from the abstract.

## Contribution

Closes the inbound-connection gap in Bitcoin eclipse attacks and shows the client's own misbehaviour/ban logic can be turned into an isolation tool, with a live-network demonstration.

## Key results

- Complete isolation (all connections) with minimal IP addresses, validated on mainnet against a real client (abstract; numbers not visible).
- Bitcoin's misbehaviour mechanism identified as an attack surface.

## Methods and models

Protocol analysis of Bitcoin Core peer management; live attack realisation. Details not read.

## Limitations and open questions

Abstract-level read; small venue; Bitcoin Core has since changed address management (e.g. anchor connections, feeler connections, asmap) so the specific exploit may be dated.

## Relevance to us

Minor addition to the eclipse case studies ([[heilman-2015-eclipse]], [[tan-2019-toward]], [[steiner-2007-exploiting]]): the lesson that defensive reputation/ban logic can be weaponised to isolate a node is relevant to any agent network that lets peers blacklist each other based on reported misbehaviour. Taxonomy: [[urdaneta-2011-survey]]. Root: [[douceur-2002-sybil]].
