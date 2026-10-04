---
id: tsang-2026-anatomy
type: paper
title: 'The Anatomy of a Blockchain Prediction Market: Polymarket in the 2024 U.S. Presidential Election'
authors:
- Kwok Ping Tsang
- Zichao Yang
year: 2026
venue: arXiv preprint (q-fin)
url: https://arxiv.org/abs/2603.03136
doi: null
arxiv: '2603.03136'
cite: 'Tsang, K. P., & Yang, Z. (2026). The Anatomy of a Blockchain Prediction Market: Polymarket in the 2024 U.S. Presidential Election. arXiv preprint arXiv:2603.03136.'
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Uses Polymarket's full on-chain settlement ledger for the 2024 US presidential election markets. Because the platform mints and burns outcome shares inside trades, naive aggregation overstates turnover: October Trump-market turnover is $391M against $958M naive volume, and moving the forecast five points cost $9.1M rather than $15.6M. Capital entered on both sides throughout the month, which the authors read as heterogeneous beliefs rather than one-sided manipulation. The overstatement holds across 249 markets and is largest in thin, young markets.

## Contribution

A measurement correction showing on-chain 'volume' can be inflated by protocol mechanics alone, separate from wash trading, and a negative finding on one-sided manipulation of the headline market.

## Key results

- Naive volume overstates turnover by about 2.4x in October ($958M vs $391M); five-point move cost $9.1M not $15.6M.

## Methods and models

Transaction-level decomposition of mint, burn and transfer flows into turnover, net inflow and activity.

## Limitations and open questions

Abstract-level read; does not attempt account-level wash or bot detection.

## Relevance to us

Before attributing activity to swarms, correct for mechanical double counting; a caution for any activity-based prevalence estimate, alongside [[ling-2026-how]].
