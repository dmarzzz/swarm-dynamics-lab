---
id: bazzi-2005-establishment
type: paper
title: "On the establishment of distinct identities in overlay networks"
authors: ["Rida A. Bazzi", "Goran Konjevod"]
year: 2005
venue: "Proceedings of the 24th Annual ACM Symposium on Principles of Distributed Computing (PODC 2005), pp. 312-320; journal version in Distributed Computing 19(4):267-287, 2007"
url: https://asu.elsevierpure.com/en/publications/on-the-establishment-of-distinct-identifies-in-overlay-networks/
doi: "10.1145/1073814.1073873"
arxiv: null
cite: "Bazzi, R. A., & Konjevod, G. (2005). On the establishment of distinct identities in overlay networks. In Proceedings of the 24th Annual ACM Symposium on Principles of Distributed Computing (PODC 2005), pp. 312-320. ACM. Journal version: Distributed Computing, 19(4), 267-287 (2007), doi:10.1007/s00446-006-0012-y."
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "98 (Semantic Scholar, journal version record, 2026-10-03)"
code: []
---

## Summary

Bazzi and Konjevod show that certificates testing whether two identities belong to distinct entities can be issued remotely and anonymously, without a central authority that knows the participants. Their protocols use distance geometry: certifiers measure distances (for example network delays) to an applicant and establish its location in Euclidean or spherical space of any dimension, so identities sharing one physical location can be told apart from identities at different locations. The protocols tolerate corrupt certifiers and collusion between applicants and certifiers, in both broadcast and point-to-point message models.

## Contribution

According to the abstract, the first demonstration that remote anonymous certification of identity distinctness is possible under adversarial conditions. It is the geometric branch of resource testing in the sense of [[douceur-2002-sybil]]: the scarce resource is physical position rather than compute.

## Key results

- Remote, anonymous certification of distinct identities is possible under adversarial conditions (claimed in the abstract; I did not read the proofs).
- Certification works in Euclidean or spherical geometry of arbitrary dimension and does not need a centralised certifying authority.
- Tolerates corrupt certifiers and collusion between applicants and certifiers.

## Methods and models

Geometric, fault-tolerant distance measurements by multiple certifiers; analysis in broadcast and point-to-point models. Only the abstract, bibliographic record and keywords (distance geometry, fault tolerance, identity verification, Sybil attack) were read, from the ASU research portal. The Springer full text was not reachable.

## Limitations and open questions

Not read beyond the abstract, so the adversary bounds and measurement-error assumptions are not checked here. Location-based distinctness fails against an attacker who controls machines in many locations (a botnet or cloud tenant), and delay measurements can be inflated by the measured party.

## Relevance to us

For robot swarms and embodied agents, physical position is a natural distinctness test; this line connects to the signal-based Sybil detection in [[gil-2015-guaranteeing]] and [[newsome-2004-sybil]]. For software agents it maps to latency or network-location diversity checks, which the Bitcoin and Ethereum p2p fixes use in cruder form (/16 and /24 prefix limits in [[heilman-2015-eclipse]] and [[marcus-2018-low-resource]]). Bounds identities per location, not influence. It was listed as missing in the scan-papers-sybil-foundations coverage note.
