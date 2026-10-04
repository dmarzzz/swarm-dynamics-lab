---
id: zhang-2011-survey
type: paper
title: "A Survey on Trust Management for VANETs"
authors: [Jie Zhang]
year: 2011
venue: 2011 IEEE 25th International Conference on Advanced Information Networking and Applications (AINA), pp. 105-112
url: https://ieeexplore.ieee.org/document/5763114
doi: 10.1109/aina.2011.86
arxiv: null
cite: "Zhang, J. (2011). A Survey on Trust Management for VANETs. In 2011 IEEE International Conference on Advanced Information Networking and Applications (AINA), pp. 105-112. IEEE. https://doi.org/10.1109/AINA.2011.86"
topics: [sybil-resistance, crowds-and-traffic]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "179 (Crossref, 2026-10-03)"
code: []
---

## Summary

Short survey (8 pages) motivated by vehicular ad-hoc networks (VANETs), where cars act on safety and traffic messages from peers they have never met, so false reports from malicious vehicles have physical consequences. The paper first lists the properties of VANETs that make trust hard (high mobility, large scale, sparse repeated interactions, real-time constraints, no fixed infrastructure), then surveys existing trust models from three communities, multi-agent systems, mobile ad-hoc networks (MANETs) and VANETs proper, and points out their key issues. From that it proposes a list of desired properties for VANET trust management as goals for the field. Abstract only (IEEE Xplore page; paywalled, no OA copy via Unpaywall). The specific desired properties and the models surveyed are not in the abstract.

## Contribution

Early consolidation of trust-management work for vehicular networks, notable for explicitly importing the multi-agent-systems reputation literature into the VANET setting and for framing requirements rather than proposing a model.

## Key results

- Qualitative: VANET characteristics defeat MAS and MANET trust models designed for repeated interaction among a stable population (abstract).
- Proposes desired properties for VANET trust management (list not visible from abstract).

## Methods and models

Literature survey; no experiments.

## Limitations and open questions

Abstract-only read; 2011 venue so pre-dates connected-vehicle standards and any learning-based trust. Trust management assumes identities are at least somewhat stable; the Sybil problem (one vehicle presenting many identities to fake a traffic jam) is the main reason VANET trust is hard, but the abstract does not say how the surveyed models treat it.

## Relevance to us

Background. VANETs are an instructive physical-world case of a swarm of mobile agents with weak identities and one-shot interactions, which is close to the LLM-agent setting where reputation cannot accumulate. Of use mainly as a pointer when the sybil-resistance survey covers reputation-based defences; the actual Sybil-detection work for vehicles is not yet in the library (gap for the collectors). Compare the social-graph family in [[yu-2011-sybil]], which VANETs cannot use, and the taxonomy in [[urdaneta-2011-survey]]. Root: [[douceur-2002-sybil]].
