---
id: yokoo-2005-robust
type: paper
title: "Robust double auction protocol against false-name bids"
authors: [Makoto Yokoo, Yuko Sakurai, Shigeo Matsubara]
year: 2005
venue: Decision Support Systems, vol. 39, no. 2, pp. 241-252 (conference version ICDCS 2001)
url: https://doi.org/10.1016/j.dss.2003.10.009
doi: 10.1016/j.dss.2003.10.009
arxiv: null
cite: "Yokoo, M., Sakurai, Y., & Matsubara, S. (2005). Robust double auction protocol against false-name bids. Decision Support Systems, 39(2), 241-252. https://doi.org/10.1016/j.dss.2003.10.009"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "3 (Crossref, 2026-10-03; the ICDCS 2001 conference version is cited more widely)"
code: []
---

## Summary

Extends the false-name-bid programme to double auctions (many buyers and many sellers of one good, the structure of stock, bond and FX markets). Without false names the PMD protocol (McAfee-style price-matching double auction) is dominant-strategy incentive compatible; the paper shows PMD loses that property once a participant can submit bids under fictitious names, then proposes the Threshold Price Double auction (TPD) protocol, which stays dominant-strategy incentive compatible under false-name bids. TPD fixes a threshold price in advance; the number of trades and the exchange prices are controlled by that threshold (buyers above and sellers below it trade at prices determined relative to the threshold rather than by each other's bids), which removes the incentive to split bids. Simulations show TPD's social surplus is very close to Pareto efficient. Abstract only (Elsevier paywalled, no OA copy); abstract text from the OpenAlex record of the conference version via Exa, which matches the journal abstract on the Elsevier page.

## Contribution

A false-name-proof double auction, showing that two-sided markets can be made Sybil-robust by anchoring prices to an exogenous threshold at a small efficiency cost.

## Key results

- PMD is not false-name-proof; TPD is dominant-strategy IC under false-name bids.
- TPD surplus close to Pareto efficient in simulation (abstract; no figures visible).

## Methods and models

Quasi-linear double-auction model, dominant-strategy analysis, simulation of surplus against the efficient benchmark; details not read.

## Limitations and open questions

Abstract-level read. Choice of threshold price requires prior information or a separate mechanism; efficiency loss is quantified only in simulation; single homogeneous good.

## Relevance to us

Completes the mechanism-design triad in the library: one-sided auctions ([[sakurai-1999-limitation]], [[yokoo-2003-characterization]], [[yokoo-2006-false]]), voting ([[wagman-2008-optimal]], [[bachrach-2008-divide]]) and now two-sided exchange. If agents trade compute, data or tasks with one another in a market, TPD-style threshold pricing is the known Sybil-robust design. General framework: [[yokoo-2000-effect]]; overview: [[conitzer-2010-using]]. Root: [[douceur-2002-sybil]].
