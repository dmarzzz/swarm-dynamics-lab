---
id: flashbots-2022-order
type: blog
title: "order flow, auctions and centralisation II - order flow auctions"
authors: [Quintus Kilbourn]
year: 2022
url: https://writings.flashbots.net/order-flow-auctions-and-centralisation-II
site: writings.flashbots.net
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 2
---

## Summary

Second post (2022-09-19) in a Flashbots series on exclusive order flow and builder centralisation. It argues that users are in a negotiating position comparable to validators and proposes order flow auctions (OFAs) that face "the other way", with extractors bidding to users for the right to execute their orders. It compares explicit auctions, fee escalators and other designs. For identity, the relevant passage is how to stop winning bidders who never execute, by reputation or by unconditional payment.

## Key claims

- In an explicit OFA, a winner may overbid or bid "with no intention of executing it simply to grief competitors"; the auction then needs a restart or a fallback, at a latency cost.
- Two disincentives are named: a reputation system (Rook was building one) and the "harsher" requirement of unconditional bids, where winners pay whether or not they execute.
- Execution enforcement pushes winners to send bundles to many builders, fragmenting extraction; designs must trade enforcement against efficiency.
- The post notes that all current explicit auctions rely on a trusted auctioneer and calls for trust-minimised designs.

## Evidence quality

Conceptual design essay, no data. The reputation versus upfront-payment comparison is later formalised in [[resnick-2023-contingent]], a Flashbots-funded paper.

## Relevance to us

Griefing by non-executing winners is a Sybil-adjacent problem: if penalties attach to an identity (reputation), an attacker can grief from disposable identities; if penalties attach to money (unconditional bids), identity stops mattering. The same choice appears for agent task markets, where an agent can win tasks and not deliver. The post points to payment-based enforcement as the identity-independent option, consistent with [[resnick-2023-contingent]] and with the spam-pricing argument in [[flashbots-2025-mev]].
