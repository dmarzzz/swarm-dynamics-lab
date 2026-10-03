---
id: tran-2009-sybil-resilient
type: paper
title: "Sybil-Resilient Online Content Voting"
authors: ["Nguyen Tran", "Bonan Min", "Jinyang Li", "Lakshminarayanan Subramanian"]
year: 2009
venue: "6th USENIX Symposium on Networked Systems Design and Implementation (NSDI 2009)"
url: https://www.usenix.org/legacy/event/nsdi09/tech/full_papers/tran/tran.pdf
doi: null
arxiv: null
cite: "Tran, N., Min, B., Li, J., & Subramanian, L. (2009). Sybil-Resilient Online Content Voting. In 6th USENIX Symposium on Networked Systems Design and Implementation (NSDI 09). USENIX Association."
topics: [sybil-resistance, collective-decision]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "259 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

SumUp is a vote aggregation system that bounds the influence of Sybil voters using max-flow on the trust network. A vote collector assigns link capacities that adapt to the expected number of votes ("adaptive vote flow"), so that with high probability the number of bogus votes accepted is at most the number of attack edges, while most honest votes still get through. User feedback on votes further shrinks the capacity of attack edges belonging to adversaries who repeatedly vote for content others reject.

## Contribution

Moves the social-graph defence from "is this identity real?" to "how much can this group of voters move the aggregate?", which is the question collective decision systems actually need answered.

## Key results

- Guarantee: bogus votes collected ≤ number of attack edges, with high probability; persistent misbehavers are pushed below their attack-edge count.
- Evaluated on YouTube and Flickr social graphs.
- Applied to a Digg voting trace and found strong evidence of Sybil voting on many articles that Digg had marked popular (measured on the trace; attribution to attack is the authors' inference).

## Methods and models

Ticket distribution and max-flow from the vote collector, capacity assignment by distance level, adaptive capacity scaling to the expected vote count, negative feedback to reduce link capacity.

## Limitations and open questions

Depends on a trust network with few attack edges; a single collector computes flows; honest votes far from the collector may be lost when capacity is tight.

## Relevance to us

Directly relevant to collective decision in agent swarms: when agents vote or rank proposals, SumUp shows how to cap Sybil influence at the number of compromised trust links instead of the number of fake agents. It is a concrete aggregation rule that could be tested against cloned LLM voters, complementing the evidence-level view in [[bara-2026-epistemic]]. Background: [[yu-2006-sybilguard]], [[douceur-2002-sybil]].
