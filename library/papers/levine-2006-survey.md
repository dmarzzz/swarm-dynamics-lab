---
id: levine-2006-survey
type: paper
title: "A Survey of Solutions to the Sybil Attack"
authors: ["Brian Neil Levine", "Clay Shields", "N. Boris Margolin"]
year: 2006
venue: "Technical report, Department of Computer Science, University of Massachusetts Amherst"
url: http://forensics.umass.edu/pubs/levine.sybil.tr.2006.pdf
doi: null
arxiv: null
cite: "Levine, B. N., Shields, C., & Margolin, N. B. (2006). A Survey of Solutions to the Sybil Attack. Technical report, Department of Computer Science, University of Massachusetts Amherst."
topics: [sybil-resistance, meta]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "236 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A short early survey that classifies 90 papers mentioning the Sybil attack or "pseudospoofing" into categories of defence and lists application domains. About half of the papers either propose trusted certification or state the problem without a solution. The rest use resource testing, recurring costs and fees, trusted devices, or domain-specific methods for mobile networks, auditing, cash economies and reputation systems.

## Contribution

The first taxonomy of Sybil defences. Its key observations still organise the field: only certification can eliminate Sybils (following [[douceur-2002-sybil]]); resource tests only discourage; recurring fees beat one-time fees; and symmetric reputation systems are provably vulnerable while asymmetric ones (trust flowing from fixed seeds) are not.

## Key results

- Categories and counts are given in a bar chart (Figure 1); the text lists the papers in each.
- Resource testing (CPU, storage, bandwidth, IP diversity) only raises the cost; Tor needs only two Sybil identities for an anonymity attack, so even expensive identities can suffice.
- Recurring fees: the authors' earlier result (Margolin and Levine, cited as a 2005 report) that a recurring per-identity fee scales attacker cost linearly with identities while a one-time fee costs a constant.
- Reputation: citing Cheng and Friedman (2005), symmetric reputation (PageRank, EigenTrust) cannot distinguish an attacker's copied subgraph from the original; asymmetric reputation from trusted seeds resists this but penalises newcomers.
- Mobile networks: Sybil identities of a single device move together, which location tracking can detect.
- Auditing: Yurkewych et al. found that in p2p computing, redundancy plus majority voting is less cost-effective under Sybil attack than a large reward with limited auditing.
- Combinatorial auctions: Yokoo et al.'s false-name bids, removable by pricing so that bundles are never more expensive than parts.

## Methods and models

Literature classification; no new experiments.

## Limitations and open questions

Pre-dates the social-graph defences (SybilGuard is mentioned only briefly) and all blockchain and proof-of-personhood work. Short (six pages).

## Relevance to us

A compact checklist of options for any swarm: certify agents, charge them recurring costs, tie them to devices, exploit physics (co-moving identities), audit outputs instead of voting, or use asymmetric reputation from trusted seeds. The point that majority voting over redundant workers is Sybil-fragile, and auditing is better, applies directly to LLM agent ensembles that vote. The false-name-proof auction pointer belongs to the mechanism-design lane. Later surveys: [[mohaisen-2013-sybil]], [[alvisi-2013-sok]], [[siddarth-2020-who]].
