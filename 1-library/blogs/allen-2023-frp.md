---
id: allen-2023-frp
type: blog
title: FRP Year in Review
authors:
- Sarah Allen
year: 2023
url: https://writings.flashbots.net/frp-year-in-review
site: Flashbots Writings
topics:
- sybil-resistance
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: skim
relevance: 2
---

## Summary

This grants-program retrospective maps Flashbots research on privacy, adversarial transaction queues, distributed block building, and auction incentives. Its most relevant section summarizes contingent-fee auctions: more contingent payments can lower revenue and execution probability and widen spreads, while a reputation-based remedy raises implementation difficulties. These are pointers to primary studies, not new results of the retrospective.

## Key claims

- FRP 28 compares contingent fees, upfront fees, and mixed payment rules; the summarized recommendation is to minimize contingent fees.
- FRP 22 introduces adversarial transaction queues as a common model for ordering incentives and execution quality.
- FRP 18 compares private-mempool cryptography and describes threshold encryption as the then-practical option.

## Evidence quality

Sponsor-authored research-program overview linking individual reports, papers, and code. Primary FRP studies were not read here, so their results are second-hand summaries. The program description and funding figures are administrative evidence, not security validation.

## Relevance to us

A citation-chasing map for reputation and auction incentives when participants may be adversarial. The post does not test false-name attacks; Sybil-resistant reputation would need separate primary evidence. Related practical protocol overview: [[smedley-2023-searching]].
