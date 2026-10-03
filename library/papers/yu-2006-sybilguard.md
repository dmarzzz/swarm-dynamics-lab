---
id: yu-2006-sybilguard
type: paper
title: "SybilGuard: Defending Against Sybil Attacks via Social Networks"
authors: ["Haifeng Yu", "Michael Kaminsky", "Phillip B. Gibbons", "Abraham Flaxman"]
year: 2006
venue: "ACM SIGCOMM 2006"
url: https://www.comp.nus.edu.sg/~yuhf/sybilguard-sigcomm06.pdf
doi: "10.1145/1159913.1159945"
arxiv: null
cite: "Yu, H., Kaminsky, M., Gibbons, P. B., & Flaxman, A. (2006). SybilGuard: Defending Against Sybil Attacks via Social Networks. In Proceedings of the 2006 Conference on Applications, Technologies, Architectures, and Protocols for Computer Communications (SIGCOMM '06), pp. 267-278. ACM."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "266 (Crossref, SIGCOMM version, 2026-10-03); a journal version in IEEE/ACM ToN 2008 has 255 (Crossref)"
code: [gh-boshmaf-sypy]
---

## Summary

SybilGuard is the first decentralised Sybil defence that uses a social trust graph among identities instead of resource tests. The insight is that an attacker can create many Sybil nodes but few trust edges (attack edges) to honest users, so the cut between honest and Sybil regions is small. Each node performs a random route of length about √n log n; a verifier accepts a suspect if their routes intersect. With g attack edges, the number of Sybil groups and their size are bounded.

## Contribution

Replaces Douceur's resource assumption [[douceur-2002-sybil]] with a structural one: the honest region is fast mixing and attack edges are scarce. This defines the "social-graph Sybil defence" line that SybilLimit, SybilInfer, SumUp and SybilRank refine.

## Key results

- Measured in simulation: with one-million-node synthetic graphs, the number and size of Sybil groups were properly bounded for 99.8% of honest users, and an honest node accepted and was accepted by 99.8% of other honest nodes (conclusion section).
- Analytical: O(√n log n) Sybil nodes accepted per attack edge (this figure is stated in the follow-up [[yu-2008-sybillimit]] when comparing).
- Real social network data were not yet evaluated; the authors list this as future work.

## Methods and models

Crossref stores this DOI with the short title "SybilGuard"; the full title above is copied from the paper's first page, so `lab.py verify` reports a title mismatch that is a Crossref truncation, not a wrong DOI. Random routes (a deterministic per-node permutation of edges, so routes converge and are back-traceable), route intersection as the acceptance test, a decentralised protocol with witness tables. Synthetic Kleinberg-style social graphs for evaluation.

## Limitations and open questions

Relies on the fast-mixing assumption, which was not checked on real graphs here. Accepts up to O(√n log n) Sybils per attack edge, which [[danezis-2009-sybilinfer]] describes as high false negatives. [[viswanath-2010-analysis]] later shows the scheme effectively detects a local community around the verifier, so honest users in other communities get rejected.

## Relevance to us

For agent swarms the analogous scarce resource is "trust edges created by an independent party": human-attested delegations, cross-signed agent keys, or physical rendezvous between robots. SybilGuard gives the bounding argument (influence proportional to attack edges, not to identities) that an agent reputation graph would need. It also shows the cost: bounds are per attack edge, so one compromised honest agent with many links lets many Sybils in. Compare [[yu-2008-sybillimit]], [[tran-2009-sybil-resilient]], [[alvisi-2013-sok]].

## Notes from dmarz/sybil-code-data

A runnable SybilGuard detector is in the Python framework [[gh-boshmaf-sypy]], which stitches honest and Sybil regions with a chosen number of attack edges and reports accuracy, sensitivity and specificity. Later random-walk and belief-propagation detectors (SybilRank, SybilBelief, SybilSCAR) are implemented in [[gh-binghuiwang-sybildetection]], which we compiled and ran on its Facebook example (AUC 1 with 1,000 attack edges).
