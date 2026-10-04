---
id: mohaisen-2013-sybil
type: paper
title: "The Sybil Attacks and Defenses: A Survey"
authors: ["Aziz Mohaisen", "Joongheon Kim"]
year: 2013
venue: "arXiv preprint (cs.CR); also published in Smart Computing Review"
url: https://arxiv.org/pdf/1312.6349
doi: null
arxiv: "1312.6349"
cite: "Mohaisen, A., & Kim, J. (2013). The Sybil Attacks and Defenses: A Survey. arXiv preprint arXiv:1312.6349."
topics: [sybil-resistance, meta]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "52 (OpenAlex, Smart Computing Review version, 2026-10-03)"
code: []
---

## Summary

A survey of Sybil attacks and defences in peer-to-peer overlays, structured (Chord, Kademlia) and unstructured (Gnutella). It describes what limits the number of identities an attacker can create (bandwidth, memory, computation), and reviews centralised certification, resource-based defences, and social-network-based defences such as SybilGuard, SybilLimit, SybilInfer and SumUp, comparing their assumptions, features and shortcomings.

## Contribution

A mid-point survey between [[levine-2006-survey]] and [[alvisi-2013-sok]]. It differs from Levine et al. by evaluating the merits and shortcomings of each defence rather than only classifying them, as the authors state in their related-work section.

## Key results

- No new measurements; comparative discussion of defences.
- Notes that hardware growth in storage and processing weakens resource-based limits on identity creation.

## Methods and models

Literature survey (10 pages).

## Limitations and open questions

Narrow to P2P overlays; short treatment of each scheme; pre-dates blockchain work.

## Relevance to us

A secondary source; useful mainly as an index into the 2006-2012 social-graph literature and for the observation that resource limits on identity erode as hardware gets cheaper, which applies even more strongly to LLM agent instances whose marginal cost keeps falling. Primary sources: [[yu-2006-sybilguard]], [[yu-2008-sybillimit]], [[danezis-2009-sybilinfer]], [[tran-2009-sybil-resilient]].
