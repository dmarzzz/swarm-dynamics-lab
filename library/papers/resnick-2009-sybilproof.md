---
id: resnick-2009-sybilproof
type: paper
title: "Sybilproof transitive trust protocols"
authors: [Paul Resnick, Rahul Sami]
year: 2009
venue: Proceedings of the 10th ACM Conference on Electronic Commerce (EC '09), Stanford, pp. 345-354
url: https://dl.acm.org/doi/10.1145/1566374.1566423
doi: 10.1145/1566374.1566423
arxiv: null
cite: "Resnick, P., & Sami, R. (2009). Sybilproof transitive trust protocols. In Proceedings of the 10th ACM Conference on Electronic Commerce (EC '09), pp. 345-354. ACM. https://doi.org/10.1145/1566374.1566423"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "22 (Crossref, 2026-10-03)"
code: []
---

## Summary

Models risky interactions between a principal and an agent who lack direct trust, enabled instead through a chain of credit or trust links, a framing the authors say covers open currency systems, network trust aggregation and manipulation-resistant recommenders. Each party keeps a trust account (balance) for each other party; if the principal's balance for the agent covers the potential loss, direct trust suffices, and indirect trust along a path opens more interactions but also widens the attacker's strategy space, in particular Sybil strategies where the attacker inserts fake intermediaries. The main result is a friction theorem: any protocol satisfying "sum-sybilproofness" (an attacker cannot raise the total trust the community extends to its identities by splitting into Sybils) must sometimes reduce expected total trust balances even on interactions that are profitable in expectation, so indirect trust cannot be used freely if trust accounts are to grow over time. They then present the hedged-transitive protocol and show it achieves the optimal expected growth rate of trust accounts among all sum-sybilproof protocols. Abstract only (ACM paywalled, no OA copy found; abstract and reference list via Exa). The reference list places it in the lineage of Friedman and Resnick's "social cost of cheap pseudonyms", Levien's attack-resistant trust metrics and Cheng and Friedman's Sybilproof reputation.

## Contribution

Shows that Sybil-proofness in transitive trust has an unavoidable efficiency cost (friction) and characterises the protocol that minimises it.

## Key results

- Sum-sybilproofness forces occasional loss of expected trust even on positive-expectation interactions (impossibility of frictionless Sybil-proof indirect trust).
- Hedged-transitive protocol is growth-rate optimal among sum-sybilproof protocols.

## Methods and models

Game-theoretic model of trust balances as transferable assets along paths; strategic safety definitions; growth-rate analysis. Details not read.

## Limitations and open questions

Abstract-level read. Model treats trust as fungible balances, which fits credit networks better than reputation; whether real systems can implement hedging is not visible from the abstract.

## Relevance to us

The theory counterpart to credit-network and web-of-trust Sybil defences: it tells an agent-platform designer that routing trust through intermediaries can be made Sybil-proof only by accepting slower trust growth, which is the same trade-off that [[wagman-2008-optimal]] finds for voting (cost buys responsiveness) and that [[cheng-2005-sybilproof]] finds for reputation (flow-based metrics only). Compare [[marti-2004-limited]] (empirical whitewashing cost) and [[kash-2012-optimizing]] (scrip Sybils). Root: [[douceur-2002-sybil]].
