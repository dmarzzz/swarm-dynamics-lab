---
id: iwasaki-2003-robust
type: paper
title: "A robust open ascending-price multi-unit auction protocol against false-name bids"
authors: [Atsushi Iwasaki, Makoto Yokoo, Kenji Terada]
year: 2003
venue: Proceedings of the 4th ACM Conference on Electronic Commerce (EC '03), San Diego, pp. 85-92 (journal version in Decision Support Systems 39(1), 2005)
url: https://dl.acm.org/doi/10.1145/779928.779939
doi: 10.1145/779928.779939
arxiv: null
cite: "Iwasaki, A., Yokoo, M., & Terada, K. (2003). A robust open ascending-price multi-unit auction protocol against false-name bids. In Proceedings of the 4th ACM Conference on Electronic Commerce (EC '03), pp. 85-92. ACM. https://doi.org/10.1145/779928.779939"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "2 (Crossref, 2026-10-03; journal version cited more)"
code: []
---

## Summary

Presents what the authors call the first open-format (ascending-price) multi-unit auction in which sincere bidding is an equilibrium even when agents' marginal utilities can increase and agents can submit false-name bids. Context: VCG is sealed-bid and loses truthfulness under false names with increasing marginal utility; the authors' earlier Iterative Reducing (IR) protocol is false-name-robust but sealed-bid and needs the auctioneer to pre-set a reservation price for one unit; open ascending formats like Ausubel's are preferred in practice for simplicity, privacy and revenue. The protocol extends the Ausubel auction (clinching) to handle increasing marginal utilities while remaining robust to false-name bids and without any reservation price. Simulations show social surplus close to Pareto efficient and better surplus and seller revenue than IR. Abstract only (ACM paywalled; abstract from the ACM DL page via Exa). The clinching rule modification and simulation parameters are not visible.

## Contribution

A false-name-robust auction in the practically preferred open ascending format, removing the reservation-price requirement of earlier sealed-bid false-name-proof protocols.

## Key results

- Sincere bidding is an equilibrium under increasing marginal utilities and false-name bids in an open format (abstract).
- Simulation: near-Pareto-efficient surplus; beats IR on surplus and revenue (numbers not visible).

## Methods and models

Multi-unit auction with possibly increasing marginal utilities, Ausubel-style ascending clinching, equilibrium analysis, simulation. Details not read.

## Limitations and open questions

Abstract-level read. Equilibrium (not dominant-strategy) guarantee; identities costless; multi-unit homogeneous goods only.

## Relevance to us

Fills in the "open/iterative format" branch of false-name-proof design, which matters if agent markets run as ascending auctions (common for compute spot markets) rather than sealed bids. Lineage: [[sakurai-1999-limitation]], [[yokoo-2000-effect]], [[yokoo-2003-characterization]]; sibling two-sided design [[yokoo-2005-robust]]; efficiency cost context [[iwasaki-2010-worst-case]]. Root: [[douceur-2002-sybil]].
