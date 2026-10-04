---
id: wang-2017-robust
type: paper
title: "Robust Large-Scale Spectrum Auctions against False-Name Bids"
authors: [Qinhui Wang, Baoliu Ye, Bin Tang, Tianyin Xu, Song Guo, Sanglu Lu, Weihua Zhuang]
year: 2017
venue: IEEE Transactions on Mobile Computing, vol. 16, no. 6, pp. 1730-1743 (conference version ALETHEIA, MobiHoc 2015)
url: https://ieeexplore.ieee.org/document/7548316
doi: 10.1109/tmc.2016.2601908
arxiv: null
cite: "Wang, Q., Ye, B., Tang, B., Xu, T., Guo, S., Lu, S., & Zhuang, W. (2017). Robust Large-Scale Spectrum Auctions against False-Name Bids. IEEE Transactions on Mobile Computing, 16(6), 1730-1743. https://doi.org/10.1109/TMC.2016.2601908"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "17 (Crossref, 2026-10-03)"
code: []
---

## Summary

Applies false-name-proof mechanism design to dynamic spectrum auctions in cognitive radio networks, where a primary user leases channels to many secondary users and channels can be reused by bidders far enough apart (spatial reuse via an interference graph). Existing spectrum auctions are strategy-proof but, the authors show, a bidder can gain by submitting bids under several fictitious names (e.g. splitting a request for a bundle of channels or regions), which is easy to do and hard to detect because the auctioneer only sees radios, not owners. ALETHEIA is a false-name-proof auction framework for large-scale dynamic spectrum access that preserves strategy-proofness, resists false-name bids and still allows spectrum reuse across many bidders; a generalised version lets bidders accept allocations that only partially satisfy their requests. Theoretical analysis and simulations show high spectrum redistribution efficiency and auction efficiency. Abstract only (IEEE paywalled; abstract from the OpenAlex record via Exa, matching the Xplore page). The construction is presumably a PORF/group-pricing design built on Yokoo et al.'s robust multi-unit auction, which the reference list cites, but the details and the efficiency numbers are not visible.

## Contribution

Shows false-name manipulation is practical in spectrum markets with spatial reuse and gives a false-name-proof, reuse-aware auction for them.

## Key results

- Existing strategy-proof spectrum auctions are vulnerable to false-name bids (abstract).
- ALETHEIA: strategy-proof + false-name-proof + spectrum reuse; generalised partial-satisfaction variant.
- High redistribution and auction efficiency in analysis and simulation (figures not visible).

## Methods and models

Interference-graph spectrum auction model, false-name-proof mechanism design, theoretical analysis plus simulation; details not read.

## Limitations and open questions

Abstract-level read. Efficiency loss relative to a non-FNP auction is unquantified from the abstract; identities costless; collusion among distinct bidders not covered.

## Relevance to us

Applied instance of the false-name-proof toolkit in a resource market with locality constraints, which resembles allocating compute or bandwidth among agents that interfere or share hosts. Theory lineage: [[sakurai-1999-limitation]], [[yokoo-2003-characterization]], [[todo-2009-characterizing]], [[iwasaki-2010-worst-case]]; sibling applications [[lin-2017-sybil-proof]], [[lin-2018-sybil-proof]], [[suyama-2005-strategy]]. Root: [[douceur-2002-sybil]].
