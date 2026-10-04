---
id: pecori-2016-s-kademlia
type: paper
title: "S-Kademlia: A trust and reputation method to mitigate a Sybil attack in Kademlia"
authors: [Riccardo Pecori]
year: 2016
venue: Computer Networks, vol. 94, pp. 205-218
url: https://doi.org/10.1016/j.comnet.2015.11.010
doi: 10.1016/j.comnet.2015.11.010
arxiv: null
cite: "Pecori, R. (2016). S-Kademlia: A trust and reputation method to mitigate a Sybil attack in Kademlia. Computer Networks, 94, 205-218. https://doi.org/10.1016/j.comnet.2015.11.010"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "24 (Crossref, 2026-10-03)"
code: []
---

## Summary

Addresses routing-table poisoning by Sybil identities in Kademlia DHTs (the overlay beneath BitTorrent's DHT, eMule's KAD and many P2P VoIP systems). Rather than preventing fake identities, the paper surveys countermeasures and proposes S-Kademlia, a routing and storage/retrieval procedure that mixes standard Kademlia bucket and lookup rules with a trust-based algorithm driven by reputation: peers score their contacts on observed behaviour (e.g. correct responses to FIND_NODE/FIND_VALUE) and bias which contacts are used and kept so that Sybil-populated regions of the ID space are avoided. The abstract reports "promising results" against a Sybil attack and favourable comparison with similar trust-based methods (Kohnen's trust-enabled Kademlia is in the reference list). Abstract only (Elsevier paywalled and bot-walled from this box; abstract from the author's institutional repository). Simulation platform, attack strength and lookup-success numbers are not visible; the reference list places it in the lineage of Danezis et al.'s Sybil-resistant DHT routing and the Levine et al. Sybil survey.

## Contribution

A trust-and-reputation overlay on Kademlia's routing and storage that degrades gracefully under Sybil routing-table poisoning without changing identity assignment.

## Key results

- Qualitative: improved routing and storage/retrieval success under Sybil attack versus plain Kademlia and prior trust-based variants (abstract; no numbers visible).

## Methods and models

Kademlia with per-contact trust scores and reputation exchange; simulation comparison; details not read.

## Limitations and open questions

Abstract-level read. Reputation in a Sybil setting is itself attackable (Sybils vouch for Sybils), so the scheme's guarantees depend on bootstrapping trust from honest observations; this is not visible from the abstract. Single-author journal paper with modest uptake.

## Relevance to us

Representative of the "tolerate and route around" school for Sybils in DHTs, alongside [[puttaswamy-2009-securing]] and the hardened design [[baumgart-2007-skademlia]] (S/Kademlia, a different paper despite the similar name). Mostly background; the live-network measurements in [[steiner-2007-exploiting]] and [[eisenbarth-2022-ethereum]] are the more useful citations. Taxonomy: [[urdaneta-2011-survey]]. Root: [[douceur-2002-sybil]].
