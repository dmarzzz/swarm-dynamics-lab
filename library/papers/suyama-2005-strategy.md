---
id: suyama-2005-strategy
type: paper
title: "Strategy/False-name Proof Protocols for Combinatorial Multi-Attribute Procurement Auction"
authors: [Takayuki Suyama, Makoto Yokoo]
year: 2005
venue: Autonomous Agents and Multi-Agent Systems, vol. 11, no. 1, pp. 7-21 (conference version AAMAS 2004, pp. 160-167)
url: https://doi.org/10.1007/s10458-005-0983-2
doi: 10.1007/s10458-005-0983-2
arxiv: null
cite: "Suyama, T., & Yokoo, M. (2005). Strategy/False-name Proof Protocols for Combinatorial Multi-Attribute Procurement Auction. Autonomous Agents and Multi-Agent Systems, 11(1), 7-21. https://doi.org/10.1007/s10458-005-0983-2"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "10 (Crossref, 2026-10-03)"
code: []
---

## Summary

Procurement (reverse) version of the false-name-proof combinatorial auction problem: the auctioneer is a buyer (e.g. a government), bidders are sellers, there are multiple items, each item is described by quality attributes as well as price, and both sides may have arbitrary substitute or complement preferences over bundles. The paper first gives a VCG-type protocol and shows that, as in forward combinatorial auctions, it is strategy-proof but not false-name-proof (a seller can gain by bidding under several identifiers). It then shows that any strategy-proof protocol in this model can be written as a price-oriented rationing-free (PORF) protocol, where for each bidder, each bundle and each quality level the payment is fixed independently of that bidder's own declaration and the bidder receives the bundle-quality pair that maximises its utility independently of others' allocations, extending Yokoo's 2003 characterisation to the multi-attribute procurement setting. Finally it constructs a false-name-proof protocol within that framework. Abstract only (Springer paywalled; abstract from the AAMAS 2004 conference record on Vidal's library page, which matches the journal abstract). The construction and any efficiency analysis are not visible.

## Contribution

Extends false-name-proof mechanism design to procurement with quality attributes, re-deriving the PORF characterisation there and giving a Sybil-robust protocol for buyers facing possibly duplicated sellers.

## Key results

- VCG-type procurement protocol is not false-name-proof.
- Strategy-proof multi-attribute procurement protocols are exactly PORF protocols (per abstract).
- A false-name-proof protocol exists in this model (construction not read).

## Methods and models

Quasi-linear multi-attribute procurement auction, dominant-strategy analysis, PORF framework; details not read.

## Limitations and open questions

Abstract-level. Efficiency loss not stated; identities costless; quality attributes assumed verifiable by the buyer.

## Relevance to us

Procurement is the direction that matters for an agent platform buying work from agents (as opposed to selling resources to them): when sellers can be one operator wearing many identities, VCG-style procurement is gameable and a PORF-style price schedule per bundle-and-quality is the known fix. Companion to [[lin-2017-sybil-proof]] (crowdsensing procurement), [[yokoo-2003-characterization]] (PORF), [[todo-2009-characterizing]] (implementability test), [[iwasaki-2010-worst-case]] (efficiency cost). Root: [[douceur-2002-sybil]].
